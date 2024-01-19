from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, crawler
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/predict/", )
def predict(db: Session = Depends(get_db)):
    return {"db": db}


@app.get("/crawl/{city_id}/{category_id}", )
def crawl(city_id: int, category_id: int, min_page: int = 0, max_page: int = 10, db: Session = Depends(get_db)):
    result = crawler.DivarCrawler(city_id=city_id, category_id=category_id, db=db, min_page=min_page,
                                  max_page=max_page).crawl()
    return {
        'city_id': city_id,
        'category_id': category_id,
        'db': db,
        'result': result
    }


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
