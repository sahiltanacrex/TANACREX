# -*- coding: utf-8 -*-

from odoo import fields, models


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    partner_production_id = fields.Many2one(related="production_id.partner_id")
    product_qty_production_id = fields.Float(related="production_id.product_qty")
    
