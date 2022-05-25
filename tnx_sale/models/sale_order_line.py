# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError, Warning

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

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.product_uom_qty=0
        print('----------')
        print(self.product_id.detailed_type)
        # if self.product_id.detailed_type == 'product':
        

    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
    
        if self.product_id and self.product_uom_qty and self.product_id.detailed_type == 'product' :
            if self.product_uom_qty <= self.product_id.qty_min:
                if self.product_uom_qty <= self.product_id.qty_min:
                    self.product_uom_qty=0
                    return {

                        'warning': {

                            'title': 'Quantité minimum Non atteint!',

                            'message': f'Attention ! La quantité minimum pour ce produit {self.product_id.name} n\'a pas été atteint. Merci de prévoir un forfait.'}

                    }
        else: 
            pass



