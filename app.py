from flask import Flask, render_template, request, redirect, url_for
from models import db, TextPost
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize the database
db.init_app(app)

@app.route('/')
def index():
    """Display all text posts"""
    posts = TextPost.query.all()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add_text():
    """Add a new text post"""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        new_post = TextPost(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('add_text.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_text(id):
    """Edit an existing text post"""
    post = TextPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('edit_text.html', post=post)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_text(id):
    """Delete a text post"""
    post = TextPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)