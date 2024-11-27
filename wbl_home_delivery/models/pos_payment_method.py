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


class InheritPosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    use_home_delivery = fields.Boolean(string="Use as Home Delivery", default=False)
