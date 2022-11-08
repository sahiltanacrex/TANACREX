# -*- coding: utf-8 -*-
{
    "name": "tnx_stock",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "tnx_base",
        "stock",
        "product",
        "sale_stock",
        "tnx_sale"
    ],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "data/carton_sequence.xml",
        "views/wizard_colisage.xml",
        "views/stock_carton.xml",
        "views/stock_picking.xml",
        "report/report_label.xml",
        "report/hide_report_picking.xml",
        # "report/report_deliveryslip.xml",
        "report/product_product_templates.xml",
        "report/note_de_colisage.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "license": "LGPL-3",
}
