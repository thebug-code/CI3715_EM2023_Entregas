from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(30), unique=True, nullable=False)
    last_name = db.Column(db.String(30), unique=True, nullable=False)
    rol = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    pass_hash = db.Column(db.String(25), nullable=False)
    
    @staticmethod
    def is_admin(self):
        return self.role.name == 'Administrator'

    def __repr__(self):
        return f"Usuario('{self.username}' '{self.first_name}' '{self.last_name}' '{self.role.name}')"

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = ('Administrator', 'Operations Manager') #Luego se explande
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None: # Si no esta el rol se anade
                role = Role(name=r)
                db.session.add(role)
                db.session.commit()
        
    def __repr__(self):
        return '<Role %r>' % self.name
