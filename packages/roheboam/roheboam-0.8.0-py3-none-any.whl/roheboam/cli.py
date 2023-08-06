import click
import mlflow
from mlflow.pyfunc.scoring_server import init

from roheboam.engine import get_toolbox_lookup
from roheboam.engine.integrations.mlflow.saving import save_mlflow_pyfunc_model
from roheboam.engine.pipeline import Pipeline
from roheboam.engine.pipeline.config_loader import load_config_from_path
from roheboam.engine.pipeline.constants import VARIABLE_KEY
from roheboam.engine.vision.deployment import run_seldon_image_model_server


@click.group()
def cli():
    pass


# Before are the commands that the server will call indirectly through
# Docker CLI through the endpoint defined by the application hosted
@click.command()
@click.option("--config_path")
@click.option("--root_save_directory")
@click.option("--gpus", default=None)
def train(config_path, root_save_directory, gpus):

    config = load_config_from_path(config_path)
    config[VARIABLE_KEY]["root_save_directory"] = root_save_directory
    config[VARIABLE_KEY]["gpus"] = gpus
    lookup = get_toolbox_lookup()
    pipeline = Pipeline.create_from_config(config, lookup)
    pipeline.run()

    train_sample_idx, val_sample_idx = next(
        iter(pipeline.get_node_output("DataSplitCreator")().split())
    )
    try:
        train_samples = pipeline.get_node_output("TrainSampleDataCreator")[
            train_sample_idx
        ]
    except KeyError:
        train_samples = pipeline.get_node_output("TrainSamples")[train_sample_idx]

    try:
        val_samples = pipeline.get_node_output("TrainSampleDataCreator")[val_sample_idx]
    except KeyError:
        val_samples = pipeline.get_node_output("TrainSamples")[val_sample_idx]

    try:
        test_samples = pipeline.get_node_output("TestSampleDataCreator")
    except KeyError:
        test_samples = pipeline.get_node_output("TestSamples")

    module = pipeline.get_node_output("ModuleCreator")(
        train_samples=train_samples, val_samples=val_samples, test_samples=test_samples
    )

    checkpoint_callback = pipeline.get_node_output("PyTorchLightningModelCheckpoint")
    trainer = pipeline.get_node_output("TrainerCreator")(
        checkpoint_callback=checkpoint_callback
    )
    trainer.fit(module)

    mlflow_save_path = pipeline.get_node_output("TimeStampedSavePath") / "mlflow"
    save_mlflow_pyfunc_model(
        mlflow_save_path,
        pipeline.get_node_output("ServingModel"),
        artifacts={
            "config_path": str(checkpoint_callback.best_config_path),
            "model_save_path": str(checkpoint_callback.best_model_path),
        },
    )


@click.command()
@click.option("--model_path")
@click.option("--model_format")
@click.option("--debug", is_flag=True)
def serve(model_path, model_format, debug):
    assert model_path is not None, "No model path is specified"
    if model_format == "mlflow":
        model = mlflow.pyfunc.load_model(str(model_path))
        app = init(model)
        app.run(host="0.0.0.0", debug=debug)

    if model_format == "seldon":
        with run_seldon_image_model_server(model_path, debug):
            pass


cli.add_command(train)
cli.add_command(serve)

if __name__ == "__main__":
    cli()
