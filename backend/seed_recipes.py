# backend/seed_recipes.py
import requests

API_URL = "http://localhost:8000/api/recipes/"

recipes_data = [
    {"name": "Sandwich Bread", "yield_qty": 4, "ingredients": [{"name": "EVOO", "grams": 20}, {"name": "Salt", "grams": 40}, {"name": "Water", "grams": 1400}, {"name": "White Flour", "grams": 1610}, {"name": "Yeast", "grams": 7}]},
    {"name": "Everything (Yield 4)", "yield_qty": 4, "ingredients": [{"name": "Everything Seasoning", "grams": 20}, {"name": "EVOO", "grams": 20}, {"name": "Salt", "grams": 40}, {"name": "Water", "grams": 1400}, {"name": "White Flour", "grams": 1610}, {"name": "Yeast", "grams": 7}]},
    {"name": "Cinnamon Cardamom", "yield_qty": 4, "ingredients": [{"name": "Cardamom", "grams": 2}, {"name": "Cinnamon", "grams": 20}, {"name": "EVOO", "grams": 20}, {"name": "Salt", "grams": 40}, {"name": "Sugar", "grams": 200}, {"name": "Swedish Pearl Sugar", "grams": 20}, {"name": "Water", "grams": 1400}, {"name": "White Flour", "grams": 1610}, {"name": "Yeast", "grams": 7}]},
    {"name": "Herbes & Cheddar", "yield_qty": 4, "ingredients": [{"name": "Cabot Vintage White Cheddar", "grams": 440}, {"name": "EVOO", "grams": 20}, {"name": "Herbes de Provence", "grams": 3}, {"name": "Salt", "grams": 40}, {"name": "Water", "grams": 1400}, {"name": "White Flour", "grams": 1610}, {"name": "Yeast", "grams": 7}]},
    {"name": "Sriracha & Cheddar", "yield_qty": 4, "ingredients": [{"name": "Cabot Vintage White Cheddar", "grams": 440}, {"name": "EVOO", "grams": 20}, {"name": "Salt", "grams": 40}, {"name": "Sriracha", "grams": 200}, {"name": "Water", "grams": 1400}, {"name": "White Flour", "grams": 1610}, {"name": "Yeast", "grams": 7}]},
    {"name": "Submarine Roll", "yield_qty": 8, "ingredients": [{"name": "EVOO", "grams": 20}, {"name": "Salt", "grams": 40}, {"name": "Water", "grams": 1250}, {"name": "White Flour", "grams": 1920}, {"name": "Yeast", "grams": 10}]},
    {"name": "Bread Bowls", "yield_qty": 9, "ingredients": [{"name": "EVOO", "grams": 20}, {"name": "Salt", "grams": 40}, {"name": "Water", "grams": 1250}, {"name": "White Flour", "grams": 1920}, {"name": "Yeast", "grams": 10}]},
    {"name": "H&C Hand", "yield_qty": 16, "ingredients": [{"name": "Cabot Vintage White Cheddar", "grams": 880}, {"name": "EVOO", "grams": 20}, {"name": "Herbes de Provence", "grams": 6}, {"name": "Salt", "grams": 40}, {"name": "Water", "grams": 1250}, {"name": "White Flour", "grams": 1920}, {"name": "Yeast", "grams": 10}]},
    {"name": "S&C Hand", "yield_qty": 16, "ingredients": [{"name": "Cabot Vintage White Cheddar", "grams": 880}, {"name": "EVOO", "grams": 20}, {"name": "Salt", "grams": 40}, {"name": "Sriracha", "grams": 400}, {"name": "Water", "grams": 1250}, {"name": "White Flour", "grams": 1920}, {"name": "Yeast", "grams": 10}]},
    {"name": "C&C Hand", "yield_qty": 16, "ingredients": [{"name": "Cardamom", "grams": 2}, {"name": "Cinnamon", "grams": 25}, {"name": "EVOO", "grams": 20}, {"name": "Salt", "grams": 40}, {"name": "Sugar", "grams": 250}, {"name": "Swedish Pearl Sugar", "grams": 50}, {"name": "Water", "grams": 1250}, {"name": "White Flour", "grams": 1920}, {"name": "Yeast", "grams": 10}]},
    {"name": "Everything (Yield 16)", "yield_qty": 16, "ingredients": [{"name": "Everything Seasoning", "grams": 20}, {"name": "EVOO", "grams": 20}, {"name": "Salt", "grams": 40}, {"name": "Water", "grams": 1250}, {"name": "White Flour", "grams": 1920}, {"name": "Yeast", "grams": 10}]},
    {"name": "Caakies", "yield_qty": 28, "ingredients": [{"name": "Almond Extract", "grams": 30}, {"name": "Baking Powder", "grams": 50}, {"name": "Baking Soda", "grams": 56}, {"name": "Brown Sugar", "grams": 110}, {"name": "Cocoa Powder", "grams": 15}, {"name": "Cornstarch", "grams": 20}, {"name": "Earth Balance Butter", "grams": 227}, {"name": "Eggs", "grams": 165}, {"name": "Salt", "grams": 6}, {"name": "Sprinkles", "grams": 30}, {"name": "Sugar", "grams": 279}, {"name": "Vanilla Extract", "grams": 3}, {"name": "White Flour", "grams": 508}]},
    {"name": "Chewy Ginger", "yield_qty": 17, "ingredients": [{"name": "Earth Balance Butter", "grams": 140}, {"name": "Eggs", "grams": 55}, {"name": "Ground Clove", "grams": 0.5}, {"name": "Ground Ginger", "grams": 6}, {"name": "Molasses", "grams": 80}, {"name": "Salt", "grams": 3}, {"name": "Sugar", "grams": 165}, {"name": "Vanilla Extract", "grams": 2.5}, {"name": "White Flour", "grams": 284}]},
    {"name": "Rye Bread", "yield_qty": 2, "ingredients": [{"name": "EVOO", "grams": 20}, {"name": "Molasses", "grams": 40}, {"name": "Rye Flour", "grams": 200}, {"name": "Salt", "grams": 20}, {"name": "Water", "grams": 1000}, {"name": "White Flour", "grams": 850}, {"name": "Yeast", "grams": 20}]}
]

def run_import():
    success_count = 0
    for recipe in recipes_data:
        try:
            response = requests.post(API_URL, json=recipe)
            if response.status_code == 200:
                print(f"✅ Imported: {recipe['name']}")
                success_count += 1
            else:
                print(f"❌ Failed: {recipe['name']} - {response.text}")
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")
            break

    print(f"\nImport complete! Added {success_count} recipes.")

if __name__ == "__main__":
    run_import()