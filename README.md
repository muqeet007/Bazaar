# Phase 2 Inventory Tracker

A robust inventory management system built with Django REST Framework, designed for efficient stock tracking and management.

## Overview

This project implements a comprehensive inventory tracking system that enables real-time monitoring of product stock levels, movement history, and automated quantity updates. The system is built with scalability in mind while maintaining simplicity in its core functionality.

## Requirements

### Core Objectives
- Develop an inventory tracking system for a single store
- Track product stock movements (stock in, sales, manual removal)
- Maintain accurate current quantity for each product
- Provide simple API interface for inventory management
- Store data locally using SQLite database

### Key Assumptions
- Single store inventory management
- Three types of stock movements:
  - Stock In (IN): Adding new inventory
  - Sales (SALE): Product sold to customers
  - Manual Removal (REMOVE): Damaged/lost items
- Local data storage is sufficient
- Basic authentication for API access
- Real-time quantity tracking required

## Technical Implementation

### Data Models

#### Store
- Name (unique identifier)
- Location
- Creation timestamp

#### Product
- Name
- Description
- Price
- Current stock quantity
- Store reference
- Creation and update timestamps

#### StockMovement
- Product reference
- Movement type (STOCK_IN, SALE, MANUAL_REMOVAL)
- Quantity (positive for stock-in, negative for sales/removals)
- Creation timestamp

### Features

#### Real-time Stock Management
- Automatic quantity updates via Django signals
- Validation to prevent negative stock quantities
- Real-time stock level tracking

#### API Endpoints
- Products:
  - CRUD operations
  - Stock movement endpoints:
    - `/products/{id}/stock_in/`
    - `/products/{id}/sell/`
    - `/products/{id}/remove/`
- Stock Movements:
  - Movement history
  - Filtering by date range and store

#### Security
- Basic authentication required for all endpoints
- Data validation at model and API levels
- Protected admin interface

### Technology Stack
- Django REST Framework
- SQLite Database
- Django Admin Interface
- Django Signals for automated updates

## API Documentation

### Authentication
All endpoints require basic authentication. Include credentials in the request header:
```
Authorization: Basic <base64-encoded-credentials>
```

### Endpoints

#### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create new product
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product

#### Stock Movements
- `POST /api/products/{id}/stock_in/` - Add stock
  ```json
  {
    "quantity": 10
  }
  ```
- `POST /api/products/{id}/sell/` - Record sale
  ```json
  {
    "quantity": 5
  }
  ```
- `POST /api/products/{id}/remove/` - Manual removal
  ```json
  {
    "quantity": 2
  }
  ```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Development

### Project Structure
```
inventory/
├── stock/
│   ├── models.py      # Data models
│   ├── views.py       # API endpoints
│   ├── serializers.py # Data serialization
│   ├── signals.py     # Automated updates
│   └── urls.py        # URL routing
└── inventory/
    ├── settings.py    # Project settings
    └── urls.py        # Main URL configuration
```

### Key Components
- Models handle data structure and validation
- Signals automate stock quantity updates
- Viewsets provide RESTful API endpoints
- Serializers handle data transformation

## Testing
Run tests using:
```bash
python manage.py test
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License.

## Author
Syed Muqeet Ur Rehman (muqeet007)
