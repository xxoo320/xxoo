import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 连接 sakila 数据库
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")  # 或直接写URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# 映射 message 表
class Message(db.Model):
    __tablename__ = "message"  # 显式指定表名
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # 自动记录时间

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        content = request.form.get("content")

        if user_id and content:
            new_msg = Message(user_id=user_id, content=content)
            db.session.add(new_msg)
            db.session.commit()
            print(f"留言已提交: {user_id} - {content}")  # 调试用

        return redirect("/")

    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
