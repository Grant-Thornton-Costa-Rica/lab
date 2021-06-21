from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Pais_Model(models.Model):
    _name = 'm.pais'
    _sql_constraints = [
        ('codigo_pais_unique', 'unique(codigo_pais)', 'Codigo: El valor del código que desea ingresar ya existe, pruebe con uno distinto.')
    ]
    
    codigo_pais = fields.Integer('Codigo')
    nombre = fields.Char('Nombre')
    nacionalidad = fields.Many2one('m.registro_salidas_pais', 'Registro de Salida')
    registro_salida = fields.One2many('m.pais', 'nacionalidad', string='Pais')





    