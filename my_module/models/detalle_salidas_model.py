from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime as dt

class Detalle_Salidas_Model(models.Model):
    _name = 'm.detalle'
    
    pais_visitado = fields.Many2one('m.pais', 'Pais Visitado')
    fecha_salida = fields.Date('Fecha Salida')
    fecha_entrada = fields.Date('Fecha Entrada')
    observaciones = fields.Char('Observaciones')
    registro_salida = fields.Many2one('m.registro', 'Detalle Salida')

    dias = fields.Char(compute='_compute_calcular_dias', string='Dias transcurridos')
    
    @api.depends('fecha_salida', 'fecha_entrada')
    def _compute_calcular_dias(self):
        if self.fecha_salida and self.fecha_entrada:
            for rec in self:
                rec.dias = (rec.fecha_entrada - rec.fecha_salida).days

    @api.constrains('fecha_salida', 'fecha_entrada')
    def fecha_val(self):
        for rec in self:
            if rec.fecha_salida > rec.fecha_entrada:
                raise ValidationError('La fecha de salida no puede ser mayor a la fecha de entrada')

