import logging
from odoo import models, fields, api

class Registro_Salidas_Pais_Model(models.Model):
    _name = 'm.registro_salidas_pais'

    nombre = fields.Char('Nombre')
    fecha_nacimiento = fields.Date('Fecha Nacimiento')
    nacionalidad = fields.Many2one('m.pais', 'Nacionalidad')
    registro_salida = fields.Many2one('m.detalle_salidas', 'Detalle Salida')
    detalle_salida = fields.One2many('m.registro_salidas_pais', 'registro_salida', string='Registro Salidas Pais')