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

from odoo import http, _
from odoo.http import request


class CashPayment(http.Controller):

    @http.route('/shop/cash_payment', type='json', auth='public', website=True)
    def cash_payment(self, provider_id=None):
        if provider_id:
            payment_provider = request.env['payment.provider'].browse(provider_id)
            order = request.website.sale_get_order(force_create=True)
            monetary = request.env['ir.qweb.field.monetary']
            currency = order.currency_id
            if order and payment_provider.code == 'cash_on_delivery' and payment_provider.cod_applicable_rule.is_cod_fee:
                order._remove_cod_fee_line()
                fee_amount = payment_provider.cod_applicable_rule.fee_amount
                order._create_cod_fee_line(payment_provider, fee_amount)
                return {
                    'is_cod_fee': True,
                    'new_amount_tax': monetary.value_to_html(order.amount_tax, {'display_currency': currency}),
                    'new_amount_total': monetary.value_to_html(order.amount_total, {'display_currency': currency}),
                }
            else:
                order._remove_cod_fee_line()
                return {
                    'is_cod_fee': False,
                    'new_amount_tax': monetary.value_to_html(order.amount_tax, {'display_currency': currency}),
                    'new_amount_total': monetary.value_to_html(order.amount_total, {'display_currency': currency}),
                }
        return {}
