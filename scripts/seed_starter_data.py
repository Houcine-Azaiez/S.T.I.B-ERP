"""Seed starter product data for the S.T.I.B Odoo prototype.

Run inside the Odoo container with:

    docker exec -i beton-odoo odoo shell -d stib_erp --no-http < scripts/seed_starter_data.py
"""

Category = env["product.category"].sudo()
Product = env["product.template"].sudo()

created_categories = []
created_products = []
updated_products = []


def get_or_create_category(path):
    parent = False
    current = None

    for part in path.split("/"):
        name = part.strip()
        domain = [("name", "=", name)]
        if parent:
            domain.append(("parent_id", "=", parent.id))
        else:
            domain.append(("parent_id", "=", False))

        current = Category.search(domain, limit=1)
        if not current:
            values = {"name": name}
            if parent:
                values["parent_id"] = parent.id
            current = Category.create(values)
            created_categories.append(current.complete_name)
        parent = current

    return current


uom_units = env.ref("uom.product_uom_unit")
uom_m2 = env.ref("uom.product_uom_square_meter")
uom_kg = env.ref("uom.product_uom_kgm")
uom_ton = env.ref("uom.product_uom_ton")

categories = {
    "paving": get_or_create_category("Finished Products/Paving Stones"),
    "blocks": get_or_create_category("Finished Products/Hollow Blocks"),
    "bordures": get_or_create_category("Finished Products/Bordures"),
    "cement": get_or_create_category("Raw Materials/Cement"),
    "aggregates": get_or_create_category("Raw Materials/Aggregates"),
    "pigments": get_or_create_category("Raw Materials/Pigments"),
    "additives": get_or_create_category("Raw Materials/Additives"),
    "pallets": get_or_create_category("Packaging/Pallets"),
}

product_specs = [
    ("Grey paving stone 20x10x6", categories["paving"], uom_m2, True, False, 25.0, 12.0),
    ("Red paving stone 20x10x6", categories["paving"], uom_m2, True, False, 28.0, 14.0),
    ("Hollow block 20x20x40", categories["blocks"], uom_units, True, False, 1.8, 0.9),
    ("Bordure 100x20x15", categories["bordures"], uom_units, True, False, 8.0, 4.0),
    ("Cement", categories["cement"], uom_ton, False, True, 0.0, 250.0),
    ("Sand", categories["aggregates"], uom_ton, False, True, 0.0, 30.0),
    ("Gravel", categories["aggregates"], uom_ton, False, True, 0.0, 40.0),
    ("Pigment", categories["pigments"], uom_kg, False, True, 0.0, 2.5),
    ("Pallet", categories["pallets"], uom_units, False, True, 0.0, 8.0),
]

for name, category, uom, sale_ok, purchase_ok, list_price, standard_price in product_specs:
    product = Product.search([("name", "=", name)], limit=1)
    values = {
        "name": name,
        "type": "consu",
        "is_storable": True,
        "categ_id": category.id,
        "uom_id": uom.id,
        "sale_ok": sale_ok,
        "purchase_ok": purchase_ok,
        "list_price": list_price,
        "standard_price": standard_price,
    }
    if "uom_ids" in Product._fields:
        values["uom_ids"] = [(6, 0, [uom.id])]

    if product:
        product.write(values)
        updated_products.append(product.name)
    else:
        product = Product.create(values)
        created_products.append(product.name)

env.cr.commit()

print("Created categories:", created_categories or "none")
print("Created products:", created_products or "none")
print("Updated products:", updated_products or "none")
print("Done.")
