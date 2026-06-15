import subprocess
from celery import Celery

# Connect Celery to your local Redis container
celery_app = Celery(
    "deployments",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def deploy_to_kind(yaml_content: str):
    """
    Takes the generated Kubernetes YAML and applies it to the local Kind cluster.
    """
    # 1. Write the YAML to a temporary file
    temp_filename = "temp_manifest.yaml"
    with open(temp_filename, "w") as f:
        f.write(yaml_content)
        
    # 2. Execute kubectl to apply the file
    try:
        print("Executing deployment to Kind cluster...")
        result = subprocess.run(
            ["kubectl", "apply", "-f", temp_filename],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Deployment Success:\n{result.stdout}")
        return {"status": "success", "logs": result.stdout}
        
    except subprocess.CalledProcessError as e:
        print(f"Deployment Failed:\n{e.stderr}")
        return {"status": "error", "logs": e.stderr}