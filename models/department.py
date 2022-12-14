from models.database import db


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey('offices.id', ondelete='CASCADE'))
    employees = db.relationship('Employee', backref='department', cascade='all,delete-orphan', passive_deletes=True)

    def __repr__(self):
        return f"\nId: {self.id}\nTitle: {self.title}\nOffice_id: {self.office_id}"
