import os
from azure.cosmos import CosmosClient, PartitionKey

COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DB_NAME = os.getenv("COSMOS_DB_NAME", "cloudmart")
COSMOS_CONTAINER_PRODUCTS = "products"
COSMOS_CONTAINER_CART = "cart"
COSMOS_CONTAINER_ORDERS = "orders"

client: CosmosClient | None = None
db = None
products_container = None
cart_container = None
orders_container = None


def init_cosmos():
    global client, db, products_container, cart_container, orders_container

    if not COSMOS_ENDPOINT or not COSMOS_KEY:
        print("WARNING: Cosmos endpoint/key not set. Running in 'no-db' mode.")
        return

    client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
    db = client.create_database_if_not_exists(id=COSMOS_DB_NAME)

    products_container = db.create_container_if_not_exists(
        id=COSMOS_CONTAINER_PRODUCTS,
        partition_key=PartitionKey(path="/category"),
        offer_throughput=400,
    )

    cart_container = db.create_container_if_not_exists(
        id=COSMOS_CONTAINER_CART,
        partition_key=PartitionKey(path="/user_id"),
        offer_throughput=400,
    )

    orders_container = db.create_container_if_not_exists(
        id=COSMOS_CONTAINER_ORDERS,
        partition_key=PartitionKey(path="/user_id"),
        offer_throughput=400,
    )

    print("Cosmos DB initialized.")
