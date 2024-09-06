
from pydantic import BaseModel
from typing import Optional,List

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id:int

    class Config:
        orm_mode=True

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id:int
    class Config:
        orm_mode=True

class PostBase(BaseModel):
    title: str
    description: str
    image: Optional[str]=None

class PostCreate(PostBase):
    category_id:int
    tag_ids: List[int]

class Post(PostBase):
    id:int
    category:Category
    tags:List[Tag]=[]

    class Config:
        orm_mode=True