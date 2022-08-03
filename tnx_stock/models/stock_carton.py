from odoo import _, fields, models, api


class StockCarton(models.Model):
    _name = "stock.carton"
    nom = fields.Char("Nom")
    poids_net = fields.Float()
    poids_brut = fields.Float()
    _rec_name = "id"

    sequence = fields.Char(string="Sequence number", readonly=True, default="/")

    @api.model
    def create(self, vals):
        seq = self.env["ir.sequence"].next_by_code("stock.carton.code") or "/"
        vals["sequence"] = seq
        return super(StockCarton, self).create(vals)

    def name_get(self):
        result = []
        for carton in self:
            name = carton.sequence + " " + carton.nom if carton.nom else carton.sequence
            result.append((carton.id, name))
        return result
