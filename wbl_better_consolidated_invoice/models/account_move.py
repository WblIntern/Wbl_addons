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

from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_consolidated_invoice_order(self):
        return self.line_ids.sale_line_ids.order_id

    def _get_better_consolidated_invoice(self):
        return self.env['ir.config_parameter'].sudo().get_param('website_sale.better_consolidated_invoice')

    def _get_layout_option(self):
        return self.env['ir.config_parameter'].sudo().get_param('website_sale.invoice_layout')
