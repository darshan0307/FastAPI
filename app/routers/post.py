from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import  List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import  get_db



router = APIRouter(
    # tests expect endpoint under "/posts/" so keep prefix plural
    prefix="/posts",
    tags=['Posts']
)


@router.post("/",  status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                  (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/" , response_model=List[schemas.PostOut], status_code=status.HTTP_200_OK)
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
             limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # query returns tuples of (Post, votes)
    raw_results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # flatten each tuple into a dict that matches the PostOut schema
    posts = []
    for post_obj, votes in raw_results:
        posts.append({
            "id": post_obj.id,
            "title": post_obj.title,
            "content": post_obj.content,
            "published": post_obj.published,
            "created_at": post_obj.created_at,
            "owner_id": post_obj.owner_id,
            "owner": post_obj.owner,
            "votes": votes
        })
    return posts


@router.get("/latest")
def latest_post():
    post = my_post[len(my_post)-1]
    return {"Post_details": post}



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()

    raw_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id == id).first()
    if raw_post:
        post_obj, votes = raw_post
        post = {
            "id": post_obj.id,
            "title": post_obj.title,
            "content": post_obj.content,
            "published": post_obj.published,
            "created_at": post_obj.created_at,
            "owner_id": post_obj.owner_id,
            "owner": post_obj.owner,
            "votes": votes
        }
    else:
        post = None
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"post with id: {id} was not found")

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, str(id))
    # delete = cursor.fetchone()
    # conn.commit()

    delete_post = db.query(models.Post).filter(models.Post.id == id)
    delete = delete_post.first()

    if delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    if delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action")


    delete_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #                 (post.title, post.content, post.published, str(id)))

    # update = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action") 

    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()

    # return the updated object directly (not wrapped) to match tests
    updated = post_query.first()
    return {
        "id": updated.id,
        "title": updated.title,
        "content": updated.content,
        "published": updated.published,
        "created_at": updated.created_at,
        "owner_id": updated.owner_id,
        "owner": updated.owner
    }

