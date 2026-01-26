from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from testdebiritservice.database import get_db
from testdebiritservice.models.price import Price

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("/")
def get_all_prices(
    ticker: str = Query(...),
    db: Session = Depends(get_db),
):
    return db.query(Price).filter(Price.ticker == ticker).all()


@router.get("/latest")
def get_latest_price(
    ticker: str = Query(...),
    db: Session = Depends(get_db),
):
    price = (
        db.query(Price)
        .filter(Price.ticker == ticker)
        .order_by(Price.timestamp.desc())
        .first()
    )

    if not price:
        raise HTTPException(status_code=404, detail="Price not found")

    return price


@router.get("/by-date")
def get_prices_by_date(
    ticker: str = Query(...),
    date_from: int = Query(...),
    date_to: int = Query(...),
    db: Session = Depends(get_db),
):
    return (
        db.query(Price)
        .filter(
            Price.ticker == ticker,
            Price.timestamp >= date_from,
            Price.timestamp <= date_to,
        )
        .all()
    )
