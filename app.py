import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 连接 Render PostgreSQL 的 sakila 数据库
# 注意：DATABASE_URL 可以直接用 Render 提供的 External Database URL
# 例如：postgres://username:password@host:port/sakila
DATABASE_URL = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# 数据库表映射
class Message(db.Model):
    __tablename__ = "message"  # 显式指定表名
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # 如果表里有 created_at

# 首页路由
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_id = request.form["user_id"]
        content = request.form["content"]

        if user_id and content:
            new_msg = Message(user_id=user_id, content=content)
            db.session.add(new_msg)
            db.session.commit()

        return redirect("/")

    # 按时间倒序显示留言
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    # 本地调试用
    app.run(host="0.0.0.0", port=5000, debug=True)
