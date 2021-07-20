# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class cabysCode(models.Model):
    _name = 'cabys.code'
    _description = 'Cabys code'
    _rec_name = 'display_name'

    name = fields.Char(string='Descripción')
    code = fields.Char(string='Código')
    tax = fields.Char(string='Impuesto')
    display_name = fields.Char(compute='_compute_display_name',store=True)
    
    category1 = fields.Char(string='Categoría 1')
    category2 = fields.Char(string='Categoría 2')
    category3 = fields.Char(string='Categoría 3')
    category4 = fields.Char(string='Categoría 4')
    category5 = fields.Char(string='Categoría 5')
    category6 = fields.Char(string='Categoría 6')
    category7 = fields.Char(string='Categoría 7')
    category8 = fields.Char(string='Categoría 8')
    
    active = fields.Boolean(string='Activo',default = True)

    @api.depends('code','name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '{}-{}'.format(record.code,record.name)

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if not recs:
               recs = self.search([('display_name', operator, name)] + args, limit=limit)
        return recs.name_get()

    