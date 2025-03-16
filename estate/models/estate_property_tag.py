from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This model is to store estate property tags"
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()
    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Tag name must be unique.')
    ]