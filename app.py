from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/task_manager'
mongo = PyMongo(app)

# Rotas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = mongo.db.tasks.find()
    task_list = []
    for task in tasks:
        task['_id'] = str(task['_id'])
        task_list.append(task)
    return jsonify(task_list)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data['title']
    description = data['description']
    due_date = data['due_date']
    priority = data['priority']
    task = {'title': title, 'description': description, 'due_date': due_date, 'priority': priority}
    result = mongo.db.tasks.insert_one(task)
    task['_id'] = str(result.inserted_id)
    return jsonify(task), 201

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = mongo.db.tasks.find_one_or_404({'_id': ObjectId(task_id)})
    task['_id'] = str(task['_id'])
    return jsonify(task)

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = mongo.db.tasks.find_one_or_404({'_id': ObjectId(task_id)})
    data = request.get_json()
    title = data['title']
    description = data['description']
    due_date = data['due_date']
    priority = data['priority']
    task['title'] = title
    task['description'] = description
    task['due_date'] = due_date
    task['priority'] = priority
    mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': task})
    return jsonify(task)

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    mongo.db.tasks.delete_one({'_id': ObjectId(task_id)})
    return jsonify({'message': 'Task deletada com sucesso'})

if __name__ == '__main__':
    app.run(debug=True)
