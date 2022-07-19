from odoo import _, fields, models, api


class NoteDeColisage(models.TransientModel):
    _name = "note.colisage.wizard"
    name = fields.Char()
    partner_id = fields.Many2one("res.partner", string="Client")
    stock_picking_ids = fields.Many2many(
        "stock.picking", "colisage_id", string="Stock selected"
    )
    poids_net = fields.Float()
    poids_brut = fields.Float()

    def report_colisage(self):
        # self.ensure_one()
        # data = []
        # for rec in self.stock_picking_ids:
        #     for line in rec.move_line_ids_without_package:
        #         data.append(
        #             {
        #                 "bc": rec.sale_id.name if rec.sale_id else None,
        #                 "bl": rec.name if rec.name else None,
        #                 "article": line.product_id.name if line.product_id else None,
        #                 "line": line.product_id.line if line.product_id else None,
        #                 "diamter": line.product_id.diameter
        #                 if line.product_id
        #                 else None,
        #                 "conditionnment": line.product_uom_id.ratio
        #                 if line.product_uom_id
        #                 else None,
        #                 "qty": line.qty_done,
        #                 "carton": line.carton_id.name if line.carton_id else None,
        #             }
        #         )
        # self = self.with_context(demo="data")
        return self.env.ref("tnx_stock.action_tnx_package_report").report_action(self)
