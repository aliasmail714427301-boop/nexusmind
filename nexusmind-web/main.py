from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoRequest(BaseModel):
    repo_url: str

@app.get("/")
def root():
    return {"message": "NexusMind API Running"}

@app.post("/repos")
def clone_repo(data: RepoRequest):
    repo_name = data.repo_url.split("/")[-1]

    if os.path.exists(repo_name):
        return {
            "status": "already_exists",
            "repo": repo_name
        }

    try:
        subprocess.run(
            ["git", "clone", data.repo_url],
            check=True
        )

        return {
            "status": "success",
            "repo": repo_name
        }

    except Exception as e:
        return {
            "status": "error",
            "detail": str(e)
        }
