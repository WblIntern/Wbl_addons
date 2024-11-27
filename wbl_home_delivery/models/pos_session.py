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


class InheritPosSession(models.Model):
    _inherit = 'pos.session'

    def _pos_ui_models_to_load(self):
        response = super()._pos_ui_models_to_load()
        response.append("delivery.person")
        response.append("delivery.time.schedule")
        return response

    def _load_model(self, model_name):
        if model_name == 'pos.payment.method':
            return self.env['pos.payment.method'].search_read([], ['id', 'image', 'use_home_delivery', 'is_cash_count',
                                                                   'is_online_payment', 'name', 'sequence',
                                                                   'split_transactions', 'type',
                                                                   'use_payment_terminal'])

        if model_name == 'delivery.person':
            return self.env['delivery.person'].search_read([], ['name', 'user', 'is_publish', 'delivery_date',
                                                                'delivery_time_slot', 'start_day_after',
                                                                'time_interval', 'max_order_in_single_slot',
                                                                'time_schedule', 'order_preparation_time'])
        if model_name == 'delivery.time.schedule':
            return self.env['delivery.time.schedule'].search_read([], ['delivery_carrier_id', 'week_days',
                                                                       'open_time_hours', 'open_time_minutes',
                                                                       'close_time_hours', 'close_time_minutes'])

        return super()._load_model(model_name)
