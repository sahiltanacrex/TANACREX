# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Sale_order(models.Model):
    _inherit = "sale.order"

    def _create_invoices(self, grouped=False, final=False, date=None):
        for order in self:
            get_currency = order.pricelist_id.currency_id
            order._cr.execute(
                f"""
                SELECT bank_id
                FROM bank_company_line
                WHERE res_currency_id ={get_currency.id}
            """,
                [list(order.ids)],
            )
            ids = order._cr.fetchall()
            moves = super()._create_invoices(grouped=grouped, final=final, date=date)
            for id in ids:
                moves.write({"bank_company_ids": [(4, id)]})
            return moves
