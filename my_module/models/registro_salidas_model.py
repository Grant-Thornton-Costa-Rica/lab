from odoo import models, fields, api
import datetime

class Registro_Salidas_Pais_Model(models.Model):
    _name = 'm.registro'
    _description = 'Modulo Registro Salidas'
    _rec_name = 'nombre'

    nombre = fields.Char('Nombre')
    fecha_nacimiento = fields.Date('Fecha Nacimiento')
    edad = fields.Char(compute='_compute_edad', string='Edad')
    nacionalidad = fields.Many2one('m.pais', 'Nacionalidad')
    company = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company_id.id)
    direccion = fields.Char('Direccion')
    detalle_salida = fields.One2many('m.detalle', 'registro_salida', string='Registro Salidas Pais')

    nombre_pais = fields.Char(compute='_compute_nombre_pais', string='')
    
    @api.depends('nacionalidad')
    def _compute_nombre_pais(self):
        self.nombre_pais = self.nacionalidad.nombre

    @api.depends('fecha_nacimiento')
    def _compute_edad(self):
        hoy = datetime.date.today()
        for rec in self:
            if rec.fecha_nacimiento:
                fecha_nacimiento = fields.Datetime.to_datetime(rec.fecha_nacimiento).date()
                edad_total = str(int((hoy - fecha_nacimiento).days / 365))
                rec.edad = edad_total
            else:
                rec.edad = "No disponible"
        

    