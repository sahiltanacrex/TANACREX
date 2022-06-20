from odoo import _, fields, models
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    packaging_id = fields.Many2one(
        "product.packaging", related="move_id.product_packaging_id"
    )
