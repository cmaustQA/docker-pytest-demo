import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class UserRequest(BaseModel):
    username: str

@app.get("/")
def read_root():
    return {"status": "online", "service": "github-analyzer"}

@app.post("/analyze_user")
async def analyze_user(request: UserRequest):
    if not request.username:
        raise HTTPException(status_code=400, detail="Username cannot be empty")
        
    github_url = f"https://api.github.com/users/{request.username}"
    

    # async client so the server doesn't freeze while waiting for GitHub
    async with httpx.AsyncClient() as client:
        response = await client.get(github_url)
    
    # Upstream Error Handling
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="User not found on GitHub")
    if response.status_code != 200:
        raise HTTPException(status_code=503, detail="GitHub API unavailable")

    data = response.json()
    
    # Grade the user
    public_repos = data.get("public_repos", 0)
    followers = data.get("followers", 0)
    
    grade = "Junior"
    if public_repos > 10 and followers > 5:
        grade = "Senior"
    if public_repos > 50:
        grade = "Rockstar"

    return {
        "username": request.username,
        "stats": {
            "repos": public_repos,
            "followers": followers
        },
        "assessed_grade": grade
    }