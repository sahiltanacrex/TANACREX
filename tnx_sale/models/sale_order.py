# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

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
    have_develop_fees = fields.Boolean(compute="_compute_have_develop_fees")

    @api.depends('order_line', 'order_line.development_expenses')
    def _compute_have_develop_fees(self):
        list_price = self.order_line.mapped('development_expenses')
        self.have_develop_fees = any(isinstance(element, (float, int)) and element > 0 for element in list_price)

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

    def get_all_type(self, val):
        product_type = val.mapped('product_id').mapped('product_type')
        list_type = list(set(product_type))
        try:
            list_type.index(False)
            list_type.remove(False)
        except ValueError:
            pass
        list_type.sort()
        return list_type

    def get_total_price_type(self, val, type):
        sub_total_price = 0
        for el in val:
            if el.product_id.product_type == type:
                sub_total_price += el.price_subtotal
        return sub_total_price
    
    def total_amount_ex(self, freight, amount_total):
        return freight + amount_total

    def get_bank_ids(self):
        currency = self.currency_id
        bank_company_line_ids = self.env['bank.company.line'].search([('res_currency_id', '=', currency.id)])
        if bank_company_line_ids:
            return bank_company_line_ids.mapped('bank_id')
        return False

    def get_right_number(self, val):
        val_string = str(val)
        val_split = val_string.split('.')
        if len(val_split) == 1:
            return '{:,}'.format(int(val)).replace(',', ' ')
        if int(val_split[1]) > 0:
            return '{:,}'.format(val).replace(',', ' ')
        else:
            return '{:,}'.format(int(val)).replace(',', ' ')
    
    def format_number_for_amount(self, num):
        formatted = "{:,.2f}".format(num).replace(",", " ")
        return formatted
    
    def amount_ttc_ls(self, val):
        return val * 1.2

    def get_validity_date(self):
        return self.date_order.date() + timedelta(days=self.validity_day)
    
    def get_production_date(self):
        return self.date_order.date() + timedelta(days=self.production_duration)
    
    def get_delivery_date(self):
        return self.date_order.date() + timedelta(days=self.delivery_time)
    