import docker


def create_detached_container(image_name, container_name):
    client = docker.from_env()
    container = client.containers.run(image_name, detach=True, name=container_name)
    return container.id


# Example usage
image_name = "my-docker-image:latest"
container_name = "Tool-123"
container_id = create_detached_container(image_name, container_name)
print(f"Created detached container with ID: {container_id}")


# Build Docker images
image_names = ["Red", "Green", "Blue"]

client = docker.from_env()  # Add this line to define the 'client' variable
for image_name in image_names:
    client.images.build(path="path/to/dockerfile", tag=image_name)

"""
# Docker Compose YAML file example
version: '3'
services:
    red:
        build:
            context: ./path/to/red
            dockerfile: Dockerfile
    green:
        build:
            context: ./path/to/green
            dockerfile: Dockerfile
    blue:
        build:
            context: ./path/to/blue
            dockerfile: Dockerfile
"""
