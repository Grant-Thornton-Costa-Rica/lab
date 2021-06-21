import logging
from odoo import models, fields, api

class Pais_Model(models.Model):
    _name = 'm.pais'

    nombre = fields.Char('Nombre')
    nacionalidad = fields.Many2one('m.registro_salidas_pais', 'Registro de Salida')
    registro_salida = fields.One2many('m.pais', 'nacionalidad', string='Pais')

    # def field_view_get(self, view_id=None, view_type='tree', toolbar=False, submenu=False):
    #     res = super(Pais_Model, self).field_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)

    #     if view_type == 'tree':
    #         from lxml import etree
    #         doc = etree.xml(res['arch'])
    #         pais = doc.xpath("//field[@name='nombre']")
    #         if pais:
    #             pais[0].set("string", "Nombre")
    #             pais[0].addnext(etree.Element('label', {'string': 'Nombre Pais'}))
    #             res['arch'] = etree.tostring(doc, encoding='unicode')
           
    #     return res

    # def write(self, values):
    #     res = super(Pais, self).write(values)

    #     if 'name' in values.keys():
    #         for pais in self:
    #             if pais.id:
    #                 pais.id.write({'name': pais.name})

    #         _logger.info(
    #             "ORM write pais >>>>>>>>> {} ".format(values)
    #         )

    #     return res
