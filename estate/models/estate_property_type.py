from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'

    name=fields.Char(string='Property Type')
    property_ids = fields.One2many('estate.property','property_type_id')
