# Setup
## Setup with Conda

### To create the environment (from scratch)
```
conda create -n roheboam python=3.10
mamba install mamba -n roheboam -c conda-forge
conda activate roheboam
mamba install pytorch=1.12.1 torchvision cudatoolkit -c pytorch -y
mamba install -c conda-forge jupyterlab jupyterlab_vim ipywidgets jupyterlab_code_formatter black isort albumentations=1.3.0 mlflow=1.29.0 pretrainedmodels=0.7.4 matplotlib=3.6.0 p-tqdm=1.4.0 click=8.0.4 pytorch-lightning=1.6.4 -y

pip install pre-commit pytest pytest-only pytest-mock python-semantic-release nbdev==1.2.2 pytest-custom-exit-code docker seldon-core==1.4.0
pre-commit install --hook-type commit-msg # this is for commitizen to work
pre-commit install --hook-type pre-push # this is for a pytest on push to work
```

### From existing environment.yml
```
conda create -n roheboam && conda config --set channel_priority false && mamba env update -n roheboam --file environment.yml
```

### To update the environment
Here we are taking inspiration from [https://stackoverflow.com/questions/70851048/does-it-make-sense-to-use-conda-poetry](here) whereby lock files are used to ensure reproducible environments. Poetry and Conda are used together, Poetry is the first choice, if there is a package or a binary that Poetry does not provide, then Conda is used.
```
# Re-generate Conda lock file(s) based on environment.yml
conda-lock lock -k explicit --conda mamba

# Update Conda packages based on re-generated lock file
mamba update --file conda-linux-64.lock

# Update Poetry packages and re-generate poetry.lock
poetry update
```

### To test in the environment:
```
PYTHONPATH=. pytest examples --ignore examples/instant_nerf
```

## Setup with Docker dev container
### To create new environment for usage (for example inside a Docker container)
```
# If mamba doesn't exist in root environment
conda install mamba -n base -c conda-forge
mamba create --name my_project_env --file conda-linux-64.lock
mamba activate my_project_env
poetry install
```

### Setup Docker development environment
`docker build . -f Dockerfile.dev -t roheboam-dev-container`
`docker run -itd --mount 'type=bind,src=$(pwd),dst=/app'`

For example:
```
docker build . -f Dockerfile.dev -t roheboam-dev-container && \
docker run -itd \
    --runtime=nvidia \
    --shm-size 64G \
    --mount 'type=bind,src=/home/kevin/Documents/Projects/roheboam,dst=/app' \
    roheboam-dev-container
```

### Run Docker image for Instant Nerf endpoint
`docker build . -f examples/instant_nerf/Dockerfile -t roheboam-instant-nerf-dev-container`
`docker run -itd --mount 'type=bind,src=$(pwd),dst=/app'`

For example:
```
docker build . -f examples/instant_nerf/Dockerfile.dev -t roheboam-instant-nerf-dev-container && \
docker run -itd \
    --runtime=nvidia \
    --shm-size 64G \
    --mount 'type=bind,src=/home/kevin/Documents/Projects/roheboam,dst=/app' \
    roheboam-instant-nerf-dev-container
```


### k8s debugging commands
When trying to figure out what has happened to a `SeldonDeployment`
`kubectl describe seldondeployments {seldon_deployment_name} -n seldon`

Describe pod
`kubectl describe pod {pod_name} -n seldon`


# To push
`SKIP=black,isort,pytest-for-examples PYTHONPATH=. git push origin $(git rev-parse --abbrev-ref HEAD) --force`

```
[WARNING] Stashed changes conflicted with hook auto-fixes... Rolling back fixes...
[INFO] Restored changes from /home/kevin/.cache/pre-commit/patch1680414974-21813.
```
### WARNING
Note here that the image tag is hard coded as `roheboam-instant-nerf`

wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py39_4.10.3-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc
export PATH=/opt/conda/bin:$PATH
conda create -n roheboam -y
conda install mamba -n base -c conda-forge
conda config --set channel_priority false
mamba env update -n roheboam --file environment.yml
export PATH="/opt/conda/envs/roheboam/bin:$PATH"
