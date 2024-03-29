from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True
    )
    property_state = fields.Selection(related="property_id.state")
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = (
                fields.Datetime.from_string(record.create_date)
                if record.create_date
                else fields.Date.today()
            )
            record.date_deadline = create_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                create_date = (
                    fields.Datetime.from_string(record.create_date)
                    if record.create_date
                    else fields.Date.today()
                )
                deadline_date = fields.Date.from_string(record.date_deadline)
                record.validity = (deadline_date - create_date.date()).days

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.offer_ids.filtered(
                lambda property_offer: property_offer.status == "accepted"
                and property_offer.id != offer.id
            ):
                raise UserError(
                    "Another offer has already been accepted for this property."
                )
            offer.property_id.state = "offer_accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.write({"status": "accepted"})
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.write({"status": "refused"})
        return True

    _sql_constraints = [
        (
            "check_offer_price_positive",
            "CHECK(price > 0)",
            "The offer price must be strictly positive.",
        )
    ]

    @api.model
    def create(self, vals):
        property_record = self.env["estate.property"].browse(vals.get("property_id"))

        if property_record.state == "new":
            property_record.write({"state": "offer_received"})
        else:
            max_existing_offer_price = max(property_record.offer_ids.mapped("price"), default=0)
            if vals.get("price") <= max_existing_offer_price:
                raise ValidationError(f"The offer price must be higher than {max_existing_offer_price}")

        return super().create(vals)
