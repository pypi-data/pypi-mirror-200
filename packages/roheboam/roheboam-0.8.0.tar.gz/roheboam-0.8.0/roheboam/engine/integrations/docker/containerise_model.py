import importlib.util
import shutil
import tempfile
from pathlib import Path
from textwrap import dedent

from ...logger import logger
from ..docker.utils import build_image


def containerise_model(
    model_path,
    model_format,
    model_image_name,
    build_env_image,
    dev_build=False,
    conda_env_file_path=None,
):
    if dev_build and (conda_env_file_path is None):
        raise ValueError(
            "There must be a conda_lock_file_path and poetry_lock_file_path if dev_build is enabled"
        )

    with tempfile.TemporaryDirectory() as temp_dir:
        if dev_build:
            logger.info("Copying roheboam source to build directory")
            _copy_roheboam(temp_dir)
            _copy_dependency_files(temp_dir, conda_env_file_path)

        logger.info(f"Copying model from {model_path} to build directory")
        _copy_model(model_path, temp_dir)

        logger.info(f"Creating Docker file")
        docker_file = _create_docker_file(
            model_path, model_format, build_env_image, dev_build
        )

        logger.info(f"Writing Docker file")
        _write_docker_file(docker_file, temp_dir)

        logger.info(f"Building image at {temp_dir}")
        image = build_image(model_image_name, temp_dir)

        return image


def _copy_model(model_path, save_path):
    shutil.copytree(model_path, f"{save_path}/{model_path.name}")


def _copy_roheboam(save_path):
    roheboam_project_path = Path(
        importlib.util.find_spec("roheboam").origin
    ).parent.parent
    shutil.copytree(
        roheboam_project_path / "roheboam", f"{save_path}/roheboam/roheboam"
    )


def _copy_dependency_files(save_path, conda_env_file_path):
    roheboam_project_path = Path(
        importlib.util.find_spec("roheboam").origin
    ).parent.parent
    shutil.copy2(roheboam_project_path / "setup.py", f"{save_path}/setup.py")
    shutil.copy2(conda_env_file_path, f"{save_path}/environment.yml")


def _create_docker_file(model_path, model_format, build_env_image, dev_build):
    docker_template = dedent(
        f"""
        FROM {build_env_image}
        RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install \
            'ffmpeg'\
            'libsm6' \
            'libxext6' \
            'libvips-dev' -y
        ENV SSL_CERT_DIR=/etc/ssl/certs
        """
    )

    if dev_build:
        docker_template += dedent(
            f"""
            WORKDIR /home/build/conda
            RUN conda create -n roheboam
            RUN conda install mamba -n base -c conda-forge
            RUN conda config --set channel_priority false
            COPY environment.yml /home/build/conda/environment.yml
            RUN mamba env update -n roheboam --file environment.yml
            ENV PATH="/opt/conda/envs/roheboam/bin:$PATH"
            """
        )

        docker_template += dedent(
            f"""
            COPY ./roheboam /home/build/roheboam
            COPY setup.py /home/build/roheboam/setup.py
            WORKDIR /home/build/roheboam
            RUN python setup.py install
            """
        )

    docker_template += dedent(
        f"""
            RUN mkdir -p /home/model
            WORKDIR /home/model
            COPY {model_path.name} /home/model
            RUN mkdir -p /home/.cache
            ENV TORCH_HOME=/home/.cache
            RUN chmod -R 777 /home
        """
    )

    if model_format == "MLFLOW":
        docker_template += dedent(
            f"""
           CMD exec roheboam serve --model_path /home/model --model_format mlflow
        """
        )

    if model_format == "SELDON":
        docker_template += dedent(
            f"""
            # Port for GRPC
            EXPOSE 5000
            # Port for REST
            EXPOSE 9000

            # Define environment variables
            ENV MODEL_NAME roheboam.engine.vision.SeldonImageModel
            ENV SERVICE_TYPE MODEL
            ENV SELDON_MODEL_PATH /home/model
            ENV FLASK_SINGLE_THREADED 1
            CMD exec roheboam serve --model_path /home/model --model_format seldon --debug
        """
        )
    return docker_template


def _write_docker_file(docker_file, save_path):
    with (Path(save_path) / "Dockerfile").open("w") as f:
        f.write(docker_file)
