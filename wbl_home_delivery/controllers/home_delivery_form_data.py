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
from odoo import http
from odoo.http import request


class HomeDeliveryFormData(http.Controller):
    @http.route(['/home/delivery'], type='json', auth="public", website=True)
    def home_delivery_form_data(self, **post):
        delivery_person_id = post.get('delivery_person_id'),
        delivery_person_id = int(delivery_person_id[0])
        form_data = {
            'delivery_name': post.get('delivery_name'),
            'delivery_mobile': post.get('delivery_mobile'),
            'delivery_email': post.get('delivery_email'),
            'delivery_locality': post.get('delivery_locality'),
            'delivery_street': post.get('delivery_street'),
            'delivery_city': post.get('delivery_city'),
            'delivery_zip': post.get('delivery_zip'),
            'cashier': post.get('cashier'),
            'delivery_note': post.get('delivery_note'),
            'delivery_time': post.get('delivery_date'),
            'order_date': post.get('order_date'),
            "is_home_delivery": True,
            "order_note": post.get('delivery_note'),
            "delivery_instruction": post.get('delivery_instruction_note'),
            "data_to_change": True,
            "delivery_person_id": delivery_person_id,
            "home_delivery_time": post.get('home_delivery_time'),
            "home_delivery_date" : post.get('home_delivery_date'),

        }
        new_address_created = post.get('new_address')
        home_delivery_data = request.env['home.delivery'].create(form_data)
        new_address = {
            'name': post.get('delivery_name'),
            'phone': post.get('delivery_mobile'),
            'email': post.get('delivery_email'),
            'street': post.get('delivery_street'),
            'city': post.get('delivery_city'),
            'zip': post.get('delivery_zip'),
            'parent_id': post.get('selected_customer_partner_id'),
        }
        if new_address_created == "True":
            res_partner = request.env['res.partner'].create(new_address)
            for rec in res_partner:
                if rec:
                    rec.write({
                        "street": post.get('delivery_street') + " ",
                        'city': post.get('delivery_city') + " ",
                        'zip': post.get('delivery_zip'),
                    })
        return True
