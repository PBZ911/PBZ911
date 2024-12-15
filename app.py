from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# 数据库文件路径，这里使用相对路径，你可以根据实际情况修改
DB_FILE = 'example.db'

# 创建数据库表（如果不存在）
def create_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 插入数据到数据库的函数
def insert_data(name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

# 从数据库查询数据的函数
def query_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    conn.close()
    return data

# 根据名字查询用户数据的函数
def query_user_by_name(name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name LIKE?", ('%'+name+'%',))
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            insert_data(name)
    data = query_data()
    return render_template('index.html', users=data)

@app.route('/search_user', methods=['POST'])
def search_user_post():
    search_name = request.form.get('search_name')
    if search_name:
        data = query_user_by_name(search_name)
        return jsonify(data)
    return jsonify([])

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
