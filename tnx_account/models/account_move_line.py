# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Account_move_line(models.Model):
    _inherit="account.move.line"
    
    order_origin = fields.Char('Bon de commande')
    diameter = fields.Float('Diamètre')
    hs_code = fields.Char('Hs Code')
    # picking_name = fields.Char('Bon de livraison')
    

    picking_name = fields.Char( store=True,string='Bon de livraison')

    # picking_name = fields.One2many('stock.picking', 'account_move_line_id', string='Stock Picking')

    
    move_line_ids = fields.Many2many(
        comodel_name="stock.move",
        relation="stock_move_invoice_line_rel",
        column1="invoice_line_id",
        column2="move_id",
        string="Related Stock Moves",
        readonly=True,
        help="Related stock moves "
        "(only when the invoice has been generated from a sale order).",
    )
