from models.database import db


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50), nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    salary = db.Column(db.Float, nullable=True)


    def __repr__(self):
        return f"\nId: {self.id}\nLast_name: {self.last_name}\n First_name: {self.first_name}\n Patronymic: {self.patronymic}" \
               f"\nDepartment_id: {self.department_id}\n Role_id: {self.role_id}\n Salary: {self.salary}"
