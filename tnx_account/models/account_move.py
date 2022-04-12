
import datetime

# -*- coding: utf-8 -*-

from odoo import models, fields, api
class Account_move(models.Model):
    _inherit="account.move"

    origin_tnx = fields.Char('Origin')
    c_f = fields.Char('C&F')
    gross_weight = fields.Char('Poids brut')
    net_weight = fields.Char('Poids net')
    volume = fields.Integer('Volume')
    seal_serial = fields.Char('Plombs')
    container_serial= fields.Char('Container')

    seq_bis = fields.Char('Num de facture Bis')

    picking_ids = fields.Many2many(
        comodel_name="stock.picking",
        string="Related Pickings",
        store=True,
        compute="_compute_picking_ids",
        help="Related pickings "
        "(only when the invoice has been generated from a sale order).",
    )
    def set_sequence_year(self):
        date = datetime.date.today()
        year = date.strftime("%Y")
        return year

    def action_post(self):
        check_partner_type=self.partner_id.partner_type
        if not self.seq_bis:
            get_ex=self.env['tnx.ex']
            get_ls=self.env['tnx.ls']
            get_vl=self.env['tnx.vl']
            if check_partner_type == 'ex':
                sec_last=0
        
                get_last = get_ex.search([], limit=1, order='create_date desc')
                
                get_year= self.set_sequence_year()

                if get_last:
                    sec_last+=get_last.name+1
                
                
                get_year=str(get_year)
                l = len(get_year)
                get_year=get_year[l - 2:]
                
                get_ex.create({"name": sec_last,"sequences_year":get_year,"rel_invoice_id": self.id,"rel_state_invoice":'posted'})

                seq_bis= f"{check_partner_type.upper()} {sec_last}/{get_year}"
                self.write({'seq_bis':seq_bis})
            
            if check_partner_type == 'ls':
                sec_last=0
        
                get_last = get_ls.search([], limit=1, order='create_date desc')
                
                get_year= self.set_sequence_year()

                if get_last:
                    sec_last+=get_last.name+1
                
                
                get_year=str(get_year)
                l = len(get_year)
                get_year=get_year[l - 2:]
                
                get_ls.create({"name": sec_last,"sequences_year":get_year,"rel_invoice_id": self.id,"rel_state_invoice":'posted'})

                seq_bis= f"{check_partner_type.upper()} {sec_last}/{get_year}"
                self.write({'seq_bis':seq_bis})
            
            if check_partner_type == 'vl':
                sec_last=0
        
                get_last = get_vl.search([], limit=1, order='create_date desc')
                
                get_year= self.set_sequence_year()

                if get_last:
                    sec_last+=get_last.name+1
                
                
                get_year=str(get_year)
                l = len(get_year)
                get_year=get_year[l - 2:]
                
                get_vl.create({"name": sec_last,"sequences_year":get_year,"rel_invoice_id": self.id,"rel_state_invoice":'posted'})

                seq_bis= f"{check_partner_type.upper()} {sec_last}/{get_year}"
                self.write({'seq_bis':seq_bis})
            
        values = super(Account_move, self).action_post()
        return values

    @api.depends("invoice_line_ids", "invoice_line_ids.move_line_ids")
    def _compute_picking_ids(self):
        for invoice in self:
            invoice.picking_ids = invoice.mapped(
                "invoice_line_ids.move_line_ids.picking_id"
            )

    def action_show_picking(self):
        """This function returns an action that display existing pickings
        of given invoice.
        It can either be a in a list or in a form view, if there is only
        one picking to show.
        """
        self.ensure_one()
        form_view_name = "stock.view_picking_form"
        xmlid = "stock.action_picking_tree_all"
        action = self.env["ir.actions.act_window"]._for_xml_id(xmlid)
        if len(self.picking_ids) > 1:
            action["domain"] = "[('id', 'in', %s)]" % self.picking_ids.ids
        else:
            form_view = self.env.ref(form_view_name)
            action["views"] = [(form_view.id, "form")]
            action["res_id"] = self.picking_ids.id
        return action

