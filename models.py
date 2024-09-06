from sqlalchemy import Column, Integer, String, Text,ForeignKey,Table, create_engine
from sqlalchemy.orm import relationship
from database import Base

# many to many relationship uchun yordamchi jadval

post_tags = Table('post_tags',
                  Base.metadata,
                  Column("post_id", ForeignKey('posts.id'),primary_key=True),
                  Column("tag_id", ForeignKey('tags.id'),primary_key=True),
                  )

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String,unique=True,index=True)

    posts = relationship('Post', back_populates='category')

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String,unique=True,index=True)

    posts = relationship('Post',secondary=post_tags ,back_populates='tag')

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String,unique=True,index=True)
    description = Column(Text,index=True)
    image = Column(String,index=True)

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category',back_populates='posts')

    tags = relationship('Tag',secondary=post_tags,back_populates='posts')