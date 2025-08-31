import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Render 提供的 DATABASE_URL 环境变量
DATABASE_URL = os.environ.get("DATABASE_URL")

# SQLAlchemy 配置
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# 数据库表
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)

# 首页
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

    messages = Message.query.order_by(Message.id.desc()).all()
    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    # 本地调试用
    app.run(host="0.0.0.0", port=5000, debug=True)
