from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///planner.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(Date)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))

    user = relationship('User', back_populates='tasks')
    category = relationship('Category')

User.tasks = relationship('Task', order_by=Task.id, back_populates='user')

def init_db():
    Base.metadata.create_all(engine)

def create_task(session, title, user_id, description=None, due_date=None, category_id=None):
    task = Task(title=title, description=description, due_date=due_date, user_id=user_id, category_id=category_id)
    session.add(task)
    session.commit()

def read_tasks(session):
    return session.query(Task).all()

def update_task(session, task_id, **kwargs):
    task = session.query(Task).filter_by(id=task_id).first()
    for key, value in kwargs.items():
        setattr(task, key, value)
    session.commit()

def delete_task(session, task_id):
    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        session.delete(task)
        session.commit()

if __name__ == '__main__':
    init_db()
    session = Session()

    create_task(session, title="Learn Python", user_id=1)
    tasks = read_tasks(session)
    for task in tasks:
        print(task.title)

    session.close()
