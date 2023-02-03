# -*- coding: utf-8 -*-
# from odoo import http


# class TnxSale(http.Controller):
#     @http.route('/tnx_sale/tnx_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tnx_sale/tnx_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tnx_sale.listing', {
#             'root': '/tnx_sale/tnx_sale',
#             'objects': http.request.env['tnx_sale.tnx_sale'].search([]),
#         })

#     @http.route('/tnx_sale/tnx_sale/objects/<model("tnx_sale.tnx_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tnx_sale.object', {
#             'object': obj
#         })
