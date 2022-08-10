from models.database import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(100), nullable=False)
    employees = db.relationship('Employee', backref='role')

    def __repr__(self):
        return f"\nId: {self.id}\nPosition: {self.position}"
