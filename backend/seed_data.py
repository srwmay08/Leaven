import requests
from datetime import date

# The URL to your local FastAPI backend
API_URL = "http://localhost:8000/api/ingredients/"

# Parsed data from your spreadsheet dump
raw_data = [
    {"name": "Almond Milk", "purchase_price": 7.88, "total_grams": 6187.97},
    {"name": "Apple Cider Vinegar", "purchase_price": 6.49, "total_grams": 907},
    {"name": "Baking Powder", "purchase_price": 7.78, "total_grams": 1247},
    {"name": "Baking Soda", "purchase_price": 8.88, "total_grams": 6124},
    {"name": "Barley Malt Syrup", "purchase_price": 11.29, "total_grams": 566},
    {"name": "Belgian Pearl Sugar", "purchase_price": 7.90, "total_grams": 225},
    {"name": "Brown Sugar", "purchase_price": 6.98, "total_grams": 3180},
    {"name": "Butter", "purchase_price": 5.19, "total_grams": 454},
    {"name": "Cabot Vintage White Cheddar", "purchase_price": 11.98, "total_grams": 907},
    {"name": "Cardamom", "purchase_price": 16.99, "total_grams": 113},
    {"name": "Cinnamon (Bulk)", "purchase_price": 5.91, "total_grams": 510},
    {"name": "Cinnamon (Jar)", "purchase_price": 7.98, "total_grams": 510},
    {"name": "Cocoa Powder", "purchase_price": 9.98, "total_grams": 652.05},
    {"name": "Cornstarch", "purchase_price": 2.49, "total_grams": 184},
    {"name": "Earth Balance Butter Tub", "purchase_price": 19.59, "total_grams": 1270},
    {"name": "Egg", "purchase_price": 9.34, "total_grams": 1200},
    {"name": "Egg Whites", "purchase_price": 12.22, "total_grams": 2724},
    {"name": "Everything Seasoning", "purchase_price": 29.49, "total_grams": 1360},
    {"name": "EVOO", "purchase_price": 21.78, "total_grams": 1820},
    {"name": "Ground Clove", "purchase_price": 7.49, "total_grams": 80},
    {"name": "Ground Ginger", "purchase_price": 5.69, "total_grams": 46},
    {"name": "Herbes de Provence", "purchase_price": 10.00, "total_grams": 226.8},
    {"name": "Honey", "purchase_price": 26.00, "total_grams": 1815},
    {"name": "Labor (Per Hour)", "purchase_price": 35.00, "total_grams": 1},
    {"name": "Maple Syrup", "purchase_price": 12.98, "total_grams": 960},
    {"name": "Molasses", "purchase_price": 4.19, "total_grams": 420},
    {"name": "Power (Per Hour)", "purchase_price": 0.36, "total_grams": 1},
    {"name": "Rye Flour", "purchase_price": 9.99, "total_grams": 1360},
    {"name": "Salt", "purchase_price": 2.18, "total_grams": 1800},
    {"name": "Semolina", "purchase_price": 11.95, "total_grams": 2268},
    {"name": "Sky Valley Sriracha", "purchase_price": 4.97, "total_grams": 524},
    {"name": "Sprinkles", "purchase_price": 19.99, "total_grams": 726},
    {"name": "Sugar", "purchase_price": 8.64, "total_grams": 4530},
    {"name": "Swedish Pearl Sugar", "purchase_price": 7.17, "total_grams": 283},
    {"name": "Vanilla", "purchase_price": 10.98, "total_grams": 227},
    {"name": "Water", "purchase_price": 0.0037, "total_grams": 3785},
    {"name": "Wheat Flour", "purchase_price": 5.85, "total_grams": 2270},
    {"name": "White Flour", "purchase_price": 9.98, "total_grams": 11340},
    {"name": "Yeast", "purchase_price": 6.18, "total_grams": 454},
]

def run_import():
    success_count = 0
    for item in raw_data:
        # We append a default date string just in case your backend expects the Ledger format
        payload = {
            "name": item["name"],
            "purchase_price": item["purchase_price"],
            "total_grams": item["total_grams"],
            "date": "2025-05-01" 
        }
        
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                print(f"✅ Imported: {item['name']}")
                success_count += 1
            else:
                print(f"❌ Failed: {item['name']} - {response.text}")
        except Exception as e:
            print(f"⚠️ Connection Error: Is your Uvicorn server running? Details: {e}")
            break

    print(f"\nImport complete! Successfully added {success_count} ingredients to the database.")

if __name__ == "__main__":
    run_import()