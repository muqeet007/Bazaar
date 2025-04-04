# Inventory Tracking System - Phase 1

## Overview

This project represents **Phase 1** of an **Inventory Tracking System** designed to track product inventory and stock movements in a single kiryana store. The system is designed to store and track the products in stock, record stock movements (in, sale, and removal), and display the current quantity of each product.

As the system expands to support multiple stores and suppliers, the design and implementation can scale to include more advanced features and support for concurrent operations.

## Assumptions

1. **Single Store Model (Phase 1):**
   - The system will initially focus on a single store, tracking product inventory and stock movements.
   - The store's data will be stored locally using **SQLite** for simplicity.

2. **Product and Stock Movement:**
   - A product can undergo three types of stock movements:
     - **IN**: Stock received or added to inventory.
     - **SALE**: Stock sold and removed from inventory.
     - **REMOVE**: Stock manually removed from inventory (e.g., damaged or expired).
   - We calculate the **current quantity** of each product based on these movements.

3. **Django and Django REST Framework:**
   - The backend is implemented using **Django** for web framework support and **Django REST Framework** (DRF) for API development.
   - The application exposes a RESTful API to interact with the product and stock movement data.

## Key Features of Phase 1

1. **Data Modeling:**
   - **Product Model:** Represents products in the inventory.
   - **Stock Movement Model:** Tracks the various movements (IN, SALE, REMOVE) for each product.

2. **Backend API:**
   - Exposes RESTful API endpoints to interact with the product and stock movement data:
     - **Products API**: CRUD operations for products.
     - **Stock Movements API**: CRUD operations for stock movements.

3. **Django Admin:**
   - Django's built-in **admin interface** is used for easy management of products and stock movements.

4. **Validation:**
   - **StockMovementSerializer** enforces that the `quantity` for stock movements must be a positive value.

## Design Decisions

1. **Product Model:**
   - **Fields:** `name` (the product name).
   - **Method `current_quantity()`:** A method to calculate the current stock of a product based on stock movements (IN, SALE, REMOVE).

2. **Stock Movement Model:**
   - **Fields:** `product`, `movement_type`, `quantity`, `timestamp`.
   - **Movement Types:** `IN`, `SALE`, and `REMOVE`, each representing a different type of stock change.
   - **Method:** A simple way to track movements in a product’s inventory.

3. **Django REST Framework:**
   - **Viewsets:** I used **ModelViewSet** for both `Product` and `StockMovement` models to generate the standard RESTful API CRUD operations.
   - **Serializers:** I used **ModelSerializer** to convert model instances into JSON and validate inputs.
   - **Read-Only Field:** The `current_quantity` field in the Product serializer is a read-only field, calculated dynamically using the `current_quantity()` method.

4. **Data Storage:**
   - I used **SQLite** for local data storage, which is simple and sufficient for Phase 1 (single store).

5. **Admin Interface:**
   - I registered the `Product` and `StockMovement` models in Django's admin interface for easy management.

## API Design

### Endpoints

#### 1. Products:
   - `GET /api/products/` - List all products.
   - `POST /api/products/` - Create a new product.
   - `GET /api/products/{id}/` - Retrieve a product by ID.
   - `PUT /api/products/{id}/` - Update a product.
   - `DELETE /api/products/{id}/` - Delete a product.

#### 2. Stock Movements:
   - `GET /api/movements/` - List all stock movements.
   - `POST /api/movements/` - Create a new stock movement.
   - `GET /api/movements/{id}/` - Retrieve a stock movement by ID.
   - `PUT /api/movements/{id}/` - Update a stock movement.
   - `DELETE /api/movements/{id}/` - Delete a stock movement.

## Example Requests

### 1. Creating a Product:
   ```json
   POST /api/products/
   {
     "name": "Product A"
   }
   ```

### 2. Creating a Stock Movement:
   ```json
   POST /api/movements/
   {
     "product": 1,
     "movement_type": "IN",
     "quantity": 100
   }
   ```

## Data Validation

- Stock movements cannot have a non-positive quantity. The `StockMovementSerializer` validates that the quantity is greater than zero.

## Evolution Rationale (v1 → v3)

### Phase 1 (Single Store Model)
   - Focus on creating a working backend with Django and Django REST Framework to manage a single store's product inventory and stock movements.  
   - Data stored locally in SQLite for simplicity.

### Phase 2 (Multiple Stores, Central Product Catalog)
   - Move to a **PostgreSQL** database to support multiple stores with a central product catalog and store-specific stock levels.  
   - Introduce **authentication** and **request throttling** to manage multiple users and API load.  
   - Add **REST API filters** to enable filtering by store and date range.

### Phase 3 (Scalable System, Real-Time Sync, Audit Logs)
   - Horizontal scalability: Move to a distributed system architecture capable of handling thousands of stores.  
   - Add **asynchronous processing** (event-driven) for real-time stock sync and handling large volumes of requests.  
   - Use **caching** strategies for performance improvement and **read/write separation**.  
   - Introduce **audit logs** for better tracking and monitoring of stock movements.

## Future Improvements (for Phase 2 and Phase 3)

1. **Scalability:** In later phases, the system should scale horizontally to handle thousands of stores, product variations, and real-time stock updates.  
2. **Security:** Phase 2 will introduce basic **authentication** (JWT/OAuth) and **authorization** to ensure only authorized users can make stock changes.  
3. **Performance Optimization:** Implement **caching**, **event-driven** architecture, and **database optimization** to ensure the system can handle high transaction volumes.  
4. **API Rate Limiting:** Implement **API rate limits** and **request throttling** to avoid abuse and protect system performance.

## Postman Testing Instructions

To test the API endpoints using Postman, follow the instructions below.

### 1. Setup Postman Environment

- Install **Postman** from [Postman Official Website](https://www.postman.com/downloads/).
- Create a **new collection** for this project in Postman.

### 2. Testing Product Endpoints

#### **Create a Product**

1. **Method**: POST  
2. **URL**: `http://127.0.0.1:8000/api/products/`  
3. **Body (JSON)**:  
   ```json
   {
     "name": "Product A"
   }
   ```  
4. **Test**: Click **Send**. The response should return the newly created product with its ID.

#### **Get All Products**

1. **Method**: GET  
2. **URL**: `http://127.0.0.1:8000/api/products/`  
3. **Test**: Click **Send**. The response should return a list of all products.

#### **Get a Product by ID**

1. **Method**: GET  
2. **URL**: `http://127.0.0.1:8000/api/products/{id}/`  
   - Replace `{id}` with the actual product ID.  
3. **Test**: Click **Send**. The response should return the product details for the specified ID.

#### **Update a Product**

1. **Method**: PUT  
2. **URL**: `http://127.0.0.1:8000/api/products/{id}/`  
   - Replace `{id}` with the actual product ID.  
3. **Body (JSON)**:  
   ```json
   {
     "name": "Updated Product"
   }
   ```  
4. **Test**: Click **Send**. The response should confirm the product was updated.

#### **Delete a Product**

1. **Method**: DELETE  
2. **URL**: `http://127.0.0.1:8000/api/products/{id}/`  
   - Replace `{id}` with the actual product ID.  
3. **Test**: Click **Send**. The response should confirm that the product has been deleted.

### 3. Testing Stock Movement Endpoints

#### **Create a Stock Movement**

1. **Method**: POST  
2. **URL**: `http://127.0.0.1:8000/api/movements/`  
3. **Body (JSON)**:  
   ```json
   {
     "product": 1,
     "movement_type": "IN",
     "quantity": 100
   }
   ```  
4. **Test**: Click **Send**. The response should return the newly created stock movement.

#### **Get All Stock Movements**

1. **Method**: GET  
2. **URL**: `http://127.0.0.1:8000/api/movements/`  
3. **Test**: Click **Send**. The response should return a list of all stock movements.

#### **Get a Stock Movement by ID**

1. **Method**: GET  
2. **URL**: `http://127.0.0.1:8000/api/movements/{id}/`  
   - Replace `{id}` with the actual stock movement ID.  
3. **Test**: Click **Send**. The response should return the details of the specified stock movement.

#### **Update a Stock Movement**

1. **Method**: PUT  
2. **URL**: `http://127.0.0.1:8000/api/movements/{id}/`  
   - Replace `{id}` with the actual stock movement ID.  
3. **Body (JSON)**:  
   ```json
   {
     "product": 1,
     "movement_type": "SALE",
     "quantity": 50
   }
   ```  
4. **Test**: Click **Send**. The response should confirm the stock movement has been updated.

#### **Delete a Stock Movement**

1. **Method**: DELETE  
2. **URL**: `http://127.0.0.1:8000/api/movements/{id}/`  
   - Replace `{id}` with the actual stock movement ID.  
3. **Test**: Click **Send**. The response should confirm that the stock movement has been deleted.

## Data Validation for Stock Movements

- **Validation Check**: Ensure that the `quantity` in stock movements is always positive.  
- When sending a request to create or update a stock movement, make sure the `quantity` is greater than zero. If not, the API will return a **400 Bad Request** error.

## Testing with Different HTTP Methods

Postman allows testing each endpoint with different HTTP methods (GET, POST, PUT, DELETE). Follow the instructions above to interact with the API using the correct method for each operation.

## Example Test Cases for Postman

### Test Case 1:
- **Action**: Create a product with name "Product A".
- **Expected Response**: A JSON response with product ID and name.

### Test Case 2:
- **Action**: Create a stock movement of type "IN" with quantity 100 for product ID 1.
- **Expected Response**: A JSON response confirming the stock movement.

### Test Case 3:
- **Action**: Update the quantity of an existing stock movement (e.g., change quantity from 100 to 50).
- **Expected Response**: A JSON response confirming the update.

### Test Case 4:
- **Action**: Delete a stock movement.
- **Expected Response**: A confirmation response stating the stock movement has been deleted.

## Author
**Syed Muqeet Ur Rehman (muqeet007)**.
 
