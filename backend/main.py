from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import detector
import generator  # Import your new generation engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoRequest(BaseModel):
    url: str

@app.post("/detect")
async def process_repository(request: RepoRequest):
    # 1. Detect the Stack
    stack_data = detector.detect_stack(request.url)
    
    # If the detector hit a rate limit or bad URL, stop immediately and return the error
    if isinstance(stack_data, dict) and "error" in stack_data:
        return stack_data
        
    # 2. Generate the Infrastructure Code
    yaml_output, filename = generator.generate_k8s_manifest(stack_data, request.url)
    
    # 3. Return the complete package back to the React UI
    return {
        "status": "Infrastructure generated successfully!",
        "file_created": filename,
        "stack_detected": stack_data,
        "manifest_preview": yaml_output
    }