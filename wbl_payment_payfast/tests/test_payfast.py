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


from odoo.tests import tagged
from odoo.tools import mute_logger
from odoo.addons.payment.tests.http_common import PaymentHttpCommon
from odoo.addons.wbl_payment_payfast.tests.common import PayfastCommon


@tagged('post_install', '-at_install')
class payfastTest(PayfastCommon, PaymentHttpCommon):

    @mute_logger(
        'odoo.addons.wbl_payment_payfast.controllers.payfast',
        'odoo.addons.wbl_payment_payfast.models.payment_transaction',
    )
    def test_webhook_notification_confirms_transaction(self):
        """ Test the processing of a webhook notification. """
        tx = self._create_transaction('redirect')
        self.assertEqual(tx.state, 'done')
