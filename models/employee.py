from models.database import db


class Employee(db.Model):
    __tablename__ = 'employees'
    staff_number = db.Column(db.Integer, primary_key=True, autoincrement=False, nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50), nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id', ondelete='SET NULL'), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='SET NULL'), nullable=True)
    salary = db.Column(db.Float, nullable=True)
    accounts = db.relationship('Account', backref='employee', cascade='all,delete-orphan', passive_deletes=True)
    tokens = db.relationship('Token', backref='employee', cascade='all,delete-orphan', passive_deletes=True)

    def __repr__(self):
        return f"\nStaff_number: {self.staff_number}\nLast_name: {self.last_name}\nFirst_name: {self.first_name}" \
               f"\nPatronymic: {self.patronymic}\nDepartment_id: {self.department_id}\nRole_id: {self.role_id}\n" \
               f"Salary: {self.salary}"
