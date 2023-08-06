import docker

from ....engine.utils.convenience import run_shell_command


def stream_docker_logs(log_generator):
    while True:
        try:
            output = log_generator.__next__()
            if "stream" in output:
                output_str = output["stream"].strip("\r\n").strip("\n")
                print(output_str)
        except StopIteration:
            print("Docker image build complete.")
            break
        except ValueError:
            print(f"Error parsing output from docker image build: {output}")


def remove_image(image, force=True, no_prune=False):
    client = docker.from_env()
    client.images.remove(image=image, force=force, noprune=no_prune)


def build_image(image_tag, context_path, docker_file_path=None):
    # client = docker.from_env()
    # image, log_generator = client.images.build(path=docker_file_path, tag=image_tag)
    # stream_docker_logs(log_generator)

    # Have to use this workaround or the layers won't cache for some reason...
    build_command = ["docker", "build", str(context_path), "-t", str(image_tag)]

    if docker_file_path is not None:
        build_command += ["-f", str(docker_file_path)]
    run_shell_command(" ".join(build_command))
