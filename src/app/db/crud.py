from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from . import models


def is_duplicate_short_link(db: Session, short_url: str):
    return (
        db.query(models.ShortLink)
        .filter(models.ShortLink.short_url == short_url)
        .first()
    ) != None


def get_redirect_url(db: Session, short_url: str):
    return (
        db.query(models.ShortLink)
        .filter(models.ShortLink.short_url == short_url)
        .first()
    )


def get_urls(
    db: Session,
):
    return db.query(models.ShortLink).all()


def save_short_link(db: Session, short_url: str = "", long_url: str = ""):
    db_short_url, db_long_url = short_url, long_url

    db_save_short_link = models.ShortLink(
        short_url=db_short_url,
        long_url=db_long_url,
        access_count=0,
        is_activate=True,
        datetime=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    )

    db.add(db_save_short_link)
    db.commit()
    db.refresh(db_save_short_link)
    return db_save_short_link


def update_state_url(db: Session, short_url: str, state: bool):
    curr_short_urls = db.query(models.ShortLink).filter(
        models.ShortLink.short_url == short_url
    )

    if not curr_short_urls.first():
        return False

    curr_short_urls.update({"is_activate": state})
    db.commit()
    return True


def increase_access_count(db: Session, short_url: str):
    curr_short_urls = db.query(models.ShortLink).filter(
        models.ShortLink.short_url == short_url
    )

    if not curr_short_urls.first():
        return False

    curr_short_urls.update({"access_count": curr_short_urls.first().access_count + 1})
    db.commit()
    return True


def get_db_detail_by_page(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(models.ShortLink)
        .order_by(desc(models.ShortLink.datetime))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_number_of_data(db: Session):
    return len(db.query(models.ShortLink).all())
