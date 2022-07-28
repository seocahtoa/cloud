class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    active = db.Column(db.Boolean, nullable=False, default=True)

    @property
    def is_active(self):
        # override UserMixin property which always returns true
        # return the value of the active column instead
        return self.active