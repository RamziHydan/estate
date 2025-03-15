from dateutil.utils import today
from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api, _

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    # Basic fields added as per requirement
    name = fields.Char(string="Name", required=True, default="Unknown")  # Char field for property name
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
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
    garden = fields.Boolean(string="Garden", defualt=True)  # Boolean field indicating garden availability
    garden_area = fields.Integer(string="Garden Area")  # Integer field for garden area size
    total_area = fields.Integer(compute='_compute_total')
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
    offer_ids = fields.One2many('estate.property.offer','property_id')
    best_price = fields.Integer(compute='_compute_highest')
    active = fields.Boolean(string="Active", default=True)

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_highest(self):
        for rec in self:
            # Map the prices from offer_ids into a list
            prices = rec.offer_ids.mapped('price')
            # If there are any prices, set best_price to the maximum; otherwise, use 0.0 or False as needed
            rec.best_price = max(prices) if prices else 0.0

    @api.onchange("garden")
    def onchange_check_area_orientation(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
            # return {'warning': {
            #     'title': _("Important ❗"),
            #     'message': ('By ckecking garden default values has been set to area and orientation as 10 and North in order')}}
        else:
            self.garden_area = 0
            self.garden_orientation = False
            # return {'warning': {
            #     'title': _("Important ❗"),
            #     'message': ('By unckecking garden current values has been removed from to area and orientation')}}

    def action_cancel(self):
        """Cancel the property if it is not already sold."""
        for rec in self:
            if rec.state == 'sold out':
                raise UserError(_("A sold property cannot be cancelled."))
            rec.state = 'offer canceled'

    def action_sold(self):
        """Mark the property as sold if it is not cancelled."""
        for rec in self:
            if rec.state == 'offer canceled':
                raise UserError(_("A cancelled property cannot be sold."))
            rec.state = 'sold out'

    _sql_constraints = [
        ('CHECK_POSITIVE', 'CHECK(expected_price > 0 AND selling_price > 0 AND best_price > 0)', 'Value must be Positive')
    ]

    # @api.constrains('expected_price', 'selling_price', 'best_price')
    # def _check_price_positive(self):
    #     for rec in self:
    #         if rec.expected_price <= 0:
    #             raise ValidationError(_("Expected Price must be positive."))
    #         # selling_price is read-only, but if it is set, validate it
    #         if rec.selling_price and rec.selling_price <= 0:
    #             raise ValidationError(_("Selling Price must be positive."))
    #         if rec.best_price and rec.best_price <= 0:
    #             raise ValidationError(_("Best Price must be positive."))

    def check_price(self):
        for rec in self:
            for offer in rec.offer_ids:
                if offer.price <= 0:
                    raise UserError(_("Offer price must be positive."))

