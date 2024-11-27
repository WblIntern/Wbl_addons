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
    'name': 'Better Consolidated Invoice - Organised Invoicing',
    'version': '17.0.1.0.0',
    'summary': """Merge multiple invoice - Consolidated Invoice - Multiple bills - Multiple invoicing - Better Invoice - Organised Consolidated Billing.""",
    'description': """Merge multiple invoice - Consolidated Invoice - Multiple bills - Multiple invoicing - Better Invoice - Organised Consolidated Billing.""",
    'category': 'Accounting',
    'author': 'Weblytic Labs',
    'company': 'Weblytic Labs',
    'website': "https://store.weblyticlabs.com",
    'depends': ['base', 'mail', 'account', 'sale_management', 'sale', 'l10n_de'],
    'price': '35.00',
    'currency': 'USD',
    'data': [
        'views/res_config_settings_views.xml',
        'views/report_invoice.xml',
    ],
    'images': ['static/description/banner.gif'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
}
