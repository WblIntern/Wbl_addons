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
from odoo.exceptions import ValidationError


class DeliveryPerson(models.Model):
    _name = "delivery.person"

    name = fields.Char(string="Name")
    user = fields.Many2one(string="Delivery Person", comodel_name="res.partner")
    is_publish = fields.Boolean(string="Is Publish", default=False)
    delivery_person_mobile = fields.Char(string="Mobile No.")
    delivery_person_email = fields.Char(string="Email")
    pos_order = fields.Many2one(comodel_name='pos.order', string="Pos Order", ondelete="cascade", index=True)

    delivery_date = fields.Boolean(string="Delivery Date")
    delivery_time_slot = fields.Boolean(string="Delivery Time Slot")
    start_day_after = fields.Integer(string="Start After (x) Days")
    time_interval = fields.Integer(string="Time Interval")
    max_order_in_single_slot = fields.Integer(string="Maximum Order in Single Slot")
    time_schedule = fields.One2many(
        'delivery.time.schedule',
        inverse_name='delivery_carrier_id',
        string='Time Schedule'
    )
    order_preparation_time = fields.Selection(
        selection='_get_order_preparation_minutes',
        string='Order Preparation Time',
        default='15',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('delivery.person') or "New"
        return super(DeliveryPerson, self).create(vals_list)

    @api.onchange('user')
    def email(self):
        if self.user:
            self.delivery_person_email = self.user.email
            self.delivery_person_mobile = self.user.phone

    def action_published(self):
        self.is_publish = False

    def action_unpublished(self):
        self.is_publish = True

    @api.constrains('time_interval', 'delivery_time_slot')
    def _check_open_close_time(self):
        for record in self:
            if record.delivery_time_slot and record.time_interval < 1:
                raise ValidationError(
                    "Time Interval not mentioned!"
                )

    @staticmethod
    def _get_order_preparation_minutes():
        return [
            ('15', '15 minutes'),
            ('30', '30 minutes'),
            ('45', '45 minutes'),
            ('60', '60 minutes'),
            ('75', '75 minutes'),
            ('90', '90 minutes'),
            ('120', '120 minutes'),
            ('180', '180 minutes'),
        ]
