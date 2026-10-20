"""Read the bundled saved example; never build geometry or write user data."""
import json
from pathlib import Path

EXAMPLE_ID = 'eq-000000000004'


def example_item():
    items = json.loads((Path(__file__).resolve().parent / 'equipment-examples.json').read_text(encoding='utf-8'))
    return next(item for item in items if item['id'] == EXAMPLE_ID)
