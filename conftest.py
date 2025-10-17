import pytest
from fastapi.testclient import TestClient
from app import app, database

@pytest.fixture(scope="module")
def client():
    """
    Create a FastAPI test client that ensures the database is connected
    before each test and disconnected after all tests.
    """
    with TestClient(app) as c:
        import asyncio

        # Ensure DB connection
        try:
            asyncio.get_event_loop().run_until_complete(database.connect())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(database.connect())

        yield c

        # Clean DB connection at teardown
        try:
            asyncio.get_event_loop().run_until_complete(database.disconnect())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(database.disconnect())
