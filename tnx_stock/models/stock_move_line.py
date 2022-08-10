from odoo import _, fields, models, api
from odoo.exceptions import UserError
from math import ceil


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.onchange("picking_id.move_line_ids_without_package.carton_id")
    def _get_carton_id_domain(self):
        # res = []
        # print("demo")
        # if self.picking_id:
        #     for rec in self.picking_id.move_line_ids_without_package:
        #         if rec.carton_id:
        #             res.append(rec.carton_id.id)
        # res = list(set(res))
        return [("id", "in", [])]

    carton_id = fields.Many2one(
        string="Carton",
        comodel_name="stock.carton",
        domain=lambda self: self._get_carton_id_domain(),
    )
