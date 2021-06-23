from odoo import models, fields, api

class Detalle_Salidas_Model(models.Model):
    _name = 'm.detalle'

    pais_visitado = fields.Many2one('m.pais', string='Pais Visitado')
    fecha_salida = fields.Datetime('Fecha Salida')
    fecha_entrada = fields.Datetime('Fecha Entrada')
    observaciones = fields.Char('Observaciones')
    registro_salida = fields.Many2one('m.detalle', 'Detalle Salida')
