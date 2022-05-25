# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError, Warning

class Sale_order_line(models.Model):
    _inherit='sale.order.line'

    development_expenses = fields.Monetary('Frais de développement')

    # unit_qty = fields.Float('Quantité unitaire')
    product_uom_qty = fields.Float('Quantité cond.')    


    @api.depends('product_uom_qty', 'discount', 'price_unit',
                 'tax_id', 'development_expenses')
    def _compute_amount(self):
        """
        tsy override tsony fa tonga dia notsindrina tanteraka sinon tsy miainga

        Compute the amounts of the SO line.

        Fully overridden to add field development_expenses to the
        formula and triggers.
        """
        if self.product_uom_qty > self.product_id.qty_min:
            self.price_unit= self.product_id.list_price

        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            
            # new: substract development_expenses
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'] + line.development_expenses,
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])

    @api.onchange('product_it')
    def _onchange_product_it(self):
        if self.product_id.qty_min > 0:
            self.price_unit=0

    @api.onchange('price_unit')
    def _onchange_price_unit(self):
        """test price units

        Returns:
            price_unit: if qty of the product in line is not enough than the quantity min in product, 
            raise a pop up and put price_unit at zero

        """
        if self.product_uom_qty <= self.product_id.qty_min:
            self.price_unit=0
            #! this return pop up
            return {

                    'warning': {

                        'title': 'Quantité minimum Non atteint!',

                        'message': f'Attention ! La quantité minimum pour ce produit {self.product_id.name} n\'a pas été atteint. Merci de prévoir un forfait.'}

                }
        else:
            pass
        

    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
    
        if self.product_id and self.product_uom_qty and self.product_id.detailed_type == 'product' :
            if self.product_uom_qty <= self.product_id.qty_min:
                return {

                    'warning': {

                        'title': 'Quantité minimum Non atteint!',

                        'message': f'Attention ! La quantité minimum pour ce produit {self.product_id.name} n\'a pas été atteint. Merci de prévoir un forfait.'}

                }
            else:
                pass
        else: 
            pass



