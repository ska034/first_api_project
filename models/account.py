from models.database import db


class Account(db.Model):
    __tablename__ = 'accounts'

    login = db.Column(db.String(20), primary_key=True, autoincrement=False, nullable=False, unique=True)
    password = db.Column(db.Text, default='first_password', nullable=False)
    staff_number = db.Column(db.Integer, db.ForeignKey('employees.staff_number', ondelete='CASCADE'))

    def __repr__(self):
        return f"\nStaff_number: {self.staff_number}\nlogin: {self.login}\npassword: {self.password}"
