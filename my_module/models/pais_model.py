from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Pais_Model(models.Model):
    _name = 'm.pais'

    nombre = fields.Char('Nombre')
    codigo_pais = fields.Integer('Codigo Pais')
    nacionalidad = fields.Many2one('m.registro_salidas_pais', 'Registro de Salida')
    registro_salida = fields.One2many('m.pais', 'nacionalidad', string='Pais')

    @api.constrains('codigo_pais')
    def check_codigo_pais(self):
        cod = self.search([]) - self
        val = [x for x in cod]
        if self in val:
            raise ValidationError('El codigo del pais que desea ingresar ya existe')

        return True



    