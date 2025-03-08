from dateutil.utils import today

from odoo import models, fields

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    # Basic fields added as per requirement
    name = fields.Char(string="Name", required=True, default="Unknown")  # Char field for property name
    tag_ids = fields.Many2many('estate.property.tag',string='Property Tag')
    property_type_id = fields.Many2one("estate.property.type",string="Property Type",)
    description = fields.Text(string="Description")  # Text field for detailed description
    postcode = fields.Char(string="Postcode")  # Char field for postal code
    date_availability = fields.Date(string="Date Available", copy=False, default=today())  # Date field for availability
    expected_price = fields.Float(string="Expected Price", required=True)  # Float field for expected price
    selling_price = fields.Float(string="Selling Price", readonly=True)  # Float field for selling price
    bedrooms = fields.Integer(string="Bedrooms", default=2)  # Integer field for number of bedrooms
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
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('offer canceled', 'Offer Canceled'),
            ('sold out', 'Sold Out')
        ],
        string="State",
        default="new"
    )
    salesperson_id = fields.Many2one(
        'res.users', string='Salesperson', default=lambda self: self.env.uid,
        help = "Salesperson responsible for the property. Defaults to the current user.")
    buyer_id = fields.Many2one(
        'res.partner', string='Buyer', copy=False,
        help="Buyer of the property. This field will not be duplicated.")
    active = fields.Boolean(string="Active", default=True)
