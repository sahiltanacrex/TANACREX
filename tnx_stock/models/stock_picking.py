from odoo import _, fields, models


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"
    bc_client = fields.Char(
        string='BC CLIENT',
        required=False)

    def report_colisages(self):
        view = self.env.ref("tnx_stock.note_colisage_form_view")
        selected = self.env.context.get("active_ids", [])
        wiz = self.env["note.colisage.wizard"].create(
            {"name": "Note de colisage", "stock_picking_ids": [(6, 0, selected)], "product_ids": [
                (6, 0, self.move_line_ids_without_package.mapped('product_id').ids)]}
        )
        return {
            "name": _("Impréssion note de colisage"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "note.colisage.wizard",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            "res_id": wiz.id,
            "context": self.env.context,
        }

    def action_open_label_custom(self):
        return self.env.ref("tnx_stock.action_etiquette_nexource_report").report_action(self)
    
    def get_right_number(self, val):
        val_string = str(val)
        val_split = val_string.split('.')
        if len(val_split) == 1:
            return '{:,}'.format(int(val)).replace(',', ' ')
        if int(val_split[1]) > 0:
            return '{:,}'.format(val).replace(',', ' ')
        else:
            return '{:,}'.format(int(val)).replace(',', ' ')
    
    
