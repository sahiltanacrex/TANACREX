from odoo import _, fields, models, api
from odoo.exceptions import UserError
from math import ceil


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"
    colisage = fields.Text(
        string="Colisage",
        required=False)

    carton_id = fields.Many2one(
        string="Carton",
        comodel_name="stock.carton",
    )
    unit_reserv = fields.Float(
        "Réservé unitaire",
        compute="_compute_unit_reserv",
        store=False,
    )

    @api.depends("product_uom_qty", "product_uom_id")
    def _compute_unit_reserv(self):
        for rec in self:
            rec.unit_reserv = rec.product_uom_qty * rec.product_uom_id.ratio

    unit_done = fields.Float(
        "Fait unitaire", default=0.0, digits=(14, 2), index=1
    )

    # qty_done = fields.Float('Done', default=0.0, digits='Product Unit of Measure',
    #                         compute="_compute_unit_done")

    @api.onchange("unit_done")
    def _compute_unit_done(self):
        for rec in self:
            if rec.product_uom_id.ratio == 0:
                rec.qty_done = rec.unit_done
            else:
                rec.qty_done = rec.unit_done / rec.product_uom_id.ratio


