import os
import traceback
from contextlib import ContextDecorator
from typing import Dict, Iterable, List, Optional, Union

import numpy as np

from ...logger import logger


class run_seldon_image_model_server(ContextDecorator):
    def __init__(self, model_path, debug=False, background_process=False):
        self.model_path = model_path
        self.debug = debug
        self.background_process = background_process

    def __enter__(self):
        cmd = "seldon-core-microservice roheboam.engine.vision.SeldonImageModel --service-type MODEL"
        if self.debug:
            cmd += " --debug"
        os.environ["SELDON_MODEL_PATH"] = self.model_path
        from ...utils.convenience import run_shell_command

        run_shell_command(cmd, background_process=self.background_process)

    def __exit__(self, *exc):
        print("Exiting")
        del os.environ["SELDON_MODEL_PATH"]


class SeldonImageModel:
    def __init__(self):
        self.loaded = False
        pass

    def load(self):
        import mlflow
        import numpy as np
        from pytorch_lightning.utilities.cloud_io import load as pl_load

        from ....engine import get_toolbox_lookup

        mlflow_model = mlflow.pyfunc.load_model(
            os.environ.get("SELDON_MODEL_PATH", str("/model"))
        )
        context = mlflow_model._model_impl.context

        self.lookup = get_toolbox_lookup()
        self.config = self.lookup["load_config_from_path"](
            context.artifacts["config_path"]
        )
        self.config["Variables"]["is_deployed"] = True
        self.pipeline = self.lookup["Pipeline"].create_from_config(
            self.config, self.lookup
        )
        self.pipeline.run(remove_nodes_with_tags=["TRAIN"])
        self.module = self.pipeline.get_node_output("ModuleCreator")()
        self.trainer = self.pipeline.get_node_output("TrainerCreator")()
        self.inference_recorder = self.pipeline.get_node_output("InferenceRecorder")
        pl_checkpoint = pl_load(
            context.artifacts["model_save_path"],
            map_location=lambda storage, loc: storage,
        )
        self.module.load_state_dict(pl_checkpoint["state_dict"])
        self.loaded = True

    def predict(
        self, X: np.ndarray, names: Optional[List[str]], meta: Dict = None
    ) -> Union[np.ndarray, List, str, bytes]:
        try:
            samples_data = [
                {"image_data": self.lookup["to_uint8_image"](image)} for image in X
            ]
            samples = [
                self.pipeline.get_node_output("SampleFromDataCreator")(**sample_data)
                for sample_data in samples_data
            ]
            test_dataset = self.pipeline.get_node_output("TestDatasetCreator")(
                samples=samples
            )
            test_dataloader = self.pipeline.get_node_output("TestDataLoaderCreator")(
                test_dataset
            )
            self.trainer.test(self.module, dataloaders=[test_dataloader])
            predictions = self.inference_recorder.serializable_results
            self.inference_recorder.flush_results()
            return predictions
        except Exception:
            logger.error(traceback.format_exc())

    def health_status(self):
        assert self.loaded, "Model is not loaded"
        return ["Success"]


lookup = {
    "SeldonImageModel": SeldonImageModel,
    "run_seldon_image_model_server": run_seldon_image_model_server,
}
