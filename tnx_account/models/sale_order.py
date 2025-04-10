# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Sale_order(models.Model):
    _inherit = "sale.order"

    bank_company_ids = fields.Many2many(
        "bank.company", "sale_order_id", string="Bank"
    )

    # def _create_invoices(self, grouped=False, final=False, date=None):
    #     for order in self:
    #         get_currency = order.pricelist_id.currency_id
    #         order._cr.execute(
    #             f"""
    #             SELECT bank_id
    #             FROM bank_company_line
    #             WHERE res_currency_id ={get_currency.id}
    #         """,
    #             [list(order.ids)],
    #         )
    #         ids = order._cr.fetchall()
    #         moves = super()._create_invoices(grouped=grouped, final=final, date=date)
    #         for id in ids:
    #             moves.write({"bank_company_ids": [(4, id)]})
    #         return moves

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoices = super()._create_invoices(grouped=grouped, final=final, date=date)

        sale_order_map = {order.id: order.bank_company_ids.ids for order in self}

        for invoice in invoices:
            order_id = invoice.origin_sale_id.id
            if order_id in sale_order_map:
                invoice.bank_company_ids = [(6, 0, sale_order_map[order_id])]

        return invoices
