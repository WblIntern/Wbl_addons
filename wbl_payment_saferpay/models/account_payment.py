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


from odoo import models, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_open_refund_wizard(self):
        """Opens the WhatsApp message wizard to send a message to the customer."""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Refund'),
            'res_model': 'refund.amount.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_user_id': self.partner_id.id},
        }
