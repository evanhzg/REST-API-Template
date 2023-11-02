from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from uvicorn import run

# Import your controller files
from app.controllers import DataController


# Create a main FastAPI app instance
app = FastAPI()

# Merge the FastAPI app instances from different controllers
app.include_router(DataController.app)

if __name__ == "__main__":
    # Run the FastAPI application using Uvicorn
    run(app, host="0.0.0.0", port=8000)


# ========================CORS========================


# **WARNING** : Edit CORS authorizations, handle data
# with caution. This works for local tests but read docs
# before pushing anything in production :
# https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Defining CORS for WSGI Application needs. Useful to
# manage what FastAPI doesn't handle such as
# non-standard requests
def application(env, start_response):
    if env["REQUEST_METHOD"] == "OPTIONS":
        start_response(
            "200 OK",
            [
                ("Content-Type", "application/json"),
                ("Access-Control-Allow-Origin", "*"),
                ("Access-Control-Allow-Headers", "Authorization, Content-Type"),
                ("Access-Control-Allow-Methods", "POST"),
            ],
        )
    return ""
