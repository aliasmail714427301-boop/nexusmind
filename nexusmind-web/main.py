from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# تفعيل CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "NexusMind API Running 🚀"}

@app.post("/repos")
def clone_repo(data: dict):
    repo_url = data.get("repo_url")

    if not repo_url:
        return {"error": "repo_url required"}

    return {
        "success": True,
        "repo": repo_url,
        "message": "Repository received successfully ✅"
    }

@app.get("/repos/{repo_name}/files")
def list_files(repo_name: str):
    return {
        "repo": repo_name,
        "files": ["README.md", "package.json", "src/index.js"]
    }

@app.get("/repos/{repo_name}/analyze")
def analyze_repo(repo_name: str):
    return {
        "repo": repo_name,
        "analysis": "This repository uses React and modern frontend structure."
    }
