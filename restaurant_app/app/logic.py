from app.models import Order

def calculate_total( order: Order) -> float:
    total = sum(item.price for item in order.items)
    return total * (1 - order.discount)

def calculate_wait_time(order: Order) -> int:
    if not order.items:
        return 0
    return max(item.cooking_time for item in order.items)