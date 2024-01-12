from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer(string="Sequence", default=1)

    _sql_constraints = [
        (
            "unique_property_tag_name",
            "UNIQUE(name)",
            "The name must be unique.",
        )
    ]
