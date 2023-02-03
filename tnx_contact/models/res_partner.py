# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    nif = fields.Char(
        string='NIF',
        required=False)
    stat = fields.Char(
        string='STAT',
        required=False)
    rcs = fields.Char(
        string='RCS',
        required=False)

    cif = fields.Char('CIF')
    free_val = fields.Char(string='')

    partner_type = fields.Selection([
        ('ex', 'EX'),
        ('vl', 'VL'),
        ('ls', 'LS'),
    ], string='Type de client')

    fax_number = fields.Char(
        string='FAX',
        required=False)

    ref_client = fields.Char(string='ref')
    # partner_type = fields.Selection(selection_add=[
    #     ('ex','EX'),('vl','VL'),('ls','LS')
    # ])

    # partner_type = fields.Selection(
    #     string='Type de client',
    #     selection=[('ex','EX'),('vl','VL'),('ls','LS')])
