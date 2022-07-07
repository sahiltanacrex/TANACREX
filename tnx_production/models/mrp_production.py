# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning


class MrpProduction(models.Model):
    """Manufacturing Orders"""

    _inherit = "mrp.production"

    partner_id = fields.Many2one(
        "res.partner", string="client", store=True, compute="_compute_source_id"
    )
    order_id = fields.Many2one(
        "sale.order", string="BC", store=True, compute="_compute_source_id"
    )
    developments = fields.Selection(
        [("1", "0%"), ("2", "25%"), ("3", "50%"), ("4", "75%"), ("5", "100%")],
        default="1",
        string="Avancement",
    )
    check_bc = fields.Boolean("Check Bc")
    image_1920 = fields.Image("Image", compute="_compute_product_id")
    bc_client = fields.Char("Bc Client")
    line_product = fields.Float("Ligne")
    product_type = fields.Char("Type de produit")
    color_product = fields.Char("Couleur")

    def action_send_mail_odf(self):
        developments_perccent = dict(self._fields["developments"].selection).get(
            self.developments
        )

        if self.partner_id:
            template_id = self.env.ref("tnx_production.send_mail_order_manufacture").id
            compose_form_id = self.env.ref("mail.email_compose_message_wizard_form").id
            ctx = {
                "default_model": "mrp.production",
                "default_res_id": self.id,
                "default_use_template": bool(template_id),
                "default_template_id": template_id,
                "default_composition_mode": "comment",
                "custom_layout": "mail.mail_notification_paynow",
                "force_email": True,
                "mail_partner_id": self.partner_id.id,
                "mail_partner_name": self.partner_id.name,
                "order_origin": self.order_id.name,
                "developments_states": developments_perccent,
            }
            return {
                "type": "ir.actions.act_window",
                "view_type": "form",
                "view_mode": "form",
                "res_model": "mail.compose.message",
                "views": [(compose_form_id, "form")],
                "view_id": compose_form_id,
                "target": "new",
                "context": ctx,
            }

    @api.depends("product_id")
    def _compute_product_id(self):
        for val in self:
            if val.product_id:
                val.image_1920 = val.product_id.image_1920

    @api.depends("origin")
    def _compute_source_id(self):
        for production in self:
            if production.origin:
                devis_name = production.origin.split(" - ")
                if len(devis_name) > 1:
                    source = self.env["sale.order"].search(
                        [("name", "=", devis_name[1])]
                    )
                    print("---------------------")
                    print(source)
                    if source:
                        try:
                            production.order_id = source
                            production.partner_id = source.partner_id
                            production.check_bc = True
                            production.bc_client = source.sale_order_partner
                            production.line_product = production.product_id.line
                            production.product_type = production.product_id.product_type
                            production.color_product = (
                                production.product_id.product_tmpl_id.color
                            )
                        except Exception as e:
                            # production.order_id = False
                            raise UserError(e)

                    else:
                        # production.order_id = False
                        print("ato ary hoe")

                    print("---------------------")
                    print(source)
