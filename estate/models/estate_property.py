from odoo import models, fields

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    # Basic fields added as per requirement
    name = fields.Char(string="Name", required=True)  # Char field for property name
    description = fields.Text(string="Description")  # Text field for detailed description
    postcode = fields.Char(string="Postcode")  # Char field for postal code
    date_availability = fields.Date(string="Date Available")  # Date field for availability
    expected_price = fields.Float(string="Expected Price", required=True)  # Float field for expected price
    selling_price = fields.Float(string="Selling Price")  # Float field for selling price
    bedrooms = fields.Integer(string="Bedrooms")  # Integer field for number of bedrooms
    living_area = fields.Integer(string="Living Area")  # Integer field for living area (in sqft/m²)
    facades = fields.Integer(string="Facades")  # Integer field for number of facades
    garage = fields.Boolean(string="Garage")  # Boolean field indicating garage presence
    garden = fields.Boolean(string="Garden")  # Boolean field indicating garden availability
    garden_area = fields.Integer(string="Garden Area")  # Integer field for garden area size
    garden_orientation = fields.Selection(
        selection=[
            ('North', 'North'),
            ('South', 'South'),
            ('East', 'East'),
            ('West', 'West')
        ],
        string="Garden Orientation"
    )  # Selection field with 4 possible values for garden orientation
