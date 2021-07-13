from odoo import models, fields, api

class Pais_Model(models.Model):
    _name = 'm.pais'
    _description = 'Modulo Pais'
    _rec_name = 'nombre'
    _sql_constraints = [
        ('codigo_pais_unique', 'unique(codigo_pais)', 'Codigo: El valor del código que desea ingresar ya existe, pruebe con uno distinto.')
    ]
    
    codigo_pais = fields.Integer('Codigo')
    nombre = fields.Char('Nombre')
    nacionalidad = fields.Many2one('m.registro', 'Nacionalidad')
    registro_salida = fields.One2many('m.detalle', 'registro_salida', string='Pais')
    pais_visitado = fields.Many2one('m.detalle', 'Pais Visitado')






    