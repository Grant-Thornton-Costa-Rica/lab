from odoo import models, fields, api

class Detalle_Salidas_Model(models.Model):
    _name = 'm.detalle'
    
    pais_visitado = fields.Many2one('m.pais', 'Pais Visitado')
    fecha_salida = fields.Datetime('Fecha Salida')
    fecha_entrada = fields.Datetime('Fecha Entrada')
    observaciones = fields.Char('Observaciones')
    registro_salida = fields.Many2one('m.registro', 'Detalle Salida')

    def _check_dates(self,):
        start = fecha_salida 
        end = fecha_entrada
        if start > end:
            return True
        return False

    _constraints = [
        (_check_dates, 'Error! La fecha de entrada debe ser menor a la fecha de entrada', ['fecha_salida'])
    ]

