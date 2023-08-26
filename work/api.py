from asyncio import current_task
from operator import index
from turtle import pos, title
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException , Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db





models.Base.metadata.create_all(bind=engine)



app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published: bool = True
   
    
while True:

    try:
        conn = psycopg2.connect(host='localhost',
                             user='postgres',
                             password='olaoluwa99',
                             database='fastapi',
                             cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesful")
        break
    except Exception as error:
         print("Connection to database failed")
         print("Error: ", error)
         time.sleep(3)



my_posts =[{"title": "title of post 1", "content": "content of post 1","id" : 1},
 {"title": "type of foods", "content": "i like pizza", "id": 2} ]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i 
    


@app.get("/")
def get_post():
    return{"Hello world"}



@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
  
    print(posts)
    
    
    
    
    return {"data": "successful"}




@app.get("/login")
def get_posts():
    cursor.execute("""SELECT * from posts """)
    posts = cursor.fetchall()
    return {"message": "Kindly login with your username and password"}





@app.get("/posts/latest")
def get_latest_posts():
    post = my_posts[len(my_posts)-1]
    return{"detail": post}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()



  
   # post_dict = post.dict()
    #post_dict['id'] = randrange(0, 100000)
   # my_posts.append(post_dict)
    return {"date": new_post}




@app.get("/posts/{id}")
def get_post(id: int,):
    cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    print(post)
    post = find_post(id)
    
    

    
    #post = find_post((id))
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'post with id {id} was not found') 
        
        #response.status_code = status.HTTP_404_NOT_FOUND       #this is another method
        #return{"message": f'post with id {id} was not found'}
    print(post)
    return {"post_  detail": post}   



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""" ,(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    #index = find_index_post(id)


    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id:{id} does not exist")

    
    
   
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, (str(id))))
    updated_post = cursor.fetchone()
    conn.commit()


    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id:{id} does not exist")
   
    return {"data": updated_post}
    
