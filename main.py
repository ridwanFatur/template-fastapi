from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from api import auth, user
from middleware.origin_middleware import check_allowed_origin
from fastapi import FastAPI

from db.database import Base, engine
from utils.config import CORS_ORIGINS


app = FastAPI(title="Template Project",
              version="1.0.0", redirect_slashes=False)


Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.middleware("http")(check_allowed_origin)


@app.get("/")
async def root():
    return {"message": "App is Ready 2"}

app.include_router(auth.router)
app.include_router(user.router)
