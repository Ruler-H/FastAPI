from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def index():
    return "<h1>Hello World 1</h1>"


@app.get("/about", response_class=HTMLResponse)
def about():
    return "<h1>Hello World 2</h1>"


@app.get("/contact", response_class=HTMLResponse)
def contact():
    return "<h1>Hello World 3</h1>"


@app.get("/notice", response_class=HTMLResponse)
def notice():
    return "<h1>Hello World 4</h1>"
