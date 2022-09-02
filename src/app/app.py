from json import JSONEncoder
import validators
import uvicorn
import os

from fastapi import Depends, FastAPI, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from db import crud, models, schemas
from db.database import SessionLocal, engine
from features.shortlink.ShortenLink import ShortLink
from processfunc import *
from frontend import *

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/src/app/static", StaticFiles(directory="./static"), name="static")
app.mount("/src/app/templates", StaticFiles(directory="./templates"), name="templates")

# initialize database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return static.TemplateResponse("/index.html", {"request": request})


@app.get("/api/db-api")
async def api_db(request: Request, db: Session = Depends(get_db)):
    num_of_data = crud.get_number_of_data(db)
    return {"status": 200, "data": crud.get_db_detail_by_page(db, 0, num_of_data)}


@app.post("/admin/deactivate-url")
async def deactivate_url_api(
    request: Request, api_key: str, short_url: str, db: Session = Depends(get_db)
):
    return crud.update_state_url(db, short_url, False)


@app.get("/admin/db", response_class=HTMLResponse)
async def show_database(request: Request, page: int = 1, db: Session = Depends(get_db)):
    number_of_record_in_page = 10
    num_of_data = crud.get_number_of_data(db)
    total = round(num_of_data / number_of_record_in_page) + 1

    if page <= 0 or page > total:
        return RedirectResponse(url="/admin/db?page=1")

    page_idx = page - 1
    offset = page_idx * number_of_record_in_page

    urls = crud.get_db_detail_by_page(db, offset, number_of_record_in_page)
    next_page = page + 1
    prev_page = page - 1
    is_disable_prev = ""
    is_disable_next = ""

    if next_page > total:
        is_disable_next = "disabled"
    if prev_page <= 0:
        is_disable_prev = "disabled"

    return templates.TemplateResponse(
        "/ShowDB/index.html",
        {
            "request": request,
            "urls": urls,
            "entity_number": len(urls),
            "start": offset,
            "prev_page": prev_page,
            "next_page": next_page,
            "is_disable_next": is_disable_next,
            "is_disable_prev": is_disable_prev,
            "total_pages": num_of_data,
            "per_page": num_of_data % number_of_record_in_page,
        },
    )


@app.get("/error", response_class=HTMLResponse)
async def error_page(request: Request):
    return render_error_page(request)


def render_error_page(
    request: Request, status_code: int = 404, details: str = "NOT FOUND"
):
    return templates.TemplateResponse(
        "error/error.html",
        {"request": request, "error_status": details, "error_code": status_code},
    )


@app.post("/api/get-urls")
async def get_urls(request: Request, db: Session = Depends(get_db)):
    return crud.get_urls(db=db)


# Auto generate a short link
@app.post("/api/api-save-short-link/")
def save_to_database(
    request: Request, url: schemas.UserInputShortLink, db: Session = Depends(get_db)
):
    status_code = 200
    message = "Successfully"
    is_valid_url = validators.url(url.long_url)
    if not is_valid_url:
        message = "Your link is not valid"
    else:
        if url.is_custom_url:
            short_url = process_custom_url(url.short_url)
        else:
            short_url = ShortLink.shorter_url(url.long_url)

        is_exist = crud.is_duplicate_short_link(db, short_url)
        db_short_link = None

        if not is_exist:
            db_short_link = crud.save_short_link(
                db=db, short_url=short_url, long_url=url.long_url
            )

            if not db_short_link:
                status_code = 400
                message = "Short link is not saved successfully"
            else:
                message = f"{request.base_url._url}{db_short_link.short_url}"

        else:
            message = "Short link is exist"

    return {"status": status_code, "message": message}


# redirect
@app.get("/{short_url}", response_class=RedirectResponse, status_code=302)
async def redirect_user(short_url: str, db: Session = Depends(get_db)):
    url_stored = crud.get_redirect_url(db, short_url)
    if url_stored is not None:
        crud.increase_access_count(db, short_url)
        return url_stored.long_url

    return "/error"


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return render_error_page(request, exc.status_code, exc.detail)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT", 8080))
