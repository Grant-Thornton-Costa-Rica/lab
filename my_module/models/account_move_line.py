from odoo import models, fields, api

class Tipo_Cedula_Model(models.Model):
    _inherit = 'account.move.line'

    codigo_cabys = fields.Char('Codigo Cabys')

    def _check_cabys(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids, context=context):
            if rec.codigo_cabys and isinstance(rec.codigo_cabys, int):
                return True
        return False
    
    _constraints = [
        (_check_cabys, 'El campo solo acepta valores numericos', ['codigo_cabys']),
    ]
