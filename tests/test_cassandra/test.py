import pytest


@pytest.fixture()
def db():
    ...

@pytest.mark('connect')
def test_connection(self):
    ...

@pytest.mark('create')
def test_create(self):
    ...

@pytest.mark('connect')
def test_read(self):
    ...

@pytest.mark('insert')
def test_update(self):
    ...

@pytest.mark('insert')
def test_delete(self):
    ...
