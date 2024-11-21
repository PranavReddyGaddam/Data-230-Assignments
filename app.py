from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()

    # Calculate wins and losses
    wins = sum(1 for post in posts if post['result'] == 'Win')
    losses = sum(1 for post in posts if post['result'] == 'Loss')

    return render_template('index.html', posts=posts, wins=wins, losses=losses)

@app.route('/post/<int:post_id>')
def post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        return "Post not found", 404
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        result = request.form['result']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content, result) VALUES (?, ?, ?)',
                         (title, content, result))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:post_id>/edit', methods=('GET', 'POST'))
def edit(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        result = request.form['result']

        if not title:
            flash('Title is required!')
        else:
            conn.execute('UPDATE posts SET title = ?, content = ?, result = ? WHERE id = ?',
                         (title, content, result, post_id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', post=post)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
