# Postman Collection Setup Guide

## 🚀 Quick Import Instructions

### 1. **Install Postman**
- Download from [https://www.postman.com](https://www.postman.com)
- Create free account

### 2. **Import Collection**
1. Open Postman
2. Click **Import** in top left
3. Select **File** tab
4. Choose `postman_collection.json` from this project
5. Click **Import**

### 3. **Start API Server**
```bash
# Make sure Flask server is running
python app.py
```

### 4. **Test the Collection**
- Click on "Inventory + Sales Analytics API" collection
- Use **Run Collection** button to test all endpoints
- Or test individual endpoints one by one

## 📋 Collection Structure

### 🏠 API Home
- `GET /` - API information and endpoints overview

### 📦 Products
- `GET /products` - Get all products
- `POST /products` - Add new product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

### 💰 Sales
- `POST /sales` - Record sale
- `GET /sales` - Get all sales

### 📊 Analytics
- `GET /analytics/revenue` - Total revenue
- `GET /analytics/low-stock` - Low stock alerts
- `GET /analytics/top-products` - Best sellers
- `GET /analytics/summary` - Complete overview

### 🧪 Error Testing
- Invalid product data
- Insufficient stock
- Non-existent resources

## 🎯 Sample Workflow

### 1. **Add Products First**
```json
POST /products
{
    "name": "Laptop",
    "price": 999.99,
    "stock": 50
}
```

### 2. **Record Sales**
```json
POST /sales
{
    "product_id": 1,
    "quantity": 2
}
```

### 3. **Check Analytics**
```bash
GET /analytics/summary
```

## 🔧 Customization Tips

### Change Base URL
1. Go to collection variables
2. Update `base_url` if your server runs elsewhere

### Modify Test Data
- Edit request bodies in each endpoint
- Change product IDs as needed
- Adjust quantities for testing

### Environment Variables (Optional)
Create environment for different servers:
- `development` - localhost:5000
- `staging` - staging-server.com
- `production` - api.yourapp.com

## 📱 Mobile Testing

Postman also has mobile apps for testing on-the-go!

## 🚨 Common Issues

### **Connection Refused**
- Make sure Flask server is running
- Check port 5000 is available

### **Invalid JSON**
- Use Postman's JSON validator
- Check for trailing commas

### **404 Errors**
- Verify URL paths
- Check server is running correct version

## 🎉 Ready to Share

Once imported, you can:
- Export collection to share with recruiters
- Generate documentation automatically
- Create team workspaces
- Schedule automated tests

This collection demonstrates professional API testing practices - perfect for your portfolio!
