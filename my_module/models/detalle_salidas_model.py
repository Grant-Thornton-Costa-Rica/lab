from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class Detalle_Salidas_Model(models.Model):
    _name = 'm.detalle'
    
    pais_visitado = fields.Many2one('m.pais', 'Pais Visitado')
    fecha_salida = fields.Datetime('Fecha Salida')
    fecha_entrada = fields.Datetime('Fecha Entrada')
    observaciones = fields.Char('Observaciones')
    registro_salida = fields.Many2one('m.registro', 'Detalle Salida')

    dias = fields.Integer(compute='_compute_calcular_dias', 'Dias transcurridos')
    
    @api.depends('fecha_salida', 'fecha_entrada')
    def _compute_calcular_dias(self):
        datetime_format = '%Y-%m-%d %H:%M:%S'
        fec_sal = datetime.datetime.strptime(fecha_salida, datetime_format)
        fec_ent = datetime.datetime.strptime(fecha_entrada, datetime_format)
        timedelta = fec_ent - fec_sal
        dif_dias = timedelta.days + float(timedelta.seconds) / 86400

        return dif_dias

    @api.constrains('fecha_salida', 'fecha_entrada')
    def fecha_val(self):
        for rec in self:
            if rec.fecha_salida > rec.fecha_entrada:
                raise ValidationError('La fecha de salida no puede ser mayor a la fecha de entrada')

