from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# -------------------------------
# 🔹 Fetch a single product
# -------------------------------
def get_product(product_id: int):
    try:
        response = supabase.table("products").select("*").eq("id", product_id).execute()
        if not response.data:
            return None
        return response.data[0]
    except Exception as e:
        return {"error": str(e)}


# -------------------------------
# 🔹 Update stock for a product
# -------------------------------
def update_stock(product_id: int, stock: int):
    try:
        response = (
            supabase.table("products")
            .update({"stock": stock})
            .eq("id", product_id)
            .execute()
        )
        if not response.data:
            return {"error": "Update failed"}
        return response.data[0]
    except Exception as e:
        return {"error": str(e)}


# -------------------------------
# 🔹 Display all products
# -------------------------------
def display_all_products():
    try:
        response = supabase.table("products").select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        return {"error": str(e)}


# -------------------------------
# 🔹 Add new product to database
# -------------------------------
def add_product_to_db(name: str, stock: int):
    """
    Inserts a new product record into the products table.
    """
    try:
        # Example schema: id | name | stock
        response = (
            supabase.table("products")
            .insert({"name": name, "stock": stock})
            .execute()
        )

        if not response.data:
            return {"error": "Insertion failed"}
        return response.data[0]
    except Exception as e:
        return {"error": str(e)}
