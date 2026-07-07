from app import app
from services.import_service import ImportService


with app.app_context():

    print("=" * 50)
    print("ALASKAN SALES™ Database Seeding")
    print("=" * 50)

    print("\nImporting Suppliers...")
    print(
        ImportService.import_suppliers(
            "ALASKAN/ALASKAN.xlsx"
        )
    )

    print("\nImporting Products...")
    print(
        ImportService.import_products(
            "PRODUCT_MASTER/RECEIPT-X_PRODUCT_MASTER.xlsx"
        )
    )

    print("\nDatabase seeding complete.")