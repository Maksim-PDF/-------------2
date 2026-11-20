import pytest
from app.models import Dish, Order
from app.database import OrderDatabase


@pytest.fixture
def temp_db(tmp_path):
    return OrderDatabase(str(tmp_path / "test_orders.db"))


def test_save_order_creates_record(temp_db):
    order = Order(table_number=1)
    order.add_item(Dish("Паста", 450, 15, 300))
    order.add_item(Dish("Стейк", 1200, 25, 400))
    order.discount = 0.1

    order_id = temp_db.save_order(order, total=1485.0, wait_time=25)

    assert order_id is not None
    rows = temp_db.fetch_recent()
    assert len(rows) == 1
    assert rows[0]["order"]["table_number"] == 1
    assert rows[0]["order"]["total"] == 1485.0
    assert len(rows[0]["items"]) == 2


def test_fetch_recent_empty(temp_db):
    assert temp_db.fetch_recent() == []


def test_fetch_recent_limit(temp_db):
    for i in range(3):
        order = Order(table_number=i + 1)
        order.add_item(Dish(f"Блюдо{i}", 100, 5, 100))
        temp_db.save_order(order, total=100.0, wait_time=5)

    assert len(temp_db.fetch_recent(limit=2)) == 2