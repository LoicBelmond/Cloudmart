from typing import List
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from ..database import products_container
from ..models import Product


def get_all_products(category: str | None = None) -> List[Product]:
    if not products_container:
        # Fallback dummy data if Cosmos not configured
        sample = [
            Product(id="1", name="Sample Laptop", category="Electronics", price=999.99),
            Product(id="2", name="Sample Phone", category="Electronics", price=699.99),
            Product(id="3", name="Sample Shoes", category="Fashion", price=89.99),
        ]
        if category:
            return [p for p in sample if p.category == category]
        return sample

    query = "SELECT * FROM c"
    params = []
    if category:
        query += " WHERE c.category = @category"
        params.append({"name": "@category", "value": category})

    items = list(products_container.query_items(
        query=query,
        parameters=params,
        enable_cross_partition_query=True
    ))
    return [Product(**item) for item in items]


def get_product(product_id: str) -> Product | None:
    if not products_container:
        return None

    try:
        item = products_container.read_item(item=product_id, partition_key="Electronics")
        return Product(**item)
    except CosmosResourceNotFoundError:
        return None
