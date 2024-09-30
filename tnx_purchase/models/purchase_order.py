from odoo import models , fields 

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    have_signature = fields.Boolean()