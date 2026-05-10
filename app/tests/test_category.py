from app.tests.conftest import TEST_CATEGORY, TEST_CATEGORY_EXPENSE


class TestGetCategories:
    def test_get_categories_empty(self, client, headers):
        response = client.get("/api/v1/categories/", headers=headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_get_categories_unauthorized(self, client):
        response = client.get("/api/v1/categories/")
        assert response.status_code == 401

    def test_get_categories_with_data(self, client, headers, created_category):
        response = client.get("/api/v1/categories/", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == created_category["name"]


class TestGetCategory:
    def test_get_category_success(self, client, headers, created_category):
        response = client.get(
            f"/api/v1/categories/{created_category['id']}", headers=headers
        )
        assert response.status_code == 200
        assert response.json()["name"] == created_category["name"]

    def test_get_category_not_found(self, client, headers):
        response = client.get("/api/v1/categories/999", headers=headers)
        assert response.status_code == 404


class TestCreateCategory:
    def test_create_category_income(self, client, headers):
        response = client.post(
            "/api/v1/categories/", json=TEST_CATEGORY, headers=headers
        )
        assert response.status_code == 201
        assert response.json()["created_item"]["name"] == TEST_CATEGORY["name"]
        assert response.json()["created_item"]["type"] == TEST_CATEGORY["type"]

    def test_create_category_expense(self, client, headers):
        response = client.post(
            "/api/v1/categories/", json=TEST_CATEGORY_EXPENSE, headers=headers
        )
        assert response.status_code == 201
        assert response.json()["created_item"]["type"] == TEST_CATEGORY_EXPENSE["type"]

    def test_create_category_invalid_type(self, client, headers):
        response = client.post(
            "/api/v1/categories/",
            json={"name": "Food", "type": "invalid"},
            headers=headers,
        )
        assert response.status_code == 422

    def test_create_category_unauthorized(self, client):
        response = client.post("/api/v1/categories/", json=TEST_CATEGORY)
        assert response.status_code == 401


class TestUpdateCategory:
    def test_update_category_name(self, client, headers, created_category):
        response = client.patch(
            f"/api/v1/categories/{created_category['id']}",
            json={"name": "Freelance"},
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Freelance"

    def test_update_category_not_found(self, client, headers):
        response = client.patch(
            "/api/v1/categories/999",
            json={"name": "Freelance"},
            headers=headers,
        )
        assert response.status_code == 404

    def test_update_category_type_conflict(self, client, headers):
        # TODO: add a transaction using this category then try to change type
        pass


class TestDeleteCategory:
    def test_delete_category_success(self, client, headers, created_category):
        response = client.delete(
            f"/api/v1/categories/{created_category['id']}", headers=headers
        )
        assert response.status_code == 204

    def test_delete_category_not_found(self, client, headers):
        response = client.delete("/api/v1/categories/999", headers=headers)
        assert response.status_code == 404

    def test_delete_category_unauthorized(self, client):
        response = client.delete("/api/v1/categories/1")
        assert response.status_code == 401
