from flask import Blueprint, redirect, url_for, session
from models.db import get_db_connection

subs_bp = Blueprint("subs", __name__)

@subs_bp.route("/subscribe/<int:user_id>")
def subscribe(user_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    conn = get_db_connection()
    conn.execute("INSERT INTO subscriptions (subscriber_id, target_id) VALUES (?, ?)", (session["user_id"], user_id))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@subs_bp.route("/feed")
def feed():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    conn = get_db_connection()
    posts = conn.execute(\"\"\"\n        SELECT p.* FROM posts p\n        JOIN subscriptions s ON p.user_id = s.target_id\n        WHERE s.subscriber_id=?\n    \"\"\", (session["user_id"],)).fetchall()\n    conn.close()\n    return render_template(\"index.html\", posts=posts)\n```\n\n---\n\n## 📌 app.py\n```python\nfrom flask import Flask, render_template, session\nfrom config import SECRET_KEY\nfrom models.db import get_db_connection\nfrom routes.auth import auth_bp\nfrom routes.posts import posts_bp\nfrom routes.subscriptions import subs_bp\n\napp = Flask(__name__)\napp.secret_key = SECRET_KEY\n\napp.register_blueprint(auth_bp)\napp.register_blueprint(posts_bp)\napp.register_blueprint(subs_bp)\n\n@app.route(\"/\")\ndef index():\n    conn = get_db_connection()\n    posts = conn.execute(\"SELECT p.*, u.username FROM posts p JOIN users u ON p.user_id=u.id WHERE is_public=1\").fetchall()\n    conn.close()\n    return render_template(\"index.html\", posts=posts)\n\nif __name__ == \"__main__\":\n    app.run(debug=True)\n```\n\n---\n\nТут есть всё по заданию:\n- ✅ регистрация/вход/выход\n- ✅ создание постов\n- ✅ подписки + лента\n- ✅ публичные и скрытые посты\n- ✅ редактирование/удаление постов\n- ✅ теги\n- ✅ комментарии\n\nХочешь, я сразу напишу **html-шаблоны** (base.html, index.html и т.д.) и css для стиля, или пока оставить каркас Python + SQL?
