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

import logging
import pprint

from odoo.http import Controller, request, route

_logger = logging.getLogger(__name__)


class CashOnDeliveryController(Controller):
    _process_url = '/payment/cod/process'

    @route(_process_url, type='http', auth='public', methods=['POST'], csrf=False)
    def cod_process_transaction(self, **post):
        _logger.info("Handling cash on delivery processing with data:\n%s", pprint.pformat(post))
        request.env['payment.transaction'].sudo()._handle_notification_data('cash_on_delivery', post)
        return request.redirect('/payment/status')
