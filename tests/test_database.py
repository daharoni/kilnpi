import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database_model import Base, Firing
import datetime

@pytest.fixture(scope="module")
def test_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_add_firing(test_session):
    new_firing = Firing(name='Test Firing', start_time=datetime.datetime.now(), firing_profile='Test Profile')
    test_session.add(new_firing)
    test_session.commit()
    assert new_firing.firing_id is not None