from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="./templates")
static = Jinja2Templates(directory="./static")
