import logging
from odoo import models, fields, api

class Pais_Model(models.Model):
    _name = 'm.pais'

    nombre = fields.Char('Nombre')
    nacionalidad = fields.Many2one('m.registro_salidas_pais', 'Registro de Salida')
    registro_salida = fields.One2many('m.pais', 'nacionalidad', string='Pais')

    