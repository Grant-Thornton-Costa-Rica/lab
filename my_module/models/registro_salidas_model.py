import logging
from odoo import models, fields, aspi

class Registro_Salidas_Pais_Model(models.Model):
    _name = 'm.registro'
    _description = 'Modulo Registro Salidas Pais'
    _rec_name = 'nombre'

    nombre = fields.Char('Nombre')
    fecha_nacimiento = fields.Date('Fecha Nacimiento')
    nacionalidad = fields.Many2one('m.pais', 'Nacionalidad')
    registro_salida = fields.Many2one('m.detalle', 'Detalle Salida')
    detalle_salida = fields.One2many('m.registro', 'registro_salida', string='Registro Salidas Pais')