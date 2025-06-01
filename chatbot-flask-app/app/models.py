from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PDFData(db.Model):
    __tablename__ = 'pdf_data'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    embedding = db.Column(db.PickleType, nullable=False)  # Store embeddings as binary data

class ChatbotResponse(db.Model):
    __tablename__ = 'chatbot_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(255), nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Timestamp for when the response was created