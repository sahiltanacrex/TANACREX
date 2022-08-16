from odoo import _, fields, models, api
from odoo.exceptions import UserError
from math import ceil


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    carton_id = fields.Many2one(
        string="Carton",
        comodel_name="stock.carton",
    )
