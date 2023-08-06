import docker


def run_mlflow_model_image(image, port="5000", gpus=None):
    client = docker.from_env()
    run_params = {"image": image, "ports": {"5000/tcp": str(port)}, "detach": True}
    if gpus is not None:
        run_params["runtime"] = "nvidia"
    container = client.containers.run(**run_params)
    return container


def run_seldon_model_image(image, rest_port="9000", grpc_port="5000", gpus=None):
    client = docker.from_env()
    run_params = {
        "image": image,
        "ports": {"9000/tcp": str(rest_port), "5000/tcp": str(grpc_port)},
        "detach": True,
    }
    if gpus is not None:
        run_params["runtime"] = "nvidia"
    container = client.containers.run(**run_params)
    return container
