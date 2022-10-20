# -*- coding: utf-8 -*-
{
    'name': "tnx_account",

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
    'depends': ['base','tnx_base','tnx_product','tnx_sale', 'tnx_contact','account','sale','stock','sale_stock','mail'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
        # 'views/account_move.xml',
        # "views/stock_view.xml",
        # "views/account_invoice_view.xml",
        # "views/bank_company.xml",
        # "views/bank_company_line.xml",
        # "views/config_seq_ex.xml",
        # "views/config_seq_ls.xml",
        # "views/config_seq_vl.xml",
        'security/ir.model.access.csv',
        # reporting
        'report/report_invoice_ex.xml',
        'report/report_invoice_vl.xml',
        'report/report_invoice_ls.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],'license': 'LGPL-3',
}
