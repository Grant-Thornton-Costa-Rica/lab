from odoo import models, fields, api

class Detalle_Salidas_Model(models.Model):
    _name = 'm.detalle'
    
    pais_visitado = fields.Many2one('m.pais', 'Pais Visitado')
    fecha_salida = fields.Datetime('Fecha Salida')
    fecha_entrada = fields.Datetime('Fecha Entrada')
    observaciones = fields.Char('Observaciones')
    registro_salida = fields.Many2one('m.registro', 'Detalle Salida')

    def _check_dates(self, cr, uid, ids, context=None):
        if context == None:
            context = {}
        obj_task = self.browse(cr, uid, ids[0], context=context)
        start = obj_task.fecha_salida or False
        end = obj_task.fecha_entrada or False
        if start and end:
            if start > end:
                return False
        return True

    _constraints = [
        (_check_dates, 'Error! La fecha de entrada debe ser menor a la fecha de entrada', ['fecha_salida'])
    ]

