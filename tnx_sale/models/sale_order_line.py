# -*- coding: utf-8 -*-

from odoo import models, api, fields
import math


class Sale_order_line(models.Model):
    _inherit = "sale.order.line"
    development_expenses = fields.Monetary("Development costs")
    unit_qty = fields.Integer("Unitary quantity")
    product_uom_qty = fields.Float("Cond Quantity", digits=(14, 2))
    qty_delivered = fields.Float(digits=(14, 2))
    qty_invoiced = fields.Float(digits=(14, 2))
    box_qty = fields.Float("Nombre de carton", compute="_compute_box_qty")
    poids_en_kg = fields.Float(
        compute="_compute_poids_total", store=True, required=False
    )

    @api.depends("product_id", "product_id.weight", "qty_delivered")
    def _compute_poids_total(self):
        for rec in self:
            rec.poids_en_kg = rec.product_id.weight * rec.qty_delivered

    @api.depends('product_uom_qty', 'product_packaging_id')
    def _compute_box_qty(self):
        for rec in self:
            if rec.product_packaging_id.qty != 0:
                rec.box_qty = rec.product_uom_qty / rec.product_packaging_id.qty
            else:
                rec.box_qty = 0

    @api.depends("discount", "price_unit", "tax_id", "development_expenses", "unit_qty")
    def _compute_amount(self):
        for rec in self:
            for line in rec:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                if line.product_id.qty_min:
                    if line.product_id.qty_min > 0:
                        if line.unit_qty < line.product_id.qty_min:
                            price = line.product_id.minimum_price

                # new: substract development_expenses
                taxes = line.tax_id.compute_all(
                    price,
                    line.order_id.currency_id,
                    line.product_uom_qty,
                    product=line.product_id,
                    partner=line.order_id.partner_shipping_id,
                )
                line.update(
                    {
                        "price_tax": sum(
                            t.get("amount", 0.0) for t in taxes.get("taxes", [])
                        ),
                        "price_total": taxes["total_included"],
                        "price_subtotal": taxes["total_excluded"]
                                          + line.development_expenses,
                    }
                )
                if rec.env.context.get(
                        "import_file", False
                ) and not rec.env.user.user_has_groups("account.group_account_manager"):
                    line.tax_id.invalidate_cache(
                        ["invoice_repartition_line_ids"], [line.tax_id.id]
                    )
            if rec.unit_qty:
                if rec.unit_qty > 0:
                    rec.product_uom_qty = rec.unit_qty / rec.product_uom.ratio
            if rec.product_id.qty_min:
                if rec.product_id.qty_min > 0:
                    if rec.unit_qty < rec.product_id.qty_min:
                        rec.price_subtotal = (
                                rec.product_id.minimum_price + rec.development_expenses
                        )

    def _prepare_invoice_line(self, **optional_values):
        """
        add order_id.name
        """
        values = super(Sale_order_line, self)._prepare_invoice_line(**optional_values)

        values["development_expenses"] = self.development_expenses
        values["price_subtotal"] = self.development_expenses + self.price_subtotal
        values["unit_qty"] = self.unit_qty
        # values["move_line_ids"] = [(4, m.id) for m in stock_moves]

        return values

    def write(self, values):
        result = super(Sale_order_line, self).write(values)
        return result

    @api.onchange("unit_qty")
    def _onchange_price_unit(self):
        """test price units

        Returns:
            price_unit: if qty of the product in line is not enough than the quantity min in product,
            raise a pop up and put price_unit at zero

        """
        if self.unit_qty:
            if self.unit_qty > 0:
                self.product_uom_qty = self.unit_qty / self.product_uom.ratio

        if self.product_id.qty_min:
            if self.product_id.qty_min > 0:
                if self.unit_qty < self.product_id.qty_min:
                    self.price_subtotal = self.product_id.minimum_price
                    # !this return pop up
                    return {
                        "warning": {
                            "title": "Quantité minimum Non atteint!",
                            "message": f"Attention ! La quantité minimum pour ce produit {self.product_id.name} a pas été atteint. Merci de prévoir un forfait.",
                        }
                    }

    @api.onchange("product_uom_qty")
    def _onchangeqty_min_product_uom_qty(self):
        self.unit_qty = math.ceil(self.product_uom_qty * self.product_uom.ratio)
        if (
                self.product_id.qty_min
                and self.product_id
                and self.product_uom_qty
                and self.product_id.detailed_type == "product"
        ):
            if self.product_id.qty_min > 0:
                if self.unit_qty < self.product_id.qty_min:
                    self.price_subtotal = self.product_id.minimum_price


class Account_move_line(models.Model):
    _inherit = "account.move.line"
    development_expenses = fields.Monetary("Prix de developpement")
    unit_qty = fields.Float("Quantité unitaire", compute='_compute_qty_unit', store=True) #inverse='_inverse_compute_qty_unit'

    # price_subtotal = fields.Monetary(compute='_compute_price_subtotal')
    # @api.depends('development_expenses')
    # def _compute_price_subtotal(self):
    #     for val in self:
    #         if val.development_expenses > 0:
    #             val.update(val._get_price_total_and_subtotal())
    #             val.price_subtotal += val.development_expenses

    @api.depends('product_id','quantity')
    def _compute_qty_unit(self):
        for rec in self:
            rec.unit_qty = rec.quantity * rec.product_uom_id.factor_inv

    # def _inverse_compute_qty_unit(self):
    #     for rec in self:
    #         if rec.product_uom_id.factor_inv == 100:
    #             rec.quantity = rec.unit_qty / 100

    @api.model
    def _get_price_total_and_subtotal_model(
            self,
            price_unit,
            quantity,
            discount,
            currency,
            product,
            partner,
            taxes,
            move_type,
    ):
        vals = super(Account_move_line, self)._get_price_total_and_subtotal_model(
            price_unit, quantity, discount, currency, product, partner, taxes, move_type
        )

        vals["price_subtotal"] += self.development_expenses

        if self.product_id:
            product = self.product_id
            if product.qty_min > 0:
                if self.unit_qty < product.qty_min:
                    vals["price_subtotal"] = (
                            self.development_expenses + product.minimum_price
                    )
        return vals
