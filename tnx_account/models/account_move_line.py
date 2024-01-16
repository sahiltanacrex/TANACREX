# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Account_move_line(models.Model):
    _inherit = "account.move.line"

    order_origin = fields.Char("Demande de prix")
    order_customer = fields.Char("BC Client")
    diameter = fields.Float("Diameter")
    hs_code = fields.Char("Hs Code")
    picking_name = fields.Char(store=True, string="Bon de livraison")
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
    price_unit_udm = fields.Float("Prix/UDM")
    punit = fields.Float(compute='_compute_new_pu', digits=(10, 4))

    def _compute_new_pu(self):
        for line in self:
            if line.product_uom_id.ratio != 0:
                line.punit = line.price_unit / line.product_uom_id.ratio
            else:
                line.punit = 0


    @api.onchange("product_id","quantity")
    def compute_qty_unit(self):
        for rec in self:
            rec.unit_qty = rec.quantity * rec.product_uom_id.factor_inv


    # @api.model_create_multi
    # def create(self, vals_list):
    #     # OVERRIDE
    #     ACCOUNTING_FIELDS = ('debit', 'credit', 'amount_currency')
    #     BUSINESS_FIELDS = ('price_unit', 'quantity', 'discount', 'tax_ids')
    #
    #     for vals in vals_list:
    #         move = self.env['account.move'].browse(vals['move_id'])
    #         vals.setdefault('company_currency_id', move.company_id.currency_id.id) # important to bypass the ORM limitation where monetary fields are not rounded; more info in the commit message
    #
    #         # Ensure balance == amount_currency in case of missing currency or same currency as the one from the
    #         # company.
    #         currency_id = vals.get('currency_id') or move.company_id.currency_id.id
    #         if currency_id == move.company_id.currency_id.id:
    #             balance = vals.get('debit', 0.0) - vals.get('credit', 0.0)
    #             vals.update({
    #                 'currency_id': currency_id,
    #                 'amount_currency': balance,
    #             })
    #         else:
    #             vals['amount_currency'] = vals.get('amount_currency', 0.0)
    #
    #         if move.is_invoice(include_receipts=True):
    #             currency = move.currency_id
    #             partner = self.env['res.partner'].browse(vals.get('partner_id'))
    #             taxes = self.new({'tax_ids': vals.get('tax_ids', [])}).tax_ids
    #             tax_ids = set(taxes.ids)
    #             taxes = self.env['account.tax'].browse(tax_ids)
    #
    #             # Ensure consistency between accounting & business fields.
    #             # As we can't express such synchronization as computed fields without cycling, we need to do it both
    #             # in onchange and in create/write. So, if something changed in accounting [resp. business] fields,
    #             # business [resp. accounting] fields are recomputed.
    #             if any(vals.get(field) for field in ACCOUNTING_FIELDS):
    #                 price_subtotal = self._get_price_total_and_subtotal_model(
    #                     vals.get('price_unit', 0.0),
    #                     vals.get('quantity', 0.0),
    #                     vals.get('discount', 0.0),
    #                     currency,
    #                     self.env['product.product'].browse(vals.get('product_id')),
    #                     partner,
    #                     taxes,
    #                     move.move_type,
    #                 ).get('price_subtotal', 0.0)
    #                 vals.update(self._get_fields_onchange_balance_model(
    #                     vals.get('quantity', 0.0),
    #                     vals.get('discount', 0.0),
    #                     vals['amount_currency'],
    #                     move.move_type,
    #                     currency,
    #                     taxes,
    #                     price_subtotal
    #                 ))
    #                 vals.update(self._get_price_total_and_subtotal_model(
    #                     vals.get('price_unit', 0.0),
    #                     vals.get('quantity', 0.0),
    #                     vals.get('discount', 0.0),
    #                     currency,
    #                     self.env['product.product'].browse(vals.get('product_id')),
    #                     partner,
    #                     taxes,
    #                     move.move_type,
    #                 ))
    #             elif any(vals.get(field) for field in BUSINESS_FIELDS):
    #                 vals.update(self._get_price_total_and_subtotal_model(
    #                     vals.get('price_unit', 0.0),
    #                     vals.get('quantity', 0.0),
    #                     vals.get('discount', 0.0),
    #                     currency,
    #                     self.env['product.product'].browse(vals.get('product_id')),
    #                     partner,
    #                     taxes,
    #                     move.move_type,
    #                 ))
    #                 vals.update(self._get_fields_onchange_subtotal_model(
    #                     vals['price_subtotal'],
    #                     move.move_type,
    #                     currency,
    #                     move.company_id,
    #                     move.date,
    #                 ))
    #         if vals.get("quantity") is not None:
    #             vals['unit_qty'] = vals.get('quantity') * 100
    #
    #     lines = super(Account_move_line, self).create(vals_list)
    #
    #     moves = lines.mapped('move_id')
    #     if self._context.get('check_move_validity', True):
    #         moves._check_balanced()
    #     moves.filtered(lambda m: m.state == 'posted')._check_fiscalyear_lock_date()
    #     lines.filtered(lambda l: l.parent_state == 'posted')._check_tax_lock_date()
    #     moves._synchronize_business_models({'line_ids'})
    #
    #     return lines

    # def write(self, vals):
    #     if vals.get("quantity") is not None:
    #         vals['unit_qty'] = vals.get('quantity') * 100
    #     return super().write(vals)