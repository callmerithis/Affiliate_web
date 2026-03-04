from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
# Optional: Supabase client
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
load_dotenv()
app = Flask(__name__)
CORS(app)
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = None
if SUPABASE_AVAILABLE and url and key:
    supabase = create_client(url, key)
# Mocked product database as fallback
PRODUCTS = [
    {
        "id": 1,
        "name": "Wireless Noise-Canceling Headphones",
        "category": "Electronics",
        "price": 199.99,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&q=80&w=800",
        "description": "Experience premium sound with our top-rated wireless headphones. Perfect for music lovers and professionals.",
        "commission_rate": "10%",
        "affiliate_link": "https://example.com/affiliate/headphones"
    },
    {
        "id": 2,
        "name": "Smart Home Hub 2.0",
        "category": "Smart Home",
        "price": 129.50,
        "image": "https://images.unsplash.com/photo-1558089687-f282ffcbc126?auto=format&fit=crop&q=80&w=800",
        "description": "Connect and control all your smart devices from one central hub with seamless voice integration.",
        "commission_rate": "8%",
        "affiliate_link": "https://example.com/affiliate/smarthub"
    },
    {
        "id": 3,
        "name": "Ergonomic Office Chair",
        "category": "Furniture",
        "price": 249.00,
        "image": "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?auto=format&fit=crop&q=80&w=800",
        "description": "Improve your posture and productivity with this premium ergonomic chair designed for long hours.",
        "commission_rate": "12%",
        "affiliate_link": "https://example.com/affiliate/chair"
    },
    {
        "id": 4,
        "name": "Minimalist Smartwatch",
        "category": "Wearables",
        "price": 149.99,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&q=80&w=800",
        "description": "Track your fitness and stay connected with this sleek, modern smartwatch that goes with any outfit.",
        "commission_rate": "15%",
        "affiliate_link": "https://example.com/affiliate/smartwatch"
    },
    {
        "id": 5,
        "name": "Professional Camera Lens",
        "category": "Photography",
        "price": 599.00,
        "image": "https://images.unsplash.com/photo-1616423640778-28d1b53229bd?auto=format&fit=crop&q=80&w=800",
        "description": "Capture breathtaking photos with this high-quality prime lens. Ideal for portraits and landscapes.",
        "commission_rate": "5%",
        "affiliate_link": "https://example.com/affiliate/camera-lens"
    },
    {
        "id": 6,
        "name": "Premium Yoga Mat",
        "category": "Fitness",
        "price": 45.00,
        "image": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?auto=format&fit=crop&q=80&w=800",
        "description": "Eco-friendly, non-slip yoga mat providing perfect cushioning for your daily practice.",
        "commission_rate": "20%",
        "affiliate_link": "https://example.com/affiliate/yogamat"
    }
]
@app.route('/api/products', methods=['GET'])
def get_products():
    if supabase:
        try:
            response = supabase.table('products').select('*').execute()
            return jsonify(response.data)
        except Exception as e:
            print(f"Error fetching from Supabase: {e}")
            # Fallback to mock data on error
            return jsonify(PRODUCTS)
    
    return jsonify(PRODUCTS)
@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    if supabase:
        try:
            response = supabase.table('products').select('*').eq('id', product_id).execute()
            if response.data and len(response.data) > 0:
                return jsonify(response.data[0])
        except Exception as e:
            print(f"Error fetching from Supabase: {e}")
    # Fallback to mock data
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404
if __name__ == '__main__':
    app.run(debug=True, port=5000)