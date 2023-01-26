from odoo import fields, models, api


class ModelName(models.Model):
    _inherit = 'stock.move'
    _description = 'Description'

    def _set_quantities_to_reservation(self):
        for move in self:
            if move.state not in ('partially_available', 'assigned'):
                continue
            for move_line in move.move_line_ids:
                if move.has_tracking != 'none' and not (move_line.lot_id or move_line.lot_name):
                    continue
                move_line.qty_done = move_line.product_uom_qty
                move_line.unit_done = move_line.unit_reserv
