import mlflow
from pytorch_lightning.utilities.cloud_io import load as pl_load

from ....engine import get_toolbox_lookup


class MLFlowImageModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
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

    def predict(self, context, model_input):
        if "images" in model_input:
            samples_data = [
                {"image_data": self.lookup["to_uint8_image"](image)}
                for image in model_input["images"]
            ]
        if "image_paths" in model_input:
            samples_data = [
                {
                    "image_data": self.lookup["to_uint8_image"](
                        self.lookup["imread_rgb"](image_path)
                    )
                }
                for image_path in model_input["image_paths"]
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
        predictions = self.inference_recorder.results
        self.inference_recorder.flush_results()
        return predictions


lookup = {"MLFlowImageModel": MLFlowImageModel}
