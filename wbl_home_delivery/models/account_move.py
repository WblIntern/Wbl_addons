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
from odoo import models, fields


class InheritAccountMove(models.Model):
    _inherit = "account.move"

    pos_order = fields.Many2one('pos.order', string="POS Order")

    selected_delivery_person = fields.Many2one(comodel_name='delivery.person', string="Delivery Partner",
                                               ondelete='cascade', related='pos_order.selected_delivery_person')
    delivery_person_name = fields.Char(string="Delivery Person Name", related='pos_order.delivery_person_name')
    delivery_person_email = fields.Char(string="Delivery Person Email", related='pos_order.delivery_person_email')
    delivery_person_mobile = fields.Char(string="Delivery Person Mobile No.",
                                         related='pos_order.delivery_person_mobile')
    home_delivery_date = fields.Char(string="Home Delivery Date", related='pos_order.home_delivery_date')
    home_delivery_time = fields.Char(string="Home Delivery Time", related='pos_order.home_delivery_time')
    delivery_instruction = fields.Char(string="Delivery Instruction", related='pos_order.delivery_instruction')
    order_note = fields.Char(string="Order Note", related='pos_order.order_note')
    is_home_delivery = fields.Boolean(string="Is Home Delivery", default=False, related='pos_order.is_home_delivery')

    def _compute_is_being_sent(self):
        response = super(InheritAccountMove, self)._compute_is_being_sent()
        pos_order = self.env['pos.order'].sudo().search([('account_move', '=', self.id)])
        if pos_order:
            for order in pos_order:
                self.write({
                    "pos_order": order,
                    "selected_delivery_person": order.selected_delivery_person,
                    "delivery_person_name": order.delivery_person_name,
                    "delivery_person_email": order.delivery_person_email,
                    "delivery_person_mobile": order.delivery_person_mobile,
                    "home_delivery_date": order.home_delivery_date,
                    "home_delivery_time": order.home_delivery_time,
                    "delivery_instruction": order.delivery_instruction,
                    "order_note": order.order_note,
                    "is_home_delivery": order.is_home_delivery
                })

        return response
