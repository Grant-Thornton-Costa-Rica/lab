# -*- coding: utf-8 -*-
{
    'name': "base_factura_electronica_v14",

    'summary': """
        Módulo de factura electrónica Costa Rica(v4.3) para odoo v14""",

    'description': """
         Módulo de factura electrónica Costa Rica(v4.3) para odoo v14
    """,

    'author': "Grant Thornton",
    'website': "https://www.grantthornton.cr/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'account', 'l10n_cr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/payment_method_views.xml',
    ],

    'external_dependencies': {
        "python": [
            'zeep',
        ],
    }
}