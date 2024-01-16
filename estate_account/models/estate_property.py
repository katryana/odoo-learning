from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_property_status_sold(self):
        result = super(EstateProperty, self).action_set_property_status_sold()

        for property_record in self:
            selling_price = property_record.selling_price
            administrative_fees = 100.00

            line_1_amount = (6 / 100) * selling_price
            line_2_amount = administrative_fees

            invoice_vals = {
                "partner_id": property_record.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "6% of Selling Price",
                            "quantity": 1,
                            "price_unit": line_1_amount,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": line_2_amount,
                        }
                    ),
                ],
            }

            self.env["account.move"].create(invoice_vals)

        return result
