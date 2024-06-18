import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.main import app
from app.database import create_db, get_db
from app.models import Course

@pytest.fixture(autouse=True, scope='module')
async def setup_db():
    await create_db()
    yield
    # No teardown needed as the database is in-memory

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.mark.asyncio
async def test_create_course(client: TestClient):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/courses/", json={"name": "Test Course", "description": "Test Description"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Course"
    assert data["description"] == "Test Description"
    assert "id" in data

@pytest.mark.asyncio
async def test_read_courses(client: TestClient):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/courses/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_read_course(client: TestClient):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First create a course to ensure there is something to fetch
        create_response = await ac.post("/courses/", json={"name": "Test Course", "description": "Test Description"})
        course_id = create_response.json()["id"]

        # Now fetch the created course
        response = await ac.get(f"/courses/{course_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Course"
    assert data["description"] == "Test Description"

""" @pytest.mark.asyncio
async def test_delete_course(client: TestClient):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First create a course to ensure there is something to delete
        create_response = await ac.post("/courses/", json={"name": "Course to Delete", "description": "Delete Description"})
        course_id = create_response.json()["id"]

        # Now delete the created course
        delete_response = await ac.delete(f"/courses/{course_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data["message"] == "Course deleted"

    # Ensure the course is deleted
    get_response = await ac.get(f"/courses/{course_id}")
    assert get_response.status_code == 404
 """