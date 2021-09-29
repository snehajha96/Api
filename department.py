from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, abort, marshal_with
# import argparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:sneha@localhost:5432/flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

emp_args = reqparse.RequestParser()
emp_args.add_argument("name", help="Name is required", required=True)


class Department(db.Model):
    __tablename__ = "department_table"
    dept_id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String, nullable=False)


resource_field = {
    "dept_id": fields.Integer,
    "dept_name": fields.String,
}


class DeptResource(Resource):
    @marshal_with(resource_field)
    def get(self, dept_id):
        dept = Department.query.filter_by(dept_id=dept_id).first()
        if dept:
            return dept
        else:
            abort(404, message="id doesn't exist {}".format(dept_id))

    @marshal_with(resource_field)
    def post(self, dept_id):
        args = emp_args.parse_args()
        dept = Department.query.filter_by(dept_id=dept_id).first()
        if dept:
            abort(409, message="Id already exist")
        dept = Department(
            dept_id=dept_id,
            dept_name=args["name"]
        )
        db.session.add(dept)
        db.session.commit()
        return dept


class Departments(Resource):
    @marshal_with(resource_field)
    def get(self):
        depts = Department.query.all()
        return depts


# db.create_all()

api.add_resource(DeptResource, "/dept/<string:dept_id>")
api.add_resource(Departments, "/departments")

if __name__ == "__main__":
    app.run(debug=True, port=4200)
