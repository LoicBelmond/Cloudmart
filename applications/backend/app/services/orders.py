from typing import List
from ..database import orders_container
from ..models import Order


def create_order(order: Order) -> Order:
    if not orders_container:
        return order
    orders_container.create_item(order.dict())
    return order


def list_orders(user_id: str) -> List[Order]:
    if not orders_container:
        return []
    items = list(
        orders_container.query_items(
            query="SELECT * FROM c WHERE c.user_id = @user_id",
            parameters=[{"name": "@user_id", "value": user_id}],
            enable_cross_partition_query=True,
        )
    )
    return [Order(**item) for item in items]
