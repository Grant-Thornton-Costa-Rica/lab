from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Detalle_Salidas_Model(models.Model):
    _name = 'm.detalle'
    
    pais_visitado = fields.Many2one('m.pais', 'Pais Visitado')
    fecha_salida = fields.Datetime('Fecha Salida')
    fecha_entrada = fields.Datetime('Fecha Entrada')
    observaciones = fields.Char('Observaciones')
    registro_salida = fields.Many2one('m.registro', 'Detalle Salida')

    @api.multi
    @api.constrains('fecha_salida', 'fecha_entrada')
    def fecha_val(self):
        for rec in self:
            if rec.fecha_salida < rec.fecha_entrada:
                raise ValidationError('La fecha de salida no puede ser mayor a la fecha de entrada')

