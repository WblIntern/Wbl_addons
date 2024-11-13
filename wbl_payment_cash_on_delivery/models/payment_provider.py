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
from datetime import datetime


class PaymentProvider(models.Model):
    _inherit = "payment.provider"
    _description = 'Payment Provider'

    code = fields.Selection(
        selection_add=[('cash_on_delivery', "Cash on Delivery")], ondelete={'cash_on_delivery': 'set default'}
    )
    product_id = fields.Many2one(comodel_name='product.product', string='Fee Service Product')
    cod_applicable_rule = fields.Many2one(comodel_name='cod.settings.rule', string='Configure COD Rule')
    # qr_code = fields.Boolean(
    #     string="Enable QR Codes", help="Enable the use of QR-codes when paying by Cash On Delivery.")

    @api.model
    def _get_compatible_providers(
            self,
            company_id,
            partner_id,
            amount,
            currency_id=None,
            force_tokenization=False,
            is_express_checkout=False,
            is_validation=False,
            sale_order_id=None,
            **kwargs
    ):
        providers = super()._get_compatible_providers(
            company_id,
            partner_id,
            amount,
            currency_id=currency_id,
            force_tokenization=force_tokenization,
            is_express_checkout=is_express_checkout,
            is_validation=is_validation,
            sale_order_id=sale_order_id,
            **kwargs
        )
        order = self.env['sale.order'].browse(sale_order_id).exists()
        partner = self.env['res.partner'].browse(partner_id)
        providers = providers.filtered(
            lambda
                provider: order.amount_total >= provider.cod_applicable_rule.min_order_amount if provider.cod_applicable_rule.min_order_amount else True
        )
        providers = providers.filtered(
            lambda
                provider: order.amount_total <= provider.cod_applicable_rule.max_order_amount if provider.cod_applicable_rule.min_order_amount else True
        )
        providers = providers.filtered(
            lambda provider: partner not in provider.cod_applicable_rule.partner_ids
        )
        now = datetime.now().strftime("%Y-%m-%d")
        providers = providers.filtered(
            lambda provider: now >= provider.cod_applicable_rule.date_begin.strftime(
                "%Y-%m-%d") if provider.cod_applicable_rule.date_begin else True
        )
        providers = providers.filtered(
            lambda provider: now <= provider.cod_applicable_rule.date_end.strftime(
                "%Y-%m-%d") if provider.cod_applicable_rule.date_end else True
        )
        providers = providers.filtered(
            lambda provider: self.cod_country_availability(provider, order.partner_shipping_id.country_id)
        )
        providers = providers.filtered(
            lambda provider: self.cod_state_availability(provider, order.partner_shipping_id.state_id)
        )
        providers = providers.filtered(
            lambda provider: self.cod_city_availability(provider, order.partner_shipping_id.city)
        )
        providers = providers.filtered(
            lambda provider: self.cod_zip_availability(provider, order.partner_shipping_id.zip)
        )
        for line in order.order_line:
            providers = providers.filtered(
                lambda provider: line.product_id not in provider.cod_applicable_rule.product_ids
            )
        return providers

    def cod_country_availability(self, provider, country_id):
        if provider.cod_applicable_rule and provider.cod_applicable_rule.country_region:
            available_countries = []
            for location in provider.cod_applicable_rule.country_region:
                if location.country_id:
                    available_countries.append(location.country_id)
            if available_countries:
                return country_id in available_countries
        return True

    def cod_state_availability(self, provider, state_id):
        if provider.cod_applicable_rule and provider.cod_applicable_rule.country_region:
            available_states = []
            for location in provider.cod_applicable_rule.country_region:
                if location.state_id:
                    available_states.append(location.state_id)
            if available_states:
                return state_id in available_states
        return True

    def cod_city_availability(self, provider, city):
        if provider.cod_applicable_rule and provider.cod_applicable_rule.country_region:
            available_cities = []
            for location in provider.cod_applicable_rule.country_region:
                if location.city:
                    available_cities.append(location.city)
            if available_cities:
                return city in available_cities
        return True

    def cod_zip_availability(self, provider, zip_code):
        if provider.cod_applicable_rule and provider.cod_applicable_rule.country_region:
            available_zips = []
            for location in provider.cod_applicable_rule.country_region:
                if location.zip:
                    available_zips.append(location.zip)
            if available_zips:
                return zip_code in available_zips
        return True
