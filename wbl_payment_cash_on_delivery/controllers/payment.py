from odoo.addons.website_sale.controllers.payment import PaymentPortal
from odoo import http
from odoo.http import request, route


class PaymentPortalInherit(PaymentPortal):

    @route('/shop/payment/transaction/<int:order_id>', type='json', auth='public', website=True)
    def shop_payment_transaction(self, order_id, access_token, **kwargs):
        order_sudo = self._document_check_access('sale.order', order_id, access_token)
        for line in order_sudo.order_line:
            if line.is_cod_fee:
                kwargs['amount'] = order_sudo.amount_total
        response = super(PaymentPortalInherit, self).shop_payment_transaction(order_id, access_token, **kwargs)
        return response
