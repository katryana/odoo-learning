from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(string="Property Type", required=True)

    _sql_constraints = [
        (
            "unique_property_tag_name",
            "UNIQUE(name)",
            "The name must be unique.",
        )
    ]
