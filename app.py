import os
import logging
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
import requests
from urllib.parse import urlparse
import tempfile
import uuid

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///image_generator.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models
    import models
    db.create_all()

from openai_service import generate_image_with_dalle

@app.route('/')
def index():
    """Main page with image generation form"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    """Generate image from text prompt"""
    try:
        prompt = request.form.get('prompt', '').strip()
        
        if not prompt:
            flash('Please enter a text prompt', 'error')
            return redirect(url_for('index'))
        
        if len(prompt) > 1000:
            flash('Prompt is too long. Please keep it under 1000 characters.', 'error')
            return redirect(url_for('index'))
        
        # Generate image using OpenAI DALL-E
        app.logger.info(f"Generating image for prompt: {prompt}")
        result = generate_image_with_dalle(prompt)
        
        if 'error' in result:
            flash(f'Error generating image: {result["error"]}', 'error')
            return redirect(url_for('index'))
        
        # Save to database
        from models import GeneratedImage
        new_image = GeneratedImage(
            prompt=prompt,
            image_url=result['url'],
            created_at=datetime.utcnow()
        )
        db.session.add(new_image)
        db.session.commit()
        
        flash('Image generated successfully!', 'success')
        return render_template('index.html', 
                             generated_image=result['url'], 
                             prompt=prompt,
                             image_id=new_image.id)
        
    except Exception as e:
        app.logger.error(f"Error in generate_image: {str(e)}")
        flash('An unexpected error occurred. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/gallery')
def gallery():
    """Display gallery of generated images"""
    try:
        from models import GeneratedImage
        images = GeneratedImage.query.order_by(GeneratedImage.created_at.desc()).limit(50).all()
        return render_template('gallery.html', images=images)
    except Exception as e:
        app.logger.error(f"Error in gallery: {str(e)}")
        flash('Error loading gallery', 'error')
        return redirect(url_for('index'))

@app.route('/download/<int:image_id>')
def download_image(image_id):
    """Download generated image"""
    try:
        from models import GeneratedImage
        image = GeneratedImage.query.get_or_404(image_id)
        
        # Download image from URL
        response = requests.get(image.image_url, timeout=30)
        response.raise_for_status()
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_file.write(response.content)
        temp_file.close()
        
        # Generate filename
        safe_prompt = "".join(c for c in image.prompt[:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_prompt}_{image.id}.png"
        
        return send_file(temp_file.name, 
                        as_attachment=True, 
                        download_name=filename,
                        mimetype='image/png')
        
    except Exception as e:
        app.logger.error(f"Error downloading image {image_id}: {str(e)}")
        flash('Error downloading image', 'error')
        return redirect(url_for('gallery'))

@app.route('/delete/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    """Delete generated image from gallery"""
    try:
        from models import GeneratedImage
        image = GeneratedImage.query.get_or_404(image_id)
        db.session.delete(image)
        db.session.commit()
        flash('Image deleted successfully', 'success')
    except Exception as e:
        app.logger.error(f"Error deleting image {image_id}: {str(e)}")
        flash('Error deleting image', 'error')
    
    return redirect(url_for('gallery'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('index.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
