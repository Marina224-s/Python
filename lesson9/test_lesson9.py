import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Database setup
DATABASE_URL = "postgresql://postgres:1@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Subject model
class Subject(Base):
    __tablename__ = 'subject'

    subject_id = Column(Integer, primary_key=True)
    subject_title = Column(String)

# Test for adding a subject
def test_add_subject():
    session = Session()
    subject = Subject(subject_id=100, subject_title="Mathematics")
    session.add(subject)
    session.commit()

    saved = session.query(Subject).filter_by(subject_id=100).first()
    assert saved.subject_title == "Mathematics"

    session.delete(saved)
    session.commit()
    session.close()

# Test for updating a subject
def test_update_subject():
    session = Session()
    subject = Subject(subject_id=200, subject_title="Physics")
    session.add(subject)
    session.commit()

    subject.subject_title = "Advanced Physics"
    session.commit()

    updated = session.query(Subject).filter_by(subject_id=200).first()
    assert updated.subject_title == "Advanced Physics"

    session.delete(updated)
    session.commit()
    session.close()

# Test for deleting a subject
def test_delete_subject():
    session = Session()
    subject = Subject(subject_id=300, subject_title="Chemistry")
    session.add(subject)
    session.commit()

    session.delete(subject)
    session.commit()

    deleted = session.query(Subject).filter_by(subject_id=300).first()
    assert deleted is None

    session.close()