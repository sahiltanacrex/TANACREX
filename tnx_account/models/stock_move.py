from odoo import _, fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    invoice_line_ids = fields.Many2many(
        comodel_name="account.move.line",
        relation="stock_move_invoice_line_rel",
        column1="move_id",
        column2="invoice_line_id",
        string="Invoice Line",
        copy=False,
        readonly=True,
    )

    def write(self, vals):
        """
        User can update any picking in done state, but if this picking already
        invoiced the stock move done quantities can be different to invoice
        line quantities. So to avoid this inconsistency you can not update any
        stock move line in done state and have invoice lines linked.
        """
        if "product_uom_qty" in vals and not self.env.context.get(
            "bypass_stock_move_update_restriction"
        ):
            for move in self:
                if move.state == "done" and move.invoice_line_ids:
                    raise UserError(
                        _("Vous ne pouvez pas modifier un mouvement de stock facturé")
                    )
        return super().write(vals)

    def get_type_false_number(self):
        type_false_lines =self.invoice_line_ids.filtered(lambda l: l.product_id.product_type == False)
        return len(type_false_lines)