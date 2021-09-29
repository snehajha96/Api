from flask import Flask
from flask_restful import Resource, Api, reqparse, marshal_with, fields, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:sneha@localhost:5432/flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

CORS(app)

emp_args = reqparse.RequestParser()
emp_args.add_argument("name", help="Name is required", required=True)
emp_args.add_argument("email", help="email is required", required=True)
emp_args.add_argument("salary", help="salary is required", required=True)
emp_args.add_argument("designation", help="designation is required", required=True)

emp_put_args = reqparse.RequestParser()
emp_put_args.add_argument("name")
emp_put_args.add_argument("email")
emp_put_args.add_argument("salary")
emp_put_args.add_argument("designation")


class Employee(db.Model):
    __tablename__ = "emp_table"
    emp_id = db.Column(db.Integer, primary_key=True)
    emp_name = db.Column(db.String, nullable=False)
    emp_email = db.Column(db.String, nullable=False)
    emp_salary = db.Column(db.String, nullable=False)
    emp_designation = db.Column(db.String, nullable=False)


resource_field = {
    "emp_id": fields.Integer,
    "emp_name": fields.String,
    "emp_email": fields.String,
    "emp_salary": fields.String,
    "emp_designation": fields.String,
}


class EmpResource(Resource):
    @marshal_with(resource_field)
    def get(self, emp_id):
        emp = Employee.query.filter_by(emp_id=emp_id).first()
        if emp:
            return emp
        else:
            abort(404, message="Employee not found with Id {}".format(emp_id))

    @marshal_with(resource_field)
    def post(self, emp_id):
        args = emp_args.parse_args()
        emp = Employee.query.filter_by(emp_id=emp_id).first()
        if emp:
            abort(409, message="Id already exist")
        emp = Employee(
            emp_id=emp_id,
            emp_name=args["name"],
            emp_email=args["email"],
            emp_salary=args["salary"],
            emp_designation=args["designation"]
        )
        db.session.add(emp)
        db.session.commit()
        return emp

    @marshal_with(resource_field)
    def put(self, emp_id):
        args = emp_put_args.parse_args()
        emp = Employee.query.filter_by(emp_id=emp_id).first()

        if emp:
            emp.emp_name = args["name"] if args["name"] else emp.emp_name
            emp.emp_email = args["email"] if args["email"] else emp.emp_email
            emp.emp_salary = args["salary"] if args["salary"] else emp.emp_salary
            emp.emp_designation = args["designation"] if args["designation"] else emp.emp.designation

            db.session.add(emp)
            db.session.commit()

            return emp
        else:
            abort(404, message="employee id not found")

    @marshal_with(resource_field)
    def delete(self, emp_id):
        emp = Employee.query.filter_by(emp_id=emp_id).first()
        if emp:
            db.session.delete(emp)
            db.session.commit()
        else:
            abort(404, message="Employee not found with Id {}".format(emp_id))

        return emp


class Employees(Resource):
    @marshal_with(resource_field)
    def get(self):
        emps = Employee.query.all()
        return emps


# db.create_all()
api.add_resource(EmpResource, "/employee/<string:emp_id>")
api.add_resource(Employees, "/employees")

if __name__ == "__main__":
    app.run(debug=True)
