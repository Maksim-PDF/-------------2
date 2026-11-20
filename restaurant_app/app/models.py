from abc import ABC, abstractmethod

# Абстрактный базовый класс
class MenuItem(ABC):
    def __init__(self, name: str, price: float, cooking_time: int):
        self.name = name
        self.price = price
        self.cooking_time = cooking_time

    @abstractmethod
    def get_info(self):
        pass

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"

# Наследование
class Dish(MenuItem):
    def __init__(self, name: str, price: float, cooking_time: int, weight: int):
        super().__init__(name, price, cooking_time)
        self.weight = weight

    def get_info(self):
        return f"Блюдо: {self.name}, Вес: {self.weight}г, Время: {self.cooking_time} мин."

# Managed-атрибут
class Order:
    def __init__(self, table_number: int):
        self.table_number = table_number
        self.items = []
        self._discount = 0.0    

    def add_item(self, item: MenuItem):
        self.items.append(item)

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value: float):
        if not(0 <= value <= 0.5):
            raise ValueError("Скидка не входит предполагаемый диапазон")
        self._discount = value

     # Dunder-метод
    def __len__(self):
        return len(self.items)

    def __str__(self):
        return f"Закакз для столика {self.table_number}. Позиция: {len(self.items)}"