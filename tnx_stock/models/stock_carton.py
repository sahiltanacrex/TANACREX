from odoo import _, fields, models, api


class StockCarton(models.Model):
    _name = "stock.carton"

    name = fields.Char("Nom")
