# -*- coding: utf-8 -*-
#
#################################################################################
# Author      : Weblytic Labs Pvt. Ltd. (<https://store.weblyticlabs.com/>)
# Copyright(c): 2023-Present Weblytic Labs Pvt. Ltd.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
##################################################################################

from odoo import models, fields, api


class InheritPosOrder(models.Model):
    _inherit = "pos.order"

    is_home_delivery = fields.Boolean(string="Is Home Delivery", default=False)
    order_note = fields.Char(string="Order Note")
    delivery_instruction = fields.Char(string="Delivery Instruction")
    home_delivery = fields.One2many(comodel_name='home.delivery', inverse_name="pos_order", string="Home Delivery")
    delivery_person = fields.One2many(comodel_name='delivery.person', inverse_name="pos_order",
                                      string="Delivery Person")
    delivery_person_name = fields.Char(string="Delivery Person Name")
    delivery_person_email = fields.Char(string="Delivery Person Email")
    delivery_person_mobile = fields.Char(string="Delivery Person Mobile No.")
    delivery_time = fields.Char(string="Deliver By")
    home_delivery_date = fields.Char(string="Home Delivery Date")
    home_delivery_time = fields.Char(string="Home Delivery Time")
    home_delivery_person_id = fields.Char(string="Home Delivery Person Id")
    selected_delivery_person = fields.Many2one(comodel_name='delivery.person', string="Delivery Partner",
                                               ondelete='cascade')

    @api.onchange('selected_delivery_person')
    def change_info(self):
        self.write({
            "delivery_person_name": self.selected_delivery_person.user.name,
            "delivery_person_email": self.selected_delivery_person.user.email,
            "delivery_person_mobile": self.selected_delivery_person.user.phone
        })

    @api.model
    def _payment_fields(self, order, ui_paymentline):
        response = super(InheritPosOrder, self)._payment_fields(order=order, ui_paymentline=ui_paymentline)
        payment_method = ui_paymentline.get('payment_method_id')
        if payment_method:
            pos_order = self.env['pos.order'].sudo().search([('id', '=', order.id)], order='id desc', limit=1)
            home_delivery = self.env['home.delivery'].sudo().search([], order='id desc', limit=1)
            delivery_person = self.env['delivery.person'].sudo().search(
                [('id', '=', home_delivery.delivery_person_id)], order='id desc', limit=1)
            for rec in home_delivery:
                if rec.data_to_change:
                    for order in pos_order:
                        order.write({
                            "is_home_delivery": True,
                            "order_note": rec.order_note,
                            "delivery_instruction": rec.delivery_instruction,
                            "delivery_person_name": delivery_person.user.name,
                            "delivery_person_mobile": delivery_person.delivery_person_mobile,
                            "delivery_person_email": delivery_person.delivery_person_email,
                            "delivery_time": rec.delivery_time,
                            "home_delivery_date": rec.home_delivery_date,
                            "home_delivery_time": rec.home_delivery_time,
                            "home_delivery_person_id": delivery_person.id,
                            "selected_delivery_person": delivery_person.id

                        })
                    rec.write({
                        "data_to_change": False
                    })

            cashier_email = self.env.user.email
            customer_email = order.partner_id.email if order.partner_id else cashier_email
            delivery_instruction = order.delivery_instruction
            template = self.env.ref('wbl_home_delivery.mail_template_home_delivery_order')
            if template and order.is_home_delivery and delivery_person.delivery_person_email:
                email_values = {
                    'email_from': cashier_email,
                    'email_to': delivery_person.delivery_person_email,
                    'subject': 'Home Delivery Order',
                    'body_html': (
                        f"A Home Delivery Order has been placed and assigned to you with Order ID: {order.id}<br/>"
                        f"<p>Order Note: {order.order_note}</p>"
                        f"<p>Delivery Instruction: {order.delivery_instruction}</p>"
                    ),
                }
                template.sudo().send_mail(order.id, force_send=True, email_values=email_values)

        return response
