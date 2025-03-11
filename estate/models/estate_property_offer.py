from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import UserError

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

    validity = fields.Integer(
        string="Validity (days)",
        default=7,
        help="Number of days the offer is valid."
    )
    date_deadline = fields.Date(
        string="Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
        help="Computed as the creation date plus the validity (days)."
    )

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                # Convert create_date (string/datetime) to a date object
                create_date_date = fields.Datetime.from_string(offer.create_date).date()
                offer.date_deadline = create_date_date + timedelta(days=offer.validity)
            else:
                # Fallback if create_date is not yet set (e.g., record not yet created)
                offer.date_deadline = False

    def _inverse_date_deadline(self):
        for offer in self:
            # Only update validity if create_date is available and date_deadline is set
            if offer.create_date and offer.date_deadline:
                # Convert create_date to a date object using from_string().date()
                create_date_date = fields.Datetime.from_string(offer.create_date).date()
                # Calculate the difference in days between deadline and creation date
                validity_days = (offer.date_deadline - create_date_date).days
                # Ensure validity is not negative
                offer.validity = validity_days if validity_days >= 0 else 0

    def action_accepted(self):
        for rec in self:
            rec.status = 'accepted'
            rec.property_id.buyer_id = rec.partner_id
            rec.property_id.selling_price = rec.price

    def action_refused(self):
        for rec in self:
            rec.status = 'refused'

