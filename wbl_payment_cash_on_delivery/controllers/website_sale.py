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

from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from datetime import datetime
from datetime import timedelta


class WebsiteSaleInherit(WebsiteSale):

    def _get_shop_payment_values(self, order, **kwargs):
        response = super(WebsiteSaleInherit, self)._get_shop_payment_values(order, **kwargs)
        if response['providers_sudo']:
            counter = 0
            for provider in response['providers_sudo']:
                if provider.code == 'cash_on_delivery':
                    response['fee_data'] = provider.cod_applicable_rule
                    counter += 1
                    break
            if counter == 0:
                cod_provider = request.env['payment.provider'].sudo().search([('code', '=', 'cash_on_delivery')])
                response['message'] = cod_provider.cod_applicable_rule.cod_unavailable_message_on_payment
        return response

    def _prepare_product_values(self, product, category, search, **kwargs):
        response = super(WebsiteSaleInherit, self)._prepare_product_values(product, category, search, **kwargs)
        cod_provider = request.env['payment.provider'].sudo().search([('code', '=', 'cash_on_delivery')])
        cod_method = request.env['payment.method'].sudo().search([('code', '=', 'cash_on_delivery')])
        if cod_provider.state == 'enabled' and cod_provider.is_published and cod_method.active:
            if cod_provider.cod_applicable_rule:
                response['cod_config'] = cod_provider.cod_applicable_rule
                expected_date = datetime.now() + timedelta(days=cod_provider.cod_applicable_rule.start_day_after)
                response['expected_delivery_date'] = expected_date
                product_ids = list()
                for product_id in cod_provider.cod_applicable_rule.product_ids:
                    product_ids.append(product_id.product_tmpl_id)
                response['is_cod_available'] = True if product not in product_ids else False
        return response


