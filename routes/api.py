from flask import Blueprint, request, send_file
from models import db, User
from PIL import Image
import requests
import io
import base64

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/optimize', methods=['POST'])
def optimize():
    api_key = request.form.get('api_key')
    quality = request.form.get('quality', 80)
    
    # Support both URL and direct upload (base64)
    image_url = request.form.get('image_url')
    image_data = request.form.get('image_data')
    
    if not api_key:
        return "Missing api_key", 400
        
    if not image_url and not image_data:
        return "Missing image_url or image_data", 400
        
    user = User.query.filter_by(api_key=api_key).first()
    
    if not user:
        return "Invalid API Key", 401
        
    if not user.is_approved:
        return "Account not approved", 403
        
    if not user.has_quota():
        return "Quota exceeded", 403
        
    try:
        if image_data:
            # Direct upload - decode base64
            img_bytes = base64.b64decode(image_data)
            img = Image.open(io.BytesIO(img_bytes))
        else:
            # URL method (may fail on PythonAnywhere free tier due to proxy)
            resp = requests.get(image_url, stream=True, timeout=30)
            resp.raise_for_status()
            img = Image.open(resp.raw)
        
        # Convert to RGB if necessary (for PNG with transparency)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        output = io.BytesIO()
        img.save(output, format='WEBP', quality=int(quality))
        output.seek(0)
        
        user.increment_usage()
        
        return send_file(output, mimetype='image/webp')
        
    except Exception as e:
        return f"Error processing image: {str(e)}", 500
