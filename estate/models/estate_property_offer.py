from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'This model created for offers'

    price = fields.Float(string='Property Price')
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
        help="This is property partner")
    property_id = fields.Many2one(
        'estate.property',
        string='Partner',
        required=True,
        help="The property for which the offer is made")