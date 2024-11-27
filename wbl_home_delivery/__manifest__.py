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
    'name': 'POS Home Delivery',
    'version': '17.0.1.0.0',
    'sequence': 8,
    'summary': """ POS shipping Home Delivery POS Point-of-sale Home Delivery Method for Extra fee on home delivery for POS Home dispatch In-store to home delivery Retail POS delivery POS-to-home logistics Transparent delivery fees Delivery from store POS. """,
    'description': """ POS shipping Home Delivery POS Point-of-sale Home Delivery Method for Extra fee on home delivery for POS Home dispatch In-store to home delivery Retail POS delivery POS-to-home logistics Transparent delivery fees Delivery from store POS. """,
    'category': 'eCommerce',
    'author': 'Weblytic Labs',
    'company': 'Weblytic Labs',
    'website': "https://store.weblyticlabs.com",
    'depends': ['point_of_sale', 'web', 'account'],
    'images': ['static/description/banner.gif'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
    'data': [
        'data/ir_sequence_data.xml',
        'data/mail_template_data.xml',
        'security/ir.model.access.csv',
        'views/home_delivery_views.xml',
        'views/delivery_person_views.xml',
        'views/pos_order_views.xml',
        'views/pos_payment_method_views.xml',
        'views/account_move_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'wbl_home_delivery/static/src/xml/home_delivery_button.xml',
            'wbl_home_delivery/static/src/js/home_delivery_button.js',
            'wbl_home_delivery/static/src/xml/home_delivery_button_popup.xml',
            'wbl_home_delivery/static/src/js/home_delivery_button_popup.js',
            'wbl_home_delivery/static/src/js/pos_store.js',
            'wbl_home_delivery/static/src/xml/order_receipt.xml',
            'wbl_home_delivery/static/src/js/payment_screen.js',
        ],
    },
}
