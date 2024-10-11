# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    @api.onchange("line_ids")
    def _dependent_payment_ref(self):
        for ref in self.line_ids:
            if ref:
                invoice = self.env['account.move'].search([('name','=', ref.payment_ref)])
                ref.amount = invoice.amount_total
            else:
                ref.amount = 0.0
