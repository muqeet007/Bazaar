# Inventory Tracker - Phase 1

A backend system for a single kiryana store to manage inventory, built for the Bazaar Tech Case Study. Uses Django and DRF to provide a REST API for products and stock movements.

## Features
- REST API for CRUD on products and stock movements.
- Real-time stock visibility with `current_quantity()`.
- Validation: `quantity > 0`, non-blank names.
- Custom Django admin with live quantities.
- SQLite for local storage.

## Setup
1. Clone: `git clone https://github.com/muqeet007/InventoryTrackerPhase1.git`
2. Virtual env: `python -m venv venv && source venv/Scripts/activate`
3. Install: `pip install -r requirements.txt`
4. Migrate: `python manage.py makemigrations && python manage.py migrate`
5. Run: `python manage.py runserver`

## API Endpoints
- `GET /api/products/` - List products.
- `POST /api/movements/` - Log a movement (e.g., `{"product": 1, "movement_type": "IN", "quantity": 50}`).

## Author
- Muqeet (muqeet007 on GitHub)