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
    description = fields.Char()
    move_id = fields.Many2one("account.move", string="Facture")

    def report_colisage(self):
        return self.env.ref("tnx_stock.action_tnx_package_report").report_action(self)
    
    def get_formatted_qty(self, qty):
        result = f'{qty:,.2f}'.split('.')[0]
        return result.replace(',', ' ')
    
    def get_formatted_weight(self, weight):
        result = f'{weight:,.1f}'
        return result.replace(',', ' ').replace('.', ',')