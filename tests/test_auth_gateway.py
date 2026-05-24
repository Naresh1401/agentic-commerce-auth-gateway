from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app, raise_server_exceptions=False)

def test_login_and_me():
    token = client.post('/auth/login', json={'username': 'demo_customer_001', 'role': 'customer'}).json()['access_token']
    response = client.get('/auth/me', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json()['role'] == 'customer'

def test_partner_cannot_call_admin_audit_log():
    response = client.get('/auth/audit-log', headers={'X-API-Key': 'demo_partner_key'})
    assert response.status_code == 403
    assert response.json()['error']['code'] == 'RBAC_DENIED'

