from odoo import models, fields, api
from openerp.tools.translate import _

class Detalle_Salidas_Model(models.Model):
    _name = 'm.detalle'
    _description = 'Modulo Detalle Salidas'
    
    pais_visitado = fields.Many2one('m.pais', 'Pais Visitado')
    fecha_salida = fields.Datetime('Fecha Salida')
    fecha_entrada = fields.Datetime('Fecha Entrada')
    observaciones = fields.Char('Observaciones')
    registro_salida = fields.Many2one('m.registro', 'Detalle Salida')

    def onchange_end_date(self, cr, uid, ids, fecha_entrada, fecha_salida):
        if (fecha_salida and fecha_entrada) and (fecha_salida < fecha_entrada):
            raise osv.except_osv(_('Warning!'),_('The start date must be less than to the end date.'))
            result = {'value': {}}
        return result

