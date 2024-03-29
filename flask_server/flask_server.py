import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

# creating a Flask app 
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
ma = Marshmallow(app)


# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# https://docs.sqlalchemy.org/en/13/core/constraints.html#unique-constraint
# https://www.w3schools.com/sql/sql_unique.asp
class User(db.Model):
    __table_name__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True, nullable=False)  # the name of the users is unique
    password = db.Column(db.String(32), nullable=False)
    ip = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return 'id:{} name:{} ip:{}'.format(self.id, self.name, self.ip)  # omit password


class UserSchema(ma.Schema):
    class Meta:
        fields = ('name', 'password', 'ip')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Call(db.Model):  # call other side
    __table_name__ = 'Call'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    src = db.Column(db.String(32), unique=True, nullable=False)  # the name of the src caller is unique
    operation = db.Column(db.String(32), nullable=False)
    dst = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return 'id:{} src:{} operation:{} dst:{}'.format(self.id, self.src, self.operation, self.dst)


class CallSchema(ma.Schema):
    class Meta:
        fields = ('src', 'operation', 'dst')


call_schema = CallSchema()
calls_schema = CallSchema(many=True)


@app.route('/user_list')
def user_list():
    if request.method == 'GET':
        results = db.session.query(User.name).all()
        user_names = [u.name for u in results]
        return jsonify(user_names)


@app.route('/get_ip', methods=['GET'])
def get_ip():
    if request.method == 'GET':
        user_name = request.form.get("name")
        result = ""
        user_info = User.query.filter_by(name=user_name).first()
        if user_info:
            result = user_info.ip
        print('sending:', result)
        return jsonify(result)


@app.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        user_name = request.form.get("name")
        password = request.form.get("password")
        result = 'False'
        user_info = User.query.filter_by(name=user_name, password=password).first()
        if user_info:
            print(user_info.name, user_info.ip)
            result = "True"
        print(f'sending {result}')
        return jsonify(result)


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # data = request.form
        # print(data)
        user_name = request.form.get("name")
        password = request.form.get("password")
        ip = request.remote_addr
        result = 'False'
        user_info = User.query.filter_by(name=user_name).first()
        # check if name already exist
        if not user_info:
            new_user = User(name=user_name, password=password, ip=ip)
            db.session.add(new_user)
            db.session.commit()
            print("new user:", new_user.id, user_name, password, ip)
            result = "True"
        print(f'sending {result}')
        return jsonify(result)


@app.route('/accept', methods=['PUT'])
def accept():
    if request.method == 'PUT':
        dst = request.form.get("dst")
        src = request.form.get("src")
        op = request.form.get("operation")
        result = ""
        row = Call.query.filter_by(dst=dst, src=src).first()
        if row:
            if row.operation == 'calling':
                row.operation = op
                db.session.commit()
                result = 'True'
        print(f'sending {result}')
        return jsonify(result)


@app.route('/stop', methods=['DELETE'])
def stop():
    if request.method == 'DELETE':
        name = request.form.get("name")
        op = request.form.get("operation")
        result = "empty"

        if op == 'calling':
            row = Call.query.filter_by(src=name).first()
            if not row:
                row = Call.query.filter_by(dst=name).first()
            if row:
                db.session.delete(row)
                db.session.commit()
                result = 'calling stopped'
        else:  # call
            row = Call.query.filter_by(src=name).first()
            if not row:
                row = Call.query.filter_by(dst=name).first()
            if row:
                db.session.delete(row)
                db.session.commit()
                result = 'call stopped'
        print('sending:', result)
        return jsonify(result)


@app.route('/call', methods=['POST'])
def call():
    if request.method == 'POST':
        src = request.form.get("src")
        operation = request.form.get("operation")
        dst = request.form.get("dst")
        result = 'call already exists'
        raw = Call.query.filter_by(src=src).first()
        if not raw:
            new_call = Call(src=src, operation=operation, dst=dst)
            db.session.add(new_call)
            db.session.commit()
            print("new_call:", new_call.id, src, operation, dst)
            result = "True"
        print('sending:', result)
        return jsonify(result)


@app.route('/check', methods=['GET'])
def check_connection():
    if request.method == 'GET':
        dst = request.form.get("dst")
        src = request.form.get("src")
        name = request.form.get("name")
        result = ""

        # check if not rejected
        if dst and src:
            data = Call.query.filter_by(dst=dst, src=src).first()
            if data:
                result = True  # not rejected

        # check if in chat
        elif name:
            data = Call.query.filter_by(dst=name, operation='call').first()
            if not data:
                data = Call.query.filter_by(src=name, operation='call').first()
            if data:
                result = True

        # check if being called; 'calling'
        elif dst and not src:
            row = Call.query.filter_by(dst=dst).first()
            if row:
                result = row.src
        # print('sending:', result)
        return jsonify(result)


if __name__ == '__main__':
    # db.create_all(app=app)
    import socket
    name = socket.gethostname()
    print(f'hostname : {name}')
    ip = socket.gethostbyname(name)
    print(f'server started\nIP : {ip}')
    app.run(debug=True, host='0.0.0.0', port=5000)
