from fastapi import FastAPI

app = FastAPI()


@app.get(
    "/", tags=["root"], summary="Root API", description="Hello World를 반환합니다."
)
def read_root():
    return {"Hello": "World"}


@app.get("/about")
def about():
    return {"message": "about page"}


@app.get("/contact")
def contact():
    return {"message": "contact page"}


@app.get("/notice")
def notice():
    return {
        "notice": [
            {"title": "공지사항1", "content": "내용"},
            {"title": "공지사항2", "content": "내용"},
            {"title": "공지사항3", "content": "내용"},
        ]
    }
