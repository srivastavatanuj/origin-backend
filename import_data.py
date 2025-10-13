import os
import django
import pandas as pd
from decimal import Decimal
import decimal
import re
from django.core.exceptions import ValidationError

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from products.models import Product, Category, Brand


def extract_weight_and_unit(row):
    """Extract weight and weight unit from Units or Supplier note."""
    # Check Typical weight if price is by weight
    if row["Is price by weight"] and pd.notna(row["Typical weight"]):
        try:
            return Decimal(str(row["Typical weight"])), str(
                row["Unit of typical weight"]
            )
        except (ValueError, TypeError, decimal.InvalidOperation):
            pass

    # Supported units
    units_map = {
        "lb": "lb",
        "kg": "kg",
        "oz": "oz",
        "g": "g",
        "ml": "ml",
    }

    def extract_numeric_weight(text):
        text = str(text).lower().strip()
        match = re.search(r"(\d*\.?\d+|\d+/\d+)", text)
        if match:
            weight_str = match.group(0)
            try:
                if "/" in weight_str:
                    num, denom = map(int, weight_str.split("/"))
                    return Decimal(num) / Decimal(denom)
                return Decimal(weight_str)
            except (ValueError, TypeError, decimal.InvalidOperation):
                return None
        return None

    def extract_from_text(text):
        text = str(text).lower().strip()
        for unit in units_map:
            if unit in text:
                weight = extract_numeric_weight(text.split(unit)[0].strip())
                if weight:
                    return weight, units_map[unit]
        return None, None

    # Try Units column
    weight, unit = extract_from_text(row["Units"])
    if weight and unit:
        return weight, unit

    # Try Supplier note column
    weight, unit = extract_from_text(row["Supplier note"])
    if weight and unit:
        return weight, unit

    # Default weights based on SKU or note patterns
    DEFAULT_WEIGHTS = {
        "AC-DP": (Decimal("1.00"), "lb"),  # Beverages
        "100ct BAG": (Decimal("0.50"), "lb"),  # Bags
        "1 box": (Decimal("2.00"), "lb"),  # Boxes
        "1 UNIT": (Decimal("1.00"), "lb"),  # Generic units
    }

    sku = str(row["SKU"]).lower()
    note = str(row["Supplier note"]).lower()
    for pattern, (default_weight, default_unit) in DEFAULT_WEIGHTS.items():
        if pattern.lower() in sku or pattern.lower() in note:
            print(
                f"Applying default weight {default_weight} {default_unit} for SKU {row['SKU']}"
            )
            return default_weight, default_unit

    # Final fallback
    print(
        f"Warning: Could not extract weight for SKU {row['SKU']}. "
        f"Is price by weight: {row['Is price by weight']}, "
        f"Typical weight: {row['Typical weight']}, "
        f"Units: {row['Units']}, Supplier note: {row['Supplier note']}. "
        f"Defaulting to 0.00 lb."
    )
    return Decimal("0.00"), "lb"


def import_excel_to_db(excel_file):
    # Create single Brand and Category
    brand, _ = Brand.objects.get_or_create(name="BlueCart")
    category, _ = Category.objects.get_or_create(name="Beverage Products")

    # Read Excel file
    df = pd.read_excel(excel_file)

    # Process each row
    for index, row in df.iterrows():
        try:
            # Check for duplicate SKU
            if Product.objects.filter(sku=row["SKU"]).exists():
                print(f"Skipping duplicate SKU: {row['SKU']} at row {index + 2}")
                continue

            # Map Status to model choices
            status = str(row["Status"]).lower()
            if status not in ["enabled", "disabled", "discontinued"]:
                status = "disabled"

            # Map Taxable
            taxable = True if str(row["Taxable"]).upper() == "Y" else False

            # Handle Price with rounding to 2 decimal places
            try:
                price_value = float(row["Price"]) if pd.notna(row["Price"]) else 0.0
                price = Decimal(str(round(price_value, 2)))
            except (ValueError, TypeError, decimal.InvalidOperation):
                print(
                    f"Invalid price for SKU {row['SKU']} at row {index + 2}: {row['Price']}"
                )
                price = Decimal("0.00")

            # Handle Qty per pack
            qty_per_pack = (
                int(row["Qty per pack"]) if pd.notna(row["Qty per pack"]) else 1
            )

            # Extract weight and unit
            weight, weight_unit = extract_weight_and_unit(row)

            # Create Product instance
            product = Product(
                sku=str(row["SKU"]),
                name=str(row["Name"]) if pd.notna(row["Name"]) else "",
                weight=weight,
                weight_unit=weight_unit if pd.notna(weight_unit) else "lb",
                price=price,
                description=(
                    str(row["Description"]) if pd.notna(row["Description"]) else ""
                ),
                status=status,
                barcode=str(row["Barcode"]) if pd.notna(row["Barcode"]) else "",
                supplier_note=(
                    str(row["Supplier note"]) if pd.notna(row["Supplier note"]) else ""
                ),
                Texable=taxable,
                QtyPerPack=qty_per_pack,
                brand=brand,
            )

            # Save the product
            product.full_clean()
            product.save()
            product.category.add(category)

            print(f"Successfully imported product: {product.sku} at row {index + 2}")

        except (ValidationError, ValueError, TypeError) as e:
            print(f"Error importing SKU {row['SKU']} at row {index + 2}: {str(e)}")
            continue


if __name__ == "__main__":
    excel_file = "BlueCart Master Catalog.xlsx"
    import_excel_to_db(excel_file)
