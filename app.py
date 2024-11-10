from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Reddy%4096320@localhost:5433/amazon_app'

db = SQLAlchemy(app)


class Stud(db.Model):
    usn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(1000), nullable=False)
    sem = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    data = Stud.query.all()
    context = []
    for dt in data:
        dd = {"usn": dt.usn, "name": dt.name, "branch": dt.branch, "sem": dt.sem}
        context.append(dd)
    print(context)
    # print("data: {}".format(data))
    return render_template('stud.html', todo=context)


@app.route('/add-stud')
def add_stud():
    return render_template('add_stud.html')


@app.route('/submit', methods=['POST'])
def create_user():
    name = request.form['name']
    branch = request.form['branch']
    sem = request.form['sem']
    print(f"name is: {name}, branch is: {branch}, and sem is: {sem}")
    new_task = Stud(name=name, branch=branch, sem=sem)
    print("new_task: {}".format(new_task))
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('add_stud'))


@app.route('/delete/<int:usn>', methods=['GET', 'DELETE'])
def delete_user(usn):
    task = Stud.query.get(usn)
    print("task: {}".format(task))

    if not task:
        return jsonify({'message': 'task not found'}), 404
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the data {}'.format(e)}), 500


@app.route('/update_student/<int:usn>', methods=['GET', 'POST'])
def update_student(usn):
    task = Stud.query.get_or_404(usn)
    print(task.usn)
    if not task:
        return jsonify({'message': 'task not found'}), 404

    if request.method == 'POST':
        task.name = request.form['name']
        task.branch = request.form['branch']
        task.sem = request.form['sem']

        try:
            db.session.commit()
            return redirect(url_for('index'))

        except Exception as e:
            db.session.rollback()
            return "there is an issue while updating the record"
    return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002, debug=True)
