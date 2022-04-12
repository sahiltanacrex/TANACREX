# -*- coding: utf-8 -*-

from odoo import models, fields, api



class Sequences_ex(models.Model):
    _name="tnx.ex"

    name = fields.Integer('Séquences ex')
    sequences_year = fields.Integer('field_name')
    rel_invoice_id = fields.Integer('Rel invoice id')
    rel_state_invoice = fields.Char('Rel STate Invoice')

    
class Sequences_vl(models.Model):
    _name="tnx.vl"

    name = fields.Integer('Séquences vl')
    sequences_year = fields.Integer('field_name')
    rel_invoice_id = fields.Integer('Rel invoice id')
    rel_state_invoice = fields.Char('Rel STate Invoice')

class Sequences_ls(models.Model):
    _name="tnx.ls"

    name = fields.Integer('Séquences ls')
    sequences_year = fields.Integer('field_name')
    rel_invoice_id = fields.Integer('Rel invoice id')
    rel_state_invoice = fields.Char('Rel STate Invoice')