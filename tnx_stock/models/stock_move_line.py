from odoo import _, fields, models, api
from odoo.exceptions import UserError
from math import ceil


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    packaging_id = fields.Many2one(
        "product.packaging", related="move_id.product_packaging_id"
    )

    packaging_qty = fields.Integer()

    @api.onchange("qty_done")
    def onchange_done(self):
        print(
            """
            >>>
            >>><<"""
        )
        res = ceil(self.qty_done / self.packaging_id.qty)
        self.sudo().write({"packaging_qty": res})
