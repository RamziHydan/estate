from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This model is to store estate property tags"

    name = fields.Char(required=True)