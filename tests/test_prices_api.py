import time


from testdebiritservice.models import Price


def seed_prices(db_session):
    """Создаём тестовые цены в базе."""
    now = int(time.time())
    prices = [
        Price(ticker="btc_usd", price=90000, timestamp=now - 100),
        Price(ticker="btc_usd", price=91000, timestamp=now),
        Price(ticker="eth_usd", price=2900, timestamp=now),
    ]
    db_session.add_all(prices)
    db_session.commit()


def test_get_prices(client, db_session):
    seed_prices(db_session)

    response = client.get("/prices", params={"ticker": "btc_usd"})
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_latest_price(client, db_session):
    seed_prices(db_session)

    response = client.get("/prices/latest", params={"ticker": "btc_usd"})
    assert response.status_code == 200

    data = response.json()
    assert data["ticker"] == "btc_usd"
    assert data["price"] == 91000


def test_get_prices_by_date(client, db_session):
    seed_prices(db_session)
    now = int(time.time())

    response = client.get(
        "/prices/by-date",
        params={
            "ticker": "btc_usd",
            "date_from": now - 200,
            "date_to": now - 50,
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
