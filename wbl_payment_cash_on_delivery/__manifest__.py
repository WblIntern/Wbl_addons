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

{
    'name': 'Cash on Delivery - Enable COD Payment',
    'version': '18.0.1.0.0',
    'summary': """Give your customers to pay via Cash on Delivery payment method.""",
    'description': """Give your customers to pay via Cash on Delivery payment method.""",
    'category': 'eCommerce',
    'author': 'Weblytic Labs',
    'company': 'Weblytic Labs',
    'website': "https://store.weblyticlabs.com",
    'price': '31.00',
	'currency': 'USD',
    'depends': ['base', 'mail', 'website', 'delivery', 'website_payment', 'website_sale', 'payment', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/payment_cod_templates.xml',
        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
        'data/account_data.xml',
        'views/payment_provider_views.xml',
        'views/cod_settings_rule_views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'wbl_payment_cash_on_delivery/static/src/js/payment_form.js',
            'wbl_payment_cash_on_delivery/static/src/js/post_processing.js',
        ],
    },
    'images': ['static/description/banner.gif'],
    'live_test_url': 'https://youtu.be/7r3WwwViYMk',
    'license': 'OPL-1',
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'installable': True,
    'auto_install': False,
    'application': True,
}
