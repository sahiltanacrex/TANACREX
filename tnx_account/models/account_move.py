
import datetime

# -*- coding: utf-8 -*-

from odoo import models, fields, api
class Account_move(models.Model):
    _inherit="account.move"

    origin_tnx = fields.Char('Origine')
    c_f = fields.Char('C&F')
    gross_weight = fields.Char('Poids brute')
    net_weight = fields.Char('Poids net')
    volume = fields.Integer('Volume')
    seal_serial = fields.Char('Plombs')
    container_serial= fields.Char('Contenaire')

    seq_bis = fields.Char('Num de facture Bis')

    picking_ids = fields.Many2many(
        comodel_name="stock.picking",
        string="Transfert relié",
        store=True,
        compute="_compute_picking_ids",
        help="Related pickings "
        "(only when the invoice has been generated from a sale order).",
    )
        
    
    bank_company_ids = fields.Many2many('bank.company', 'account_move_id', string='Banque')

    delivery_adress = fields.Char('Adresse de livraison')


    def set_sequence_year(self):
        date = datetime.date.today()
        year = date.strftime("%Y")
        return year

    def action_post(self):

        """if sequences is set and every param is right create sequences by button click

        Returns:
            _sequences_: test type of customer and set if EX, LS , VL
        """

        check_partner_type=self.partner_id.partner_type

        if check_partner_type and not self.seq_bis:
            get_ex=self.env['tnx.ex']
            get_ls=self.env['tnx.ls']
            get_vl=self.env['tnx.vl']

            if check_partner_type == 'ex':
                self._set_seq(get_ex)
            
            if check_partner_type == 'ls':
                self._set_seq(get_ls)
                
            
            if check_partner_type == 'vl':
                self._set_seq(get_vl)
                
            
        values = super(Account_move, self).action_post()
        self.update({'name':self.name + '-' + check_partner_type.upper()})
        # self.update({'name':self.name + '-' + check_partner_type.upper()})

        return values

    def _set_seq(self,type):
        """
            this function create the second sequences from invoice
        """
        check_partner_type=self.partner_id.partner_type

        sec_last=1
        
        get_last_id = type.search([], limit=1, order='id desc')
        
        last_create_date=get_last_id.create_date 

        #! TODO this get_year is for testing if it was new year and it restart count
        if last_create_date != False:
            get_last_year=last_create_date.strftime("%Y")
        else:
            get_last_year=1993

        # import pudb; pudb.set_trace()
        
        get_year= self.set_sequence_year()

        if get_last_id:
            if get_last_year == get_year:
                sec_last=get_last_id.name+1
            
        
        get_year=str(get_year)
        l = len(get_year)
        get_year=get_year[l - 2:]
        
        type.create({
            "name": sec_last,
            "sequences_year":get_year,
            "rel_invoice_id": self.id,
            "rel_state_invoice":'posted'
            })

        seq_bis= f"{check_partner_type.upper()} {sec_last}/{get_year}"
        self.write({'seq_bis':seq_bis})
        # self.update({'name':self.name + '-' + check_partner_type.upper()})

    


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

    def get_customer_order(self,customer_bc):
        """
            get BC client dans BC original
        """
        so=self.env['sale.order'].search([('name', '=', customer_bc)])

        # self._cr.execute(f"""
        #     SELECT sale_order_partner
        #     FROM sale_order
        #     WHERE name = '{customer_bc}'
        # """, [list(self.ids)])
        
        # customer_sale_order = self._cr.fetchone()
        return so.sale_order_partner

    def get_delivery_order_id(self,id):
        """
            get BL id
        """
        id_bl=[]

        bc=self.env['sale.order'].search([('name', '=', id)])

        bl=self.env['stock.picking'].search([('origin','=',bc.name)])

        for i in bl:
            id_bl.append(i.id)

        return id_bl

    def get_bl_name(self,id):
        """
            get BL name
        """      
        bl_name=self.env['stock.picking'].search([('id','=',id)])
        return bl_name.name


    def get_bank(self,bank_id,currency_id):
        list_info=[]
        get_len=len(bank_id)-1
        count=0
        
        for i in bank_id:
            serial_bank=self.env['bank.company.line'].search([('res_currency_id', '=', currency_id),('bank_id', '=', i.id)])
            list_info.append(serial_bank.bank_id.bank)
            
            if count < get_len:
                list_info.append(serial_bank.account_registration + ", ")
                count+=1
            else:
                list_info.append(serial_bank.account_registration)


        values=' '.join([str(item) for item in list_info])
        return values

