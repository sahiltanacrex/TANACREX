from odoo import _, fields, models, api


class StockCarton(models.Model):
    _name = "stock.carton"
    name = fields.Char("Nom du carton")
    poids_net = fields.Float()
    poids_brut = fields.Float()

    sequence = fields.Char(string="Sequence number", readonly=True, default="/")

    @api.model
    def create(self, vals):
        seq = self.env["ir.sequence"].next_by_code("stock.carton.code") or "/"
        vals["sequence"] = seq
        vals["name"] = f"{vals['name']} {seq}"
        return super(StockCarton, self).create(vals)
