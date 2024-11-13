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

from odoo import fields, models


class CodSettingsRule(models.Model):
    _name = 'cod.settings.rule'
    _description = "Cod Settings Rule"

    name = fields.Char(string="Rule Name", required=True)
    min_order_amount = fields.Float(string='Minimum Order Amount')
    max_order_amount = fields.Float(string='Maximum Order Amount')
    product_ids = fields.Many2many(string="Disable COD for the Products", comodel_name='product.product')
    partner_ids = fields.Many2many(string='Disable COD for the Customers', comodel_name='res.partner')
    date_begin = fields.Datetime(string='Start Date')
    date_end = fields.Datetime(string='End Date')
    # country_id = fields.Many2one('res.country', string='Country')
    country_region = fields.One2many(comodel_name='cod.country.region', inverse_name='setting_rule_id',
                                     string='Available COD for the Locations')
    cod_available_alert = fields.Char(string="COD Available Alert")
    expected_delivery_date = fields.Boolean(string="Display Expected Delivery Date")
    start_day_after = fields.Integer('Start After (x) Days', default=2)
    cod_policy = fields.Text(string="Cash On Delivery Policy")
    cod_unavailable_message_on_product = fields.Text(string="COD Unavailable Message on Product")
    cod_unavailable_message_on_payment = fields.Text(string="COD Unavailable Message on Payment")
    is_cod_fee = fields.Boolean(string="Enable Fee")
    fee_name = fields.Char(string="Fee Name")
    fee_amount = fields.Float(string="Fee Amount")
    state = fields.Selection(
        selection=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
        ],
        string='Status',
        required=True,
        readonly=True,
        default='active',
    )
    