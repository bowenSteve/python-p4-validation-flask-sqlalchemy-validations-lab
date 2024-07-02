from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if name=='':
            raise ValueError("Record must have a name")
        check=Author.query.filter(Author.name==name).first()
        if check:
            raise ValueError("Record must have a unique name")
        return name
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number.isdigit():
            raise ValueError("Phone number should be a digit")
        if len(phone_number) !=10 :
            raise ValueError("Phone number should be exactly ten digits")
        return phone_number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title',)
    def validate_title(self, key, title):
        clickbaits=["Won't Believe", "Secret", "Top", "Guess"]
        if title=='':
            raise ValueError("Post must have a title")
        if not any(phrase in title for phrase in clickbaits):
            raise ValueError("Title must contain one of the following phrases: 'Won't Believe', 'Secret', 'Top', 'Guess'")
        return title
    @validates('content')
    def validate_content(self, key, content):
        if len(content)<250:
            raise ValueError("Content is too short!")
        return content
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary)>250:
            raise ValueError("Summary is too long")
        return summary
    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Incorrect Category")
        return category
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
