from odoo import models, fields, api

class Bank(models.Model):
    _name="bank.company"
    _rec_name = "bank"
    _inherit = ['mail.thread']

    bank = fields.Char('Nom de la banque', track_visibility='onchange')
    bank_company_line_ids = fields.One2many('bank.company.line', 'bank_id', string='Numero de compte bancaire', track_visibility='onchange')
    account_move_id = fields.Many2one('account.move', string='Account move')


class Bank_line(models.Model):
    _name="bank.company.line"
    _inherit = ['mail.thread']
    _rec_name = "account_registration"

    
    account_registration = fields.Char('Numero de compte', track_visibility='onchange')
    res_currency_id = fields.Many2one('res.currency', string='Devise client', track_visibility='onchange')
    bank_id = fields.Many2one('bank.company', string='Banque')
    