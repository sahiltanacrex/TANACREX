# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Sale_order(models.Model):
    _inherit = "sale.order"
    sale_order_partner = fields.Char("BC client")
    production_duration = fields.Integer("Indicatif de fabrication", required=True)
    delivery_time = fields.Integer("Indicatif de livraison", required=True)
    poids_en_kg = fields.Float(
        compute="_compute_poids_total", store=True, required=False
    )
    payment_method = fields.Selection([('bank_transfer', 'Bank Transfer'), ('check', 'Check'), ('cash', 'Cash')])
    validity_day = fields.Integer()

    @api.constrains('validity_day')
    def _validity_day_constrains(self):
        for rec in self:
            if rec.validity_day <= 0:
                raise ValidationError(_('Validity period must be greater than 0.'))

    @api.depends("order_line.poids_en_kg")
    def _compute_poids_total(self):
        for rec in self:
            res = 0
            for line in rec.order_line:
                res += line.poids_en_kg
            rec.poids_en_kg = res

    box_qty = fields.Float(
        compute="_compute_box_qty", store=True, required=False
    )

    @api.depends("order_line.box_qty")
    def _compute_box_qty(self):
        for rec in self:
            res = 0
            for line in rec.order_line:
                res += line.box_qty
            rec.box_qty = res
