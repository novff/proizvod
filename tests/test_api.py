def register(client, email="operator@example.com"):
    return client.post("/api/auth/register",json={"email":email,"full_name":"Тестовый оператор","password":"StrongPass123!"})
def login(client,email="operator@example.com"):
    return client.post("/api/auth/login",json={"email":email,"password":"StrongPass123!"})
def test_health(client):
    response=client.get("/health"); assert response.status_code==200; assert response.json()["status"]=="ok"
def test_register_and_login(client):
    assert register(client).status_code==201
    response=login(client); assert response.status_code==200; assert "access_token" in response.json()
def test_duplicate_registration_rejected(client):
    register(client); response=register(client); assert response.status_code==409
def test_private_endpoint_requires_token(client):
    response=client.get("/api/components"); assert response.status_code==401
def test_operator_can_create_ticket(client):
    register(client); token=login(client).json()["access_token"]
    response=client.post("/api/tickets",headers={"Authorization":f"Bearer {token}"},json={"title":"Проверить обновление","description":"Проверка после установки"})
    assert response.status_code==201; assert response.json()["status"]=="new"
def test_operator_cannot_create_component(client):
    register(client); token=login(client).json()["access_token"]
    response=client.post("/api/components",headers={"Authorization":f"Bearer {token}"},json={"name":"Test App","version":"1.0"})
    assert response.status_code==403


def test_admin_can_create_component(client):
    response=client.post("/api/auth/login",json={"email":"admin@example.com","password":"Admin12345!"})
    assert response.status_code==200
    token=response.json()["access_token"]
    created=client.post("/api/components",headers={"Authorization":f"Bearer {token}"},json={"name":"Учебная CRM","version":"1.0.0","vendor":"Учебный проект"})
    assert created.status_code==201
    assert created.json()["name"]=="Учебная CRM"


def test_operator_sees_only_own_tickets(client):
    register(client)
    token=login(client).json()["access_token"]
    headers={"Authorization":f"Bearer {token}"}
    client.post("/api/tickets",headers=headers,json={"title":"Моя заявка","description":"Тест"})
    response=client.get("/api/tickets",headers=headers)
    assert response.status_code==200
    assert len(response.json())==1
    assert response.json()[0]["title"]=="Моя заявка"
