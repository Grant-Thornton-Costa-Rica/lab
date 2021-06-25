from odoo import models, fields, api

class Registro_Salidas_Pais_Model(models.Model):
    _name = 'm.registro'
    _description = 'Modulo Registro Salidas'
    _rec_name = 'nombre'

    nombre = fields.Char('Nombre')
    fecha_nacimiento = fields.Date('Fecha Nacimiento')
    nacionalidad = fields.Many2one('m.pais', 'Nacionalidad')
    direccion = fields.Char('Direccion')
    detalle_salida = fields.One2many('m.detalle', 'registro_salida', string='Registro Salidas Pais')

    nombre_pais = fields.Char(compute='_compute_nombre_pais', string='')
    
    @api.depends('nacionalidad')
    def _compute_nombre_pais(self):
        self.nombre_pais = self.nacionalidad.nombre

    edad = fields.Char(compute='_compute_edad', string='')
    
    @api.depends('fecha_nacimiento')
    def _compute_edad(self):
        for rec in self:
            if rec.fecha_nacimiento and rec.fecha_nacimiento <= fields.Date.today():
                rec.age = relativedelta(
                    fields.Date.from_string(fields.Date.today()),
                    fields.Date.from_string(rec.fecha_nacimiento)
                ).years
            else:
                rec.age = 0

    