from odoo import models, fields, api

class Detalle_Salidas_Model(models.Model):
    _name = 'm.detalle'
    
    pais_visitado = fields.Many2one('m.pais', 'Pais Visitado')
    fecha_salida = fields.Datetime('Fecha Salida')
    fecha_entrada = fields.Datetime('Fecha Entrada')
    observaciones = fields.Char('Observaciones')
    registro_salida = fields.Many2one('m.registro', 'Detalle Salida')

    def _check_date(self, cr, uid, vals, context=None):
    for obj in self.browse(cr, uid, ids):
        start_date = obj.fecha_salida
        end_date = obj.fecha_entrada

        if start_date and end_date:
            DATETIME_FORMAT = "%Y-%m-%d"
            from_dt = datetime.datetime.strptime(start_date, DATETIME_FORMAT)
            to_dt = datetime.datetime.strptime(end_date, DATETIME_FORMAT)

            if to_dt < from_dt:
                return False
            return True

    _constraints = [
        (_check_date, 'Your Message!', ['fecha_salida','fecha_entrada']),
    ]

