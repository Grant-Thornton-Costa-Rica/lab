from odoo import models, fields, api

class accountMoveLineModel(models.Model):
    _inherit = 'account.move.line'

    codigo_cabys = fields.Char('Codigo Cabys')

    
    
