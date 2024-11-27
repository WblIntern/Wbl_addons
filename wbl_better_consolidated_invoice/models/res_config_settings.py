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

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    better_consolidated_invoice = fields.Boolean(string="Better Consolidated Invoice", default=True)
    invoice_layout = fields.Selection(
        string="Layout",
        selection=[
            ('layout-1', "Layout 1"),
            ('layout-2', "Layout 2"),
            ('layout-3', "Layout 3"),
        ],
    )

    def set_values(self):
        response = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('website_sale.better_consolidated_invoice',
                                                         self.better_consolidated_invoice)
        self.env['ir.config_parameter'].sudo().set_param('website_sale.invoice_layout', self.invoice_layout)
        return response

    @api.model
    def get_values(self):
        response = super(ResConfigSettings, self).get_values()
        ir_config_parameter_sudo = self.env['ir.config_parameter'].sudo()
        response.update(
            better_consolidated_invoice=ir_config_parameter_sudo.get_param('website_sale.better_consolidated_invoice'),
            invoice_layout=ir_config_parameter_sudo.get_param('website_sale.invoice_layout'),
        )
        return response
