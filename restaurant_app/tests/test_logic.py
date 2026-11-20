import pytest
from app.models import Dish, Order
from app.logic import calculate_total, calculate_wait_time

# Тест 1: Проверка правильности подсчета суммы без скидки
def test_calculate_total_no_discount():
    order = Order(table_number=1)
    order.add_item(Dish("Паста", 450, 15, 300))
    order.add_item(Dish("Стейк", 1200, 25, 400))
    # 450 + 1200 = 1650
    assert calculate_total(order) == 1650.0

# Тест 2: Проверка подсчета суммы со скидкой
def test_calculate_total_with_discount():
    order = Order(table_number=2)
    order.add_item(Dish("Паста", 1000, 15, 300))
    order.discount = 0.1  # Скидка 10%
    # 1000 - 10% = 900
    assert calculate_total(order) == 900.0

# Тест 3: Проверка времени ожидания
def test_calculate_wait_time():
    order = Order(table_number=3)
    order.add_item(Dish("Салат", 300, 10, 200))
    order.add_item(Dish("Стейк", 1200, 25, 400)) # Стейк готовится дольше всех
    assert calculate_wait_time(order) == 25

# Тест 4: Проверка защиты данных (Managed-атрибут)
# Мы пытаемся скидку 80%, а программа должна выдать ошибку
def test_discount_validation():
    order = Order(table_number=4)
    with pytest.raises(ValueError):
        order.discount = 0.8