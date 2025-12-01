from typing import List
from ..database import cart_container
from ..models import CartItem


def get_cart(user_id: str) -> List[CartItem]:
    if not cart_container:
        return []

    items = list(
        cart_container.query_items(
            query="SELECT * FROM c WHERE c.user_id = @user_id",
            parameters=[{"name": "@user_id", "value": user_id}],
            enable_cross_partition_query=True,
        )
    )
    return [CartItem(**item) for item in items]


def add_to_cart(item: CartItem) -> CartItem:
    if not cart_container:
        return item
    cart_container.create_item(item.dict())
    return item


def remove_from_cart(user_id: str, item_id: str) -> None:
    if not cart_container:
        return
    cart_container.delete_item(item=item_id, partition_key=user_id)
