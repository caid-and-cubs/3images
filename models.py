from app import db
from datetime import datetime

class GeneratedImage(db.Model):
    """Model for storing generated images"""
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<GeneratedImage {self.id}: {self.prompt[:50]}...>'
