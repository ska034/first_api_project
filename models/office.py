from app import db


class Office(db.Model):
    __tablename__ = 'offices'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    country = db.Column(db.String(50),nullable = False)
    address = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"\nId: {self.id}\nTitle: {self.title}\n Address: {self.address}"
