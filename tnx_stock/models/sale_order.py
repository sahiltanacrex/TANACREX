from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for do_pick in self.picking_ids:
            do_pick.write({'bc_client': self.sale_order_partner})
        return res
