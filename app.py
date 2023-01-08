import os

from bson.objectid import ObjectId
from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient

app = Flask(__name__)

username = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]

client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.wjacgwr.mongodb.net/?retryWrites=true&w=majority")

db = client.flask_db
todos = db.todos


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        todos.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('index'))
    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)


@app.post('/<id_>/delete/')
def delete(id_):
    todos.delete_one({"_id": ObjectId(id_)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
