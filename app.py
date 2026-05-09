from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, Product, Sale
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Home page route - serves the frontend
@app.route('/')
def home():
    return render_template('index.html')

# API info route
@app.route('/api')
def api_info():
    return jsonify({
        'message': 'Inventory + Sales Analytics API',
        'version': '1.0.0',
        'endpoints': {
            'products': '/products',
            'sales': '/sales',
            'analytics': {
                'revenue': '/analytics/revenue',
                'low_stock': '/analytics/low-stock',
                'top_products': '/analytics/top-products',
                'summary': '/analytics/summary'
            }
        },
        'documentation': 'See README.md for API usage'
    })

# Product Routes
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    
    if not data or not all(key in data for key in ['name', 'price', 'stock']):
        return jsonify({'error': 'Missing required fields: name, price, stock'}), 400
    
    try:
        product = Product(
            name=data['name'],
            price=float(data['price']),
            stock=int(data['stock'])
        )
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201
    except ValueError:
        return jsonify({'error': 'Invalid data types'}), 400

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        if 'name' in data:
            product.name = data['name']
        if 'price' in data:
            product.price = float(data['price'])
        if 'stock' in data:
            product.stock = int(data['stock'])
        
        db.session.commit()
        return jsonify(product.to_dict())
    except ValueError:
        return jsonify({'error': 'Invalid data types'}), 400

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

# Sales Routes
@app.route('/sales', methods=['POST'])
def record_sale():
    data = request.get_json()
    
    if not data or not all(key in data for key in ['product_id', 'quantity']):
        return jsonify({'error': 'Missing required fields: product_id, quantity'}), 400
    
    try:
        product_id = int(data['product_id'])
        quantity = int(data['quantity'])
        
        product = Product.query.get_or_404(product_id)
        
        if product.stock < quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        # Calculate total
        total = product.price * quantity
        
        # Update stock
        product.stock -= quantity
        
        # Create sale record
        sale = Sale(
            product_id=product_id,
            quantity=quantity,
            total=total
        )
        
        db.session.add(sale)
        db.session.commit()
        
        return jsonify(sale.to_dict()), 201
        
    except ValueError:
        return jsonify({'error': 'Invalid data types'}), 400

@app.route('/sales', methods=['GET'])
def get_sales():
    sales = Sale.query.order_by(Sale.timestamp.desc()).all()
    return jsonify([sale.to_dict() for sale in sales])

# Analytics Routes
@app.route('/analytics/revenue', methods=['GET'])
def get_revenue():
    total_revenue = db.session.query(db.func.sum(Sale.total)).scalar() or 0
    return jsonify({'total_revenue': total_revenue})

@app.route('/analytics/low-stock', methods=['GET'])
def get_low_stock():
    low_stock_products = Product.query.filter(Product.stock <= 5).all()
    return jsonify([product.to_dict() for product in low_stock_products])

@app.route('/analytics/top-products', methods=['GET'])
def get_top_products():
    top_products = db.session.query(
        Product.name,
        db.func.sum(Sale.quantity).label('total_sold'),
        db.func.sum(Sale.total).label('total_revenue')
    ).join(Sale).group_by(Product.id).order_by(db.func.sum(Sale.total).desc()).limit(5).all()
    
    return jsonify([
        {
            'name': product.name,
            'total_sold': product.total_sold,
            'total_revenue': product.total_revenue
        } for product in top_products
    ])

@app.route('/analytics/summary', methods=['GET'])
def get_analytics_summary():
    total_revenue = db.session.query(db.func.sum(Sale.total)).scalar() or 0
    total_sales = db.session.query(db.func.count(Sale.id)).scalar() or 0
    total_products = db.session.query(db.func.count(Product.id)).scalar() or 0
    low_stock_count = db.session.query(db.func.count(Product.id)).filter(Product.stock <= 5).scalar() or 0
    
    return jsonify({
        'total_revenue': total_revenue,
        'total_sales': total_sales,
        'total_products': total_products,
        'low_stock_count': low_stock_count
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
