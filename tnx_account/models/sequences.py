# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SequencesEx(models.Model):
    _name = "tnx.ex"

    name = fields.Integer("Sequence ex")
    sequences_year = fields.Integer("Sequence year")
    rel_invoice_id = fields.Integer("Rel invoice id")
    rel_state_invoice = fields.Char("Rel state invoice")


class SequencesVl(models.Model):
    _name = "tnx.vl"

    name = fields.Integer("Sequence vl")
    sequences_year = fields.Integer("Sequence year")
    rel_invoice_id = fields.Integer("Rel invoice id")
    rel_state_invoice = fields.Char("Rel state invoice")


class SequencesLs(models.Model):
    _name = "tnx.ls"

    name = fields.Integer("Séquence LS ")
    sequences_year = fields.Integer("Sequence année")
    rel_invoice_id = fields.Integer("Rel invoice id")
    rel_state_invoice = fields.Char("Rel state invoice")
