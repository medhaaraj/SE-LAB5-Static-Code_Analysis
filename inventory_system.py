import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Inventory data storage
STOCK_DATA: Dict[str, int] = {}


def add_item(item: str = "default", qty: int = 0,
             logs: Optional[List[str]] = None) -> None:
    """Add an item and quantity to the inventory, with validation."""
    if logs is None:
        logs = []

    if not isinstance(item, str) or not item.strip():
        logging.error("add_item: invalid 'item' type or empty name: %r", item)
        raise ValueError("item must be a non-empty string")

    if not isinstance(qty, int) or qty < 0:
        logging.error("add_item: invalid 'qty': %r", qty)
        raise ValueError("qty must be a non-negative integer")

    STOCK_DATA[item] = STOCK_DATA.get(item, 0) + qty
    timestamp = datetime.now().isoformat()
    log_entry = f"{timestamp}: Added {qty} of {item}"
    logs.append(log_entry)
    logging.info(log_entry)


def remove_item(item: str, qty: int) -> None:
    """Remove quantity of an item if present in inventory."""
    if not isinstance(item, str) or not item.strip():
        logging.error("remove_item: invalid 'item': %r", item)
        raise ValueError("item must be a non-empty string")

    if not isinstance(qty, int) or qty <= 0:
        logging.error("remove_item: invalid 'qty': %r", qty)
        raise ValueError("qty must be a positive integer")

    if item not in STOCK_DATA:
        logging.warning("remove_item: item %s not found.", item)
        return

    current = STOCK_DATA[item]
    if current <= qty:
        del STOCK_DATA[item]
        logging.info("Removed %d of %s; item deleted.", qty, item)
    else:
        STOCK_DATA[item] = current - qty
        logging.info("Removed %dof %s;newqty=%d.", qty, item, STOCK_DATA[item])


def get_qty(item: str) -> int:
    """Return quantity of an item; 0 if not found."""
    if not isinstance(item, str) or not item.strip():
        logging.error("get_qty: invalid 'item': %r", item)
        raise ValueError("item must be a non-empty string")

    return STOCK_DATA.get(item, 0)


def load_data(file_path: str = "inventory.json") -> None:
    """Load inventory data safely from a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                logging.warning("load_data: file %s is empty.", file_path)
                STOCK_DATA.clear()
                return

            data = json.loads(content)
            if not isinstance(data, dict):
                raise ValueError("inventory file must contain a JSON object")

            STOCK_DATA.clear()
            STOCK_DATA.update(data)
            logging.info("Inventory loaded from %s", file_path)
    except FileNotFoundError:
        logging.warning("File %snot found.Startin empty inventory.", file_path)
        STOCK_DATA.clear()
    except json.JSONDecodeError as err:
        logging.error("Failed to parse JSON in %s: %s", file_path, err)
        raise


def save_data(file_path: str = "inventory.json") -> None:
    """Save inventory data to a JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(STOCK_DATA, file, indent=2, ensure_ascii=False)
        logging.info("Inventory saved to %s", file_path)
    except OSError as err:
        logging.error("Failed to write to %s: %s", file_path, err)
        raise


def print_data() -> None:
    """Log the current inventory report."""
    logging.info("Items Report:")
    for name, qty in STOCK_DATA.items():
        logging.info("%s -> %d", name, qty)


def check_low_items(threshold: int = 5) -> List[str]:
    """Return items with quantity below a given threshold."""
    if not isinstance(threshold, int) or threshold < 0:
        logging.error("check_low_items: invalid threshold: %r", threshold)
        raise ValueError("threshold must be a non-negative integer")

    return [name for name, qty in STOCK_DATA.items() if qty < threshold]


def main() -> None:
    """Main execution for inventory demo."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    try:
        add_item("apple", 10)
        add_item("banana", 2)
    except ValueError as err:
        logging.warning("main: skipping invalid add_item: %s", err)

    try:
        add_item(123, "ten")  # invalid input to test validation
    except ValueError as err:
        logging.warning("main: invalid add_item input: %s", err)

    remove_item("apple", 3)
    remove_item("orange", 1)

    logging.info("Apple stock: %d", get_qty("apple"))
    logging.info("Low items: %s", check_low_items())

    try:
        save_data()
        load_data()
        print_data()
    except Exception as err:
        logging.error("main: error during save/load: %s", err)


if __name__ == "__main__":
    main()
