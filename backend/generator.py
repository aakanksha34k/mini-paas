import os
from jinja2 import Environment, FileSystemLoader

# Tell Jinja2 to look inside your 'templates' folder
env = Environment(loader=FileSystemLoader('templates'))

def generate_k8s_manifest(stack_info, repo_url):
    # Extract a simple, lowercase app name from the end of the GitHub URL
    app_name = repo_url.rstrip('/').split('/')[-1].lower()
    
    # Load your blueprint
    template = env.get_template('deployment.yaml.j2')
    
    # Render the template by injecting our Python variables into the Jinja2 {{ tags }}
    # Note: stack_info is a Pydantic model here, so we access the port using dot notation
    rendered_yaml = template.render(
        app_name=app_name,
        image_name=f"{app_name}:latest",
        port=stack_info.port
    )
    
    # Save the dynamically generated manifest to a physical file
    output_filename = f"{app_name}-k8s.yaml"
    with open(output_filename, "w") as f:
        f.write(rendered_yaml)
        
    return rendered_yaml, output_filename