from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from collections import Counter
import subprocess
import shutil
import ast
import os

app = FastAPI()

BASE_DIR = Path("repos")
BASE_DIR.mkdir(exist_ok=True)


class RepoRequest(BaseModel):
    repo_url: str


# ----------------------------
# Clone Repository
# ----------------------------
@app.post("/repos")
def clone_repo(data: RepoRequest):

    repo_name = data.repo_url.split("/")[-1].replace(".git", "")
    repo_path = BASE_DIR / repo_name

    if repo_path.exists():
        return {
            "status": "exists",
            "repo": repo_name,
            "path": str(repo_path)
        }

    try:
        subprocess.run(
            ["git", "clone", data.repo_url, str(repo_path)],
            check=True
        )

        return {
            "status": "cloned",
            "repo": repo_name,
            "path": str(repo_path)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------
# List Files
# ----------------------------
@app.get("/repos/{repo_name}/files")
def list_files(repo_name: str):

    repo_path = BASE_DIR / repo_name

    if not repo_path.exists():
        raise HTTPException(status_code=404, detail="Repository not found")

    files = []

    for path in repo_path.rglob("*"):
        if path.is_file():
            files.append(str(path.relative_to(repo_path)))

    return {
        "status": "success",
        "repo": repo_name,
        "total_files": len(files),
        "files": files
    }


# ----------------------------
# Analyze Repository
# ----------------------------
@app.get("/repos/{repo_name}/analyze")
def analyze_repo(repo_name: str):

    repo_path = BASE_DIR / repo_name

    if not repo_path.exists():
        raise HTTPException(status_code=404, detail="Repository not found")

    py_files = list(repo_path.rglob("*.py"))

    functions = []
    classes = []
    imports = []
    endpoints = []
    language_counter = Counter()

    important_files = []

    framework = "unknown"

    for file in repo_path.rglob("*"):

        if file.is_file():

            language_counter[file.suffix] += 1

            if file.name.lower() in [
                "requirements.txt",
                "package.json",
                "dockerfile",
                "docker-compose.yml",
                "README.md",
                "pyproject.toml"
            ]:
                important_files.append(str(file.relative_to(repo_path)))

    for py_file in py_files:

        try:
            code = py_file.read_text(encoding="utf-8")

            tree = ast.parse(code)

            for node in ast.walk(tree):

                # Functions
                if isinstance(node, ast.FunctionDef):

                    functions.append({
                        "name": node.name,
                        "line": node.lineno
                    })

                # Classes
                elif isinstance(node, ast.ClassDef):

                    classes.append({
                        "name": node.name,
                        "line": node.lineno
                    })

                # Imports
                elif isinstance(node, ast.Import):

                    for n in node.names:
                        imports.append(n.name)

                elif isinstance(node, ast.ImportFrom):

                    if node.module:
                        imports.append(node.module)

                # FastAPI Endpoints
                elif isinstance(node, ast.FunctionDef):

                    for deco in node.decorator_list:

                        if isinstance(deco, ast.Call):

                            if hasattr(deco.func, "attr"):

                                method = deco.func.attr.upper()

                                if method in [
                                    "GET",
                                    "POST",
                                    "PUT",
                                    "DELETE",
                                    "PATCH"
                                ]:

                                    endpoint = ""

                                    if deco.args:
                                        if isinstance(deco.args[0], ast.Constant):
                                            endpoint = deco.args[0].value

                                    endpoints.append({
                                        "method": method,
                                        "endpoint": endpoint,
                                        "function": node.name
                                    })

        except Exception:
            continue

    # Detect Framework
    imports_text = " ".join(imports).lower()

    if "fastapi" in imports_text:
        framework = "FastAPI"

    elif "flask" in imports_text:
        framework = "Flask"

    elif "django" in imports_text:
        framework = "Django"

    # Detect Project Type
    project_type = "unknown"

    if framework != "unknown":
        project_type = f"{framework} API Project"

    elif any(".js" == ext for ext in language_counter):
        project_type = "JavaScript Project"

    elif any(".py" == ext for ext in language_counter):
        project_type = "Python Project"

    summary = {
        "project_type": project_type,
        "framework": framework,
        "files_scanned": len(py_files),
        "functions_found": len(functions),
        "classes_found": len(classes),
        "api_endpoints_found": len(endpoints),
        "main_languages": dict(language_counter.most_common(5)),
        "important_files": important_files[:10],
    }

    return {
        "status": "success",
        "repo": repo_name,
        "analysis": {
            "functions": functions[:50],
            "classes": classes[:50],
            "imports": list(set(imports))[:50],
            "languages": dict(language_counter),
            "important_files": important_files,
            "project_type": project_type,
            "framework": framework,
            "files_scanned": len(py_files),
            "summary": summary,
            "endpoints": endpoints[:50]
        }
    }
