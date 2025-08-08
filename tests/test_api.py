from fastapi.testclient import TestClient

from market_sage_pro.api.main import app


def test_health():
    client = TestClient(app)
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'


def test_signal_endpoint():
    client = TestClient(app)
    r = client.post('/signal', json={
        'ensemble_up_prob': 0.7,
        'ensemble_down_prob': 0.3,
        'predicted_move_pct': 0.3,
        'rsi': 50,
        'price_vs_ema21': 1,
        'ivr': 0.2,
        'prob_big_move': 0.7,
    })
    assert r.status_code == 200
    data = r.json()
    assert 'action' in data