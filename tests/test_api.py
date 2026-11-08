import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.database import Base, get_db
from backend.main import app
from backend.models import User
from backend.security import hash_password, verify_password

class APITests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
        Base.metadata.create_all(self.engine)
        self.sessions = sessionmaker(bind=self.engine)
        def override_db():
            with self.sessions() as session:
                yield session
        app.dependency_overrides[get_db] = override_db
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()
        self.engine.dispose()

    def test_registration_never_returns_password_and_stores_argon2(self):
        response = self.client.post("/users/", json={"email": "demo@example.com", "password": "long-demo-password"})
        self.assertEqual(response.status_code, 201)
        self.assertNotIn("hashed_password", response.json())
        self.assertNotIn("password", response.json())
        with self.sessions() as db:
            user = db.query(User).one()
            self.assertTrue(user.hashed_password.startswith("$argon2id$"))
            self.assertTrue(verify_password("long-demo-password", user.hashed_password))
            self.assertFalse(user.is_admin)

    def test_duplicate_registration(self):
        data = {"email": "demo@example.com", "password": "long-demo-password"}
        self.client.post("/users/", json=data)
        self.assertEqual(self.client.post("/users/", json=data).status_code, 400)

    def test_invalid_email_and_short_password(self):
        for data in ({"email": "invalid", "password": "long-demo-password"},
                     {"email": "demo@example.com", "password": "short"}):
            self.assertEqual(self.client.post("/users/", json=data).status_code, 422)

    def test_hashes_are_salted_and_wrong_password_fails(self):
        first = hash_password("long-demo-password")
        self.assertNotEqual(first, hash_password("long-demo-password"))
        self.assertFalse(verify_password("incorrect", first))

    def test_health(self):
        self.assertEqual(self.client.get("/health").status_code, 200)
