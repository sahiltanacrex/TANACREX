# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning

class MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'

    partner_id = fields.Many2one('res.partner', string='client',store=True)
    order_id = fields.Many2one('sale.order', string='BC',store=True)
    developments = fields.Selection([('1', '0%'), ('2', '25%'), ('3', '50%'), ('4', '75%'),('5', '100%')], default='1',string="Avancement")


    def action_send_mail_odf(self):
        order=self.env['sale.order']
        if self.origin:
            get_str_origin=self.origin 
            origin=get_str_origin.split(" - ")
            get_sale_order_origin=origin[1]
            
            if get_sale_order_origin:
                origin_sale=order.search([('name', '=', get_sale_order_origin)])
                self.partner_id= origin_sale.partner_id
                self.order_id= origin_sale
        developments_perccent=dict(self._fields['developments'].selection).get(self.developments)

        if self.partner_id:
            template_id = self.env.ref('tnx_production.send_mail_order_manufacture').id
            compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
            ctx = {
                'default_model': 'mrp.production',
                'default_res_id': self.id,
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                'default_composition_mode': 'comment',
                'custom_layout': "mail.mail_notification_paynow",
                'force_email': True,
                'mail_partner_id':self.partner_id.id,
                'mail_partner_name':self.partner_id.name,
                'order_origin':self.order_id.name,
                'developments_states':developments_perccent,
            }
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mail.compose.message',
                'views': [(compose_form_id, 'form')],
                'view_id': compose_form_id,
                'target': 'new',
                'context': ctx,
            }
        