# Inventory + Sales Analytics API System

A comprehensive backend system for managing inventory and tracking sales analytics. Built with Flask, SQLAlchemy, and SQLite.

## Features

### Product Management
- **GET /products** - Retrieve all products
- **POST /products** - Add a new product
- **PUT /products/<id>** - Update product details
- **DELETE /products/<id>** - Delete a product

### Sales Management
- **POST /sales** - Record a sale (automatically reduces stock)
- **GET /sales** - Retrieve all sales records

### Analytics Dashboard
- **GET /analytics/revenue** - Total revenue from all sales
- **GET /analytics/low-stock** - Products with low stock (≤5 units)
- **GET /analytics/top-products** - Top 5 best-selling products
- **GET /analytics/summary** - Complete analytics overview

## Tech Stack

- **Backend**: Flask 2.3.3
- **Database**: SQLite with SQLAlchemy 3.0.5
- **CORS**: Flask-CORS 4.0.0
- **Environment**: python-dotenv 1.0.0

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## Database Schema

### Products Table
- `id` (Primary Key)
- `name` (String, 100 chars)
- `price` (Float)
- `stock` (Integer)
- `created_at` (DateTime)

### Sales Table
- `id` (Primary Key)
- `product_id` (Foreign Key)
- `quantity` (Integer)
- `total` (Float)
- `timestamp` (DateTime)

## API Examples

### Add a Product
```bash
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99, "stock": 50}'
```

### Record a Sale
```bash
curl -X POST http://localhost:5000/sales \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

### Get Analytics Summary
```bash
curl http://localhost:5000/analytics/summary
```

## Sample Response Formats

### Product Response
```json
{
  "id": 1,
  "name": "Laptop",
  "price": 999.99,
  "stock": 48,
  "created_at": "2024-01-15T10:30:00.123456"
}
```

### Sale Response
```json
{
  "id": 1,
  "product_id": 1,
  "quantity": 2,
  "total": 1999.98,
  "timestamp": "2024-01-15T14:30:00.123456",
  "product_name": "Laptop"
}
```

### Analytics Summary Response
```json
{
  "total_revenue": 1999.98,
  "total_sales": 1,
  "total_products": 1,
  "low_stock_count": 0
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request` - Invalid data or missing fields
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Business Logic

- **Stock Management**: Sales automatically reduce product stock
- **Validation**: Prevents sales when insufficient stock is available
- **Analytics**: Real-time calculation of revenue and sales metrics
- **Data Integrity**: Foreign key constraints ensure data consistency

## Project Structure

```
inventory-api/
├── app.py              # Main Flask application
├── models.py           # SQLAlchemy database models
├── database.db         # SQLite database (auto-created)
├── requirements.txt    # Python dependencies
└── README.md          # This documentation
```

## Future Enhancements

- JWT authentication
- Swagger/OpenAPI documentation
- Docker containerization
- CSV export functionality
- Advanced filtering and pagination
- Real-time dashboard with charts
- Email notifications for low stock

## Contributing

This project serves as a demonstration of backend development skills including:
- REST API design
- Database modeling
- Business logic implementation
- Error handling
- Data analytics

Perfect for Python backend developer portfolios!
