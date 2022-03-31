# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Res_partner(models.Model):
    _inherit="res.partner"

    nif = fields.Char(
        string='NIF',
        required=False)
    stat = fields.Char(
        string='STAT',
        required=False)
    rcs = fields.Char(
        string='RCS',
        required=False)

    partner_type = fields.Selection([
        ('ex', 'EX'),
        ('vl', 'VL'),
        ('ls', 'LS'),
    ], string='Type de client')

    # partner_type = fields.Selection(selection_add=[
    #     ('ex','EX'),('vl','VL'),('ls','LS')
    # ])
    
    # partner_type = fields.Selection(
    #     string='Type de client',
    #     selection=[('ex','EX'),('vl','VL'),('ls','LS')])

    res_currency_id = fields.Many2one('res.currency', string='Devise client')