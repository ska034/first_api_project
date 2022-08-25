from models.database import db


class Token(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    staff_number = db.Column(db.Integer, db.ForeignKey('employees.staff_number', ondelete='CASCADE'))
    token = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.Integer, nullable=True)
    end_time = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"\nstaff_number: {self.staff_number}\naccess token: {self.token}\nstart_time: {self.start_time}" \
               f"\nend_time: {self.end_time}"
