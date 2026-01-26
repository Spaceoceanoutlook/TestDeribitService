import asyncio
import time

from testdebiritservice.celery import celery_app
from testdebiritservice.services.debirit_client import DebiritClient
from testdebiritservice.database import SessionLocal
from testdebiritservice.models.price import Price
from settings import settings


@celery_app.task(name="testdebiritservice.tasks.fetch_prices.fetch_prices")
def fetch_prices():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_fetch_prices_async())
    loop.close()


async def _fetch_prices_async():
    client = DebiritClient()
    db = SessionLocal()

    try:
        for ticker in settings.tickers:
            price = await client.get_index_price(ticker)

            price_row = Price(ticker=ticker, price=price, timestamp=int(time.time()))

            db.add(price_row)

        db.commit()

    except Exception:
        db.rollback()

    finally:
        db.close()
