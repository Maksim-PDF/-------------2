import os
import sqlite3
from datetime import datetime
from app.models import Order

DEFAULT_DB_PATH = os.environ.get("DB_PATH", "data/orders.db")


class OrderDatabase:
    """Хранилище заказов ресторана в SQLite."""

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        # Гарантируем, что папка для файла БД существует
        directory = os.path.dirname(db_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        self._init_schema()

    # служебное
    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS orders (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_number  INTEGER NOT NULL,
                    total         REAL    NOT NULL,
                    discount      REAL    NOT NULL DEFAULT 0,
                    wait_time     INTEGER NOT NULL,
                    created_at    TEXT    NOT NULL
                );

                CREATE TABLE IF NOT EXISTS order_items (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id      INTEGER NOT NULL,
                    name          TEXT    NOT NULL,
                    price         REAL    NOT NULL,
                    cooking_time  INTEGER NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_orders_created_at
                    ON orders(created_at DESC);
                """
            )

    # публичный API
    def save_order(self, order: Order, total: float, wait_time: int) -> int:
        """Сохранить заказ и вернуть его id."""
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO orders (table_number, total, discount, wait_time, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    order.table_number,
                    total,
                    order.discount,
                    wait_time,
                    datetime.now().isoformat(timespec="seconds"),
                ),
            )
            order_id = cur.lastrowid
            conn.executemany(
                """
                INSERT INTO order_items (order_id, name, price, cooking_time)
                VALUES (?, ?, ?, ?)
                """,
                [(order_id, it.name, it.price, it.cooking_time) for it in order.items],
            )
            conn.commit()
            return order_id

    def fetch_recent(self, limit: int = 10) -> list[dict]:
        """Вернуть последние N заказов вместе с их позициями."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM orders ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
            result = []
            for row in rows:
                items = conn.execute(
                    "SELECT name, price, cooking_time FROM order_items WHERE order_id = ?",
                    (row["id"],),
                ).fetchall()
                result.append(
                    {"order": dict(row), "items": [dict(i) for i in items]}
                )
            return result