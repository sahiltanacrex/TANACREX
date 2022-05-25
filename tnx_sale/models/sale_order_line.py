# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Sale_order_line(models.Model):
    _inherit='sale.order.line'

    development_expenses = fields.Float('Frais de développement')

    @api.onchange('development_expenses')
    def _onchange_development_expenses(self):
        price_subtotal=0
        if self.development_expenses:
            price_subtotal+=self.price_subtotal+self.development_expenses
            self.update({
                'price_subtotal': price_subtotal,
            })

    