# -*- coding: utf-8 -*-
# from odoo import http


# class TnxProduct(http.Controller):
#     @http.route('/tnx_product/tnx_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tnx_product/tnx_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tnx_product.listing', {
#             'root': '/tnx_product/tnx_product',
#             'objects': http.request.env['tnx_product.tnx_product'].search([]),
#         })

#     @http.route('/tnx_product/tnx_product/objects/<model("tnx_product.tnx_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tnx_product.object', {
#             'object': obj
#         })
