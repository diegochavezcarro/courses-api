import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.main import app
from app.models import Course
from app.database import get_db

client = TestClient(app)

@pytest.fixture
def fake_db_session():
    class FakeSession:
        def __init__(self):
            self.data = []

        async def add(self, instance):
            self.data.append(instance)

        async def commit(self):
            pass

        async def refresh(self, instance):
            pass

        class Result:
            def __init__(self, data):
                self.data = data

            def scalars(self):
                return self

            def first(self):
                return self.data[0] if self.data else None

            def all(self):
                return self.data

        async def execute(self, query):
            return self.Result([row for row in self.data if isinstance(row, Course)])

        async def query(self, model):
            return [row for row in self.data if isinstance(row, model)]

        async def delete(self, instance):
            self.data.remove(instance)

    return FakeSession()

@pytest.fixture
def override_get_db(fake_db_session):
    async def _override_get_db():
        yield fake_db_session
    app.dependency_overrides[get_db] = _override_get_db

@pytest.mark.asyncio
async def test_create_course_endpoint(override_get_db):
    response = client.post("/courses/", json={"name": "Test Course", "description": "Test Description"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Course"
    assert data["description"] == "Test Description"
    assert "id" in data

@pytest.mark.asyncio
async def test_read_courses_endpoint(override_get_db):
    response = client.get("/courses/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_read_course_endpoint(override_get_db):
    # First create a course to ensure there is something to fetch
    create_response = client.post("/courses/", json={"name": "Test Course", "description": "Test Description"})
    course_id = create_response.json()["id"]

    # Now fetch the created course
    response = client.get(f"/courses/{course_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Course"
    assert data["description"] == "Test Description"

@pytest.mark.asyncio
async def test_delete_course_endpoint(override_get_db):
    # First create a course to ensure there is something to delete
    create_response = client.post("/courses/", json={"name": "Course to Delete", "description": "Delete Description"})
    course_id = create_response.json()["id"]

    # Now delete the created course
    delete_response = client.delete(f"/courses/{course_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data["message"] == "Course deleted"

    # Ensure the course is deleted
    get_response = client.get(f"/courses/{course_id}")
    assert get_response.status_code == 404
