import uvicorn
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote


models.Base.metadata.create_all(bind=engine)
# ensure models are imported 

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello World !!!!!!!! Run Syccessfully "}








# @app.post("/iteams/")
# async def update_items(data: int):
#     """
#     """
#     print(data)
#     return data * 10




# my_post = [{"title": "title of post 1", "content": "content of post 1", "id":1}, {
#     "title": "favorite foods", "content": "i like biriyani", "id":2
# }]


# def find_post(id):
#     for i in my_post:
#         if i["id"] == id:
#             return i


# def find_index_post(id):
#     for i, p in enumerate(my_post):
#         if p['id'] == id:
#             return i


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port= 5000)

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):

#     posts = db.query(models.Post).all()

#     print(posts)
#     return {"data": posts}