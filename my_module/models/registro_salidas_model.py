from odoo import models, fields, api
from datetime import date

class Registro_Salidas_Pais_Model(models.Model):
    _name = 'm.registro'
    _description = 'Modulo Registro Salidas'
    _rec_name = 'nombre'

    nombre = fields.Char('Nombre')
    fecha_nacimiento = fields.Date('Fecha Nacimiento')
    edad = fields.Char(compute='_compute_edad', string='Edad')
    nacionalidad = fields.Many2one('m.pais', 'Nacionalidad')
    direccion = fields.Char('Direccion')
    detalle_salida = fields.One2many('m.detalle', 'registro_salida', string='Registro Salidas Pais')

    nombre_pais = fields.Char(compute='_compute_nombre_pais', string='')
    
    @api.depends('nacionalidad')
    def _compute_nombre_pais(self):
        self.nombre_pais = self.nacionalidad.nombre

    @api.depends('fecha_nacimiento')
    def _compute_edad(self):
        hoy = date.today()
        if fecha_nacimiento:
            dif = int(fecha_nacimiento.replace(year = hoy.year) > hoy)
            return date.hoy().year - fecha_nacimiento - dif
        else:
            return 0
        

    