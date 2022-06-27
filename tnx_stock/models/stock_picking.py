from odoo import _, fields, models, api


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    def report_colisages(self):
        view = self.env.ref('tnx_stock.note_colisage_form_view')
        selected = self.env.context.get("active_ids", [])
        wiz = self.env['note.colisage.wizard'].create({
            'name': "Note de colisage",
            'stock_picking_ids': [(6, 0, selected)]
        })
        return {
            'name': _('Impréssion note de colisage'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'note.colisage.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': wiz.id,
            'context': self.env.context,
        }

