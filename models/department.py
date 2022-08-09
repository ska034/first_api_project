from models.database import db


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey('offices.id'))

    def __repr__(self):
        return f"\nId: {self.id}\nTitle: {self.title}\n Office_id: {self.office_id}"