#coding: utf-8

from odoo.tools import is_html_empty
from odoo import models, fields, api

from markupsafe import Markup


class ResCompany(models.Model):
    _inherit = "res.company"

    company_details_with_nif_stat = fields.Html(
        compute="compute_company_details_with_nif", store=False
    )

    @api.depends("company_details", "nif", "stat")
    def compute_company_details_with_nif(self):
        for company in self:
            if not is_html_empty(company.company_details):
                company_details = str(company.company_details).replace("</p>", "")
                company.company_details_with_nif_stat = Markup(
                    f"{company_details}<br/>NIF: {company.nif}<br/>STAT: {company.stat}</p>"
                )
            else:
                company.company_details_with_nif_stat = Markup(
                    f"<p>{company_details}<br/>NIF: {company.nif}<br/>STAT: {company.stat}</p>"
                )
