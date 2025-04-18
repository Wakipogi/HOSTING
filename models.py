from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TextPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<TextPost {self.title}>'