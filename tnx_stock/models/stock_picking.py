from odoo import _, fields, models, api


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    def report_colisage(self):
        return self.env.ref("tnx_stock.action_tnx_package_report").report_action(self)

    def get_data(self):
        datas = {"ids": self.env.context.get("active_ids", [])}
        ids = self.env["stock.picking"].browse(datas)
        return ids
