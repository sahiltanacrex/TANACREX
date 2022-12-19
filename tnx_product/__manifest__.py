# -*- coding: utf-8 -*-
{
    'name': "tnx_product",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'tnx_base', 'stock', 'product', 'mail', 'uom', 'sale'],

    # always loaded
    'data': [
        'views/product_format.xml',
        'views/product_template.xml',
        'views/templates.xml',
        'views/hscode_product.xml',
        'views/product_template_views.xml',
        'security/ir.model.access.csv',
        # send mail
        'data/mail_templates/template_bat.xml',
        'data/uom_data/uom_data.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ], 'license': 'LGPL-3',
}
