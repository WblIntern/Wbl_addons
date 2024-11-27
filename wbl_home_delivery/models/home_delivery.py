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

from odoo import fields, models, api


class HomeDelivery(models.Model):
    _name = 'home.delivery'
    _description = "Home Delivery"

    name = fields.Char(string="Name")
    new_address = fields.Boolean(string="Ship to different Address")
    delivery_name = fields.Char(string="Customer")
    delivery_mobile = fields.Char(string="Mobile/Phone")
    delivery_email = fields.Char(string="Email")
    delivery_locality = fields.Char(string="Locality")
    delivery_street = fields.Char(string="Street")
    delivery_city = fields.Char(string="City")
    delivery_zip = fields.Char(string="Zip")
    delivery_time = fields.Char(string="Delivery Time")
    delivery_note = fields.Char(string="Order Note")
    is_published = fields.Boolean(string="Published")
    delivery_instruction = fields.Char(string="Delivery Instruction")
    delivery_person = fields.Char(string="Delivery Person")
    cashier = fields.Char(string="Cashier")
    session = fields.Char(string="Session")
    order_ref = fields.Char(string="Order Ref")
    order_date = fields.Char(string="Order Date")
    is_home_delivery = fields.Boolean(string="Is Home Delivery", default=False)
    order_note = fields.Char(string="Order Note")
    data_to_change = fields.Boolean(string="Data Alter", default=False)
    delivery_person_id = fields.Char(string="Delivery Person Id")
    pos_order = fields.Many2one(comodel_name='pos.order', string="Pos Order")
    home_delivery_date = fields.Char(string="Home Delivery Date")
    home_delivery_time = fields.Char(string="Home Delivery Time")

    def action_publish(self):
        self.is_published = False

    def action_unpublish(self):
        self.is_published = True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('home.delivery') or "New"
        return super(HomeDelivery, self).create(vals_list)
