# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import float_compare


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    def _prepare_invoice_line(self, **optional_values):
        """
            add order_id.name 
        """
        picking=self.env['stock.picking'].search([('origin', '=', self.order_id.name), ('state', '=', 'done')])
        
        stock_move=self.env['stock.move']
        all_picking=""
        tab=[]

        print(len(picking))
        for i in picking:
            tab.append(i.id)

        # stock_move=self.env['stock.move'].search([('picking_id', 'in', tab),('product_id', '=', self.product_id.id)])
        
        
        # print(stock_move)

        if len(picking) > 1:
            for i in picking:
                stock_move=self.env['stock.move'].search([('picking_id', 'in', tab),('state', '=', 'done')])
                
                if stock_move:
                    tab.append(i.id)
                    if all_picking == "":
                        all_picking+=i.name
                    else:
                        all_picking+= ", " + i.name
        else:
            all_picking=picking.name
        
        
        
        values = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)

        stock_moves = self.get_stock_moves_link_invoice()
        # Invoice returned moves marked as to_refund
        if (
            float_compare(
                self.qty_to_invoice, 0.0, precision_rounding=self.currency_id.rounding
            )
            < 0
        ):
            stock_moves = stock_moves.filtered(
                lambda m: m.to_refund and not m.invoice_line_ids
            )
        values["move_line_ids"] = [(4, m.id) for m in stock_moves]

        values['order_customer']=self.order_id.sale_order_partner
        values['order_origin']=self.order_id.name
        values['diameter']=self.product_id.diameter
        values['hs_code']=self.product_id.hs_code.hs_code
        values['picking_name']=all_picking
        
        return values

    def get_stock_moves_link_invoice(self):
        skip_check_invoice_state = self.env.context.get(
            "skip_check_invoice_state", False
        )
        return self.mapped("move_ids").filtered(
            lambda mv: (
                mv.state == "done"
                and not (
                    not skip_check_invoice_state
                    and any(
                        inv.state != "cancel"
                        for inv in mv.invoice_line_ids.mapped("move_id")
                    )
                )
                and not mv.scrapped
                and (
                    mv.location_dest_id.usage == "customer"
                    or (mv.location_id.usage == "customer" and mv.to_refund)
                )
            )
        )

    # def _prepare_invoice_line(self, **optional_values):
    #     vals = super()._prepare_invoice_line(**optional_values)
    #     stock_moves = self.get_stock_moves_link_invoice()
    #     # Invoice returned moves marked as to_refund
    #     if (
    #         float_compare(
    #             self.qty_to_invoice, 0.0, precision_rounding=self.currency_id.rounding
    #         )
    #         < 0
    #     ):
    #         stock_moves = stock_moves.filtered(
    #             lambda m: m.to_refund and not m.invoice_line_ids
    #         )
    #     vals["move_line_ids"] = [(4, m.id) for m in stock_moves]
    #     return vals