from flask import Blueprint, render_template, request, redirect, url_for, session
from models.db import get_db_connection

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("/create", methods=["GET", "POST"])
def create_post():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        tags = request.form["tags"]
        is_public = 1 if request.form.get("is_public") else 0
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO posts (user_id, title, content, is_public, tags) VALUES (?, ?, ?, ?, ?)",
            (session["user_id"], title, content, is_public, tags)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("create_post.html")

@posts_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def post(post_id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id=?", (post_id,)).fetchone()
    comments = conn.execute("SELECT c.content, u.username FROM comments c JOIN users u ON c.user_id=u.id WHERE c.post_id=?", (post_id,)).fetchall()
    conn.close()
    if request.method == "POST" and "user_id" in session:
        content = request.form["content"]
        conn = get_db_connection()
        conn.execute("INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)", (post_id, session["user_id"], content))
        conn.commit()
        conn.close()
        return redirect(url_for("posts.post", post_id=post_id))
    return render_template("post.html", post=post, comments=comments)

@posts_bp.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id=?", (post_id,)).fetchone()
    conn.close()
    if "user_id" not in session or post["user_id"] != session["user_id"]:
        return redirect(url_for("index"))
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        tags = request.form["tags"]
        conn = get_db_connection()
        conn.execute("UPDATE posts SET title=?, content=?, tags=? WHERE id=?", (title, content, tags, post_id))
        conn.commit()
        conn.close()
        return redirect(url_for("posts.post", post_id=post_id))
    return render_template("edit_post.html", post=post)

@posts_bp.route("/delete/<int:post_id>")
def delete_post(post_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE id=?", (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))
