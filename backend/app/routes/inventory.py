from fastapi import APIRouter, HTTPException
from database import (
    get_product,
    update_stock,
    display_all_products,
    add_product_to_db,
)
from redis_pubsub import publish_update

router = APIRouter(prefix="/inventory", tags=["Inventory"])


# -------------------------------
# 🔹 Update product stock
# -------------------------------
@router.post("/update-stock/{product_id}")
def update_stock_endpoint(product_id: int, stock: int):
    """
    Update stock quantity for a given product ID and publish the change to Redis.
    """
    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    updated = update_stock(product_id, stock)
    if "error" in updated:
        raise HTTPException(status_code=500, detail=updated["error"])

    # Publish to Redis for real-time sync across instances
    publish_update(product_id, stock)

    return {"message": "✅ Stock updated successfully", "product": updated}


# -------------------------------
# 🔹 Display all products
# -------------------------------
@router.get("/all")
def display_products():
    """
    Retrieve all products from Supabase.
    """
    products = display_all_products()
    if isinstance(products, dict) and "error" in products:
        raise HTTPException(status_code=500, detail=products["error"])

    if not products:
        raise HTTPException(status_code=404, detail="No products found in the database")

    return {"count": len(products), "products": products}


# -------------------------------
# 🔹 Add a new product
# -------------------------------
@router.post("/add-product/{name}/{stock}")
def add_product(name: str, stock: int):
    """
    Add a new product to Supabase and publish to Redis for real-time sync.
    """
    try:
        # Add to Supabase
        new_product = add_product_to_db(name, stock)
        if "error" in new_product:
            raise Exception(new_product["error"])

        # Notify Redis subscribers
        publish_update(product_id=new_product["id"], stock=stock)

        return {
            "message": "✅ Product added successfully",
            "product": new_product
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# 🔹 Get a single product
# -------------------------------
@router.get("/product/{product_id}")
def get_single_product(product_id: int):
    """
    Retrieve a specific product by ID.
    """
    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"product": product}
