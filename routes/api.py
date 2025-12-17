from flask import Blueprint, request, send_file
from models import db, User
from PIL import Image
import requests
import io

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/optimize', methods=['POST'])
def optimize():
    api_key = request.form.get('api_key')
    image_url = request.form.get('image_url')
    quality = request.form.get('quality', 80) # Default 80
    
    if not api_key or not image_url:
        return "Missing api_key or image_url", 400
        
    user = User.query.filter_by(api_key=api_key).first()
    
    if not user:
        return "Invalid API Key", 401
        
    if not user.is_approved:
        return "Account not approved", 403
        
    if not user.has_quota():
        return "Quota exceeded", 403
        
    try:
        # Download Image
        resp = requests.get(image_url, stream=True)
        resp.raise_for_status()
        
        # Process Image
        img = Image.open(resp.raw)
        output = io.BytesIO()
        
        # Convert to WebP
        img.save(output, format='WEBP', quality=float(quality))
        output.seek(0)
        
        user.increment_usage()
        
        return send_file(output, mimetype='image/webp')
        
    except Exception as e:
        return f"Error processing image: {str(e)}", 500
