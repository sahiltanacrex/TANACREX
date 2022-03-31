# -*- coding: utf-8 -*-

from termios import CINTR
from odoo import models, fields, api

class Hr_employee(models.Model):
    _inherit='hr.employee'
    cnaps = fields.Char('CNAPS')
    cin = fields.Char('CIN')
    matricule = fields.Char('Matricule')
    classification = fields.Selection([
        ('hc', 'HC'),
        ('op', 'OP'),
        ('etc', 'Etc'),
    ], string='Classification')