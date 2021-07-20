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
        'data/identification_type_data.xml',
        'data/sale_condition_data.xml',
        'data/payment_method_data.xml',
        'data/tax_code_data.xml',
        'data/tax_rate_data.xml',
        'data/document_type_data.xml',
        'data/product_code_type_data.xml',
        'data/reference_document_data.xml',
        'data/reference_code_data.xml',
        'data/exoneration_document_data.xml',
        'data/res.country.state.csv',
        'data/res.country.canton.csv',
        'data/res.country.district.csv',
        'data/res.country.neighborhood.csv',
        'views/res_company_views.xml',
        'views/activity_code_views.xml',
        'views/sale_condition_views.xml',
        'views/payment_method_views.xml',
        'views/identification_type_views.xml',
        'views/document_type_views.xml',
        'views/res_country_canton_views.xml',
        'views/res_country_district_views.xml',
        'views/res_country_neighborhood_views.xml',
        'views/product_code_type_views.xml',
        'views/reference_document_views.xml',
        'views/reference_code_views.xml',
        'views/exoneration_document_views.xml',
        'views/menu_views.xml',
        'security/ir.model.access.csv',
    ],

    'external_dependencies': {
        "python": [
            'zeep',
        ],
    }
}