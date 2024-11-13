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

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _action_confirm(self):
        tx = self.sudo().transaction_ids._get_last()
        if tx.provider_id.code == "cash_on_delivery":
            self.payment_term_id = self.env.ref('wbl_payment_cash_on_delivery.account_payment_term_cash_on_delivery').id
        res = super()._action_confirm()

    def _remove_cod_fee_line(self):
        """Remove delivery products from the sales orders"""
        cod_fee_lines = self.order_line.filtered("is_cod_fee")
        if not cod_fee_lines:
            return
        to_delete = cod_fee_lines.filtered(lambda x: x.qty_invoiced == 0)
        if not to_delete:
            raise UserError(
                _('You can not update the cod fee costs on an order where it was already invoiced!\n\nThe following delivery lines (product, invoiced quantity and price) have already been processed:\n\n')
                + '\n'.join(['- %s: %s x %s' % (line.product_id.with_context(display_default_code=False).display_name, line.qty_invoiced, line.price_unit) for line in cod_fee_lines])
            )
        to_delete.unlink()

    def set_cod_fee_line(self, payment_provider, amount):
        self._remove_cod_fee_line()
        for order in self:
            order._create_cod_fee_line(payment_provider, amount)
        return True

    def _prepare_cod_fee_line_vals(self, payment_provider, price_unit):
        context = {}
        if self.partner_id:
            # set delivery detail in the customer language
            context['lang'] = self.partner_id.lang
            carrier = payment_provider.with_context(lang=self.partner_id.lang)
        product_id = self.env['product.product'].browse(payment_provider.product_id.id)
        # Apply fiscal position
        taxes = product_id.taxes_id.filtered(lambda t: t.company_id.id == self.company_id.id)
        taxes_ids = taxes.ids
        if self.partner_id and self.fiscal_position_id:
            taxes_ids = self.fiscal_position_id.map_tax(taxes).ids

        # Create the sales order line

        if product_id.description_sale:
            so_description = '%s: %s' % (payment_provider.name, product_id.description_sale)
        else:
            so_description = payment_provider.name
        values = {
            'order_id': self.id,
            'name': so_description,
            'price_unit': price_unit,
            'product_uom_qty': 1,
            'product_uom': product_id.uom_id.id,
            'product_id': product_id.id,
            'tax_id': [(6, 0, taxes_ids)],
            'is_cod_fee': True,
        }
        return values

    def _create_cod_fee_line(self, payment_provider, price_unit):
        values = self._prepare_cod_fee_line_vals(payment_provider, price_unit)
        return self.env['sale.order.line'].sudo().create(values)
