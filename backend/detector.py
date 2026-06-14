import requests
from pydantic import BaseModel
from typing import Optional

class StackInfo(BaseModel):
    runtime: str
    framework: str
    port: Optional[int]

def detect_stack(repo_url: str):
    try:
        # Extract owner and repo from the URL (e.g., https://github.com/owner/repo)
        parts = repo_url.rstrip('/').split('/')
        owner, repo = parts[-2], parts[-1]
        
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        
        # Standard unauthenticated request
        headers = {
            "Accept": "application/vnd.github.v3+json"
        }

        response = requests.get(api_url, headers=headers)
        
        # Handle specific GitHub API errors
        if response.status_code == 403 or response.status_code == 429:
             return {"error": "GitHub API rate limit hit (60 requests/hr). Please wait or add a token later."}
        elif response.status_code == 404:
             return {"error": "Repository not found. Ensure the URL is correct and the repository is public."}
        elif response.status_code != 200:
            return {"error": f"Could not fetch repo contents. GitHub returned status {response.status_code}."}

        # Parse the JSON response
        contents = [item['name'] for item in response.json()]
        
        # Your stack detection logic
        if "package.json" in contents:
            return StackInfo(runtime="node", framework="express/next", port=3000)
        elif "requirements.txt" in contents or "pyproject.toml" in contents:
            return StackInfo(runtime="python", framework="fastapi/django", port=8000)
        elif "go.mod" in contents:
            return StackInfo(runtime="go", framework="generic", port=8080)
        elif "Dockerfile" in contents:
            return StackInfo(runtime="docker", framework="custom", port=None)
            
        return {"error": "Stack not recognized. No package.json, requirements.txt, or Dockerfile found."}
        
    except Exception as e:
        return {"error": f"Internal detection error: {str(e)}"}