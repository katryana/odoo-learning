from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer()

    _sql_constraints = [
        (
            "unique_property_type_name",
            "UNIQUE(name)",
            "The name must be unique.",
        )
    ]
