# -*- coding: utf-8 -*-
{
    "name": "tnx_payroll",
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
    "depends": ["base", "hr_contract", "hr_work_entry", "hr", "hr_payroll"],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        "views/views.xml",
        "views/templates.xml",
        "views/hr_contract_view.xml",
        "views/hr_payslip.xml",
        "views/hr_salary_rule.xml",
        "report/base_external_layout.xml",
        "report/payslip_report.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "license": "LGPL-3",
    "assets": {
        "web.report_assets_common": [
            "tnx_payroll/static/src/css/report_css.css",
        ],
    },
}
