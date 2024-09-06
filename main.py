from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal,engine
import models
import schema

#MB yaratish
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# dependancy

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD uchun Category endpointlari
@app.post("/categories/",response_model=schema.Category)
def create_new_category(category:schema.CategoryCreate,db:Session=Depends(get_db)):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/categories/",response_model=List[schema.Category])
def read_all_categories(db:Session=Depends(get_db)):
    return db.query(models.Category).all()

# CRUD uchun Tag endpointlari
@app.post("/tags/",response_model=schema.Tag)
def create_tag(tag:schema.TagCreate,db:Session=Depends(get_db)):
    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@app.get("/tags/",response_model=List[schema.Tag])
def read_all_tags(db:Session=Depends(get_db)):
    return db.query(models.Tag).all()

# CRUD uchun Post endpointlari
@app.post("/posts/",response_model=schema.Post)
def create_post(post:schema.PostCreate,db:Session=Depends(get_db)):
    db_post = models.Post(
        title=post.title,
        description=post.description,
        image=post.image,
        category_id=post.category_id
    )
    db.add(db_post)

    #taglarni bog'lash
    db_post.tags = db.query(models.Tag).filter(models.Tag.id.in_(post.tag_ids)).all()

    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/",response_model=List[schema.Post])
def read_all_posts(db:Session=Depends(get_db)):
    return db.query(models.Post).all()

@app.get("/posts/{post_id}",response_model=schema.Post)
def read_post(post_id:int,db:Session=Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id==post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404,detail="Post not found")
    return db_post

@app.put("/posts/{post_id}",response_model=schema.Post)
def update_post(post_id:int,post:schema.PostCreate,db:Session=Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id==post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404,detail="Post not found")

    db_post.title = post.title
    db_post.description = post.description
    db_post.image = post.image
    db_post.category_id = post.category_id
    db_post.tags = db.query(models.Tag).filter(models.Tag.id.in_(post.tag_ids)).all()

    db.commit()
    db.refresh(db_post)
    return db_post

@app.delete("/posts/{post_id}")
def delete_post(post_id:int,db:Session=Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id==post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404,detail="Post not found")
    db.delete(db_post)
    db.commit()
    db.refresh(db_post)
    return {"message":"Post deleted successfully"}