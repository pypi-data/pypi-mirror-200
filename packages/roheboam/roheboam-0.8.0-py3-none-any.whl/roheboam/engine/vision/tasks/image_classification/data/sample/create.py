import numpy as np

from ......vision.utils import imread_rgb
from .sample import ImageClassificationSample


def create_image_classification_sample(
    image_data=None,
    image_path=None,
    load_image_fn=imread_rgb,
    label_data=None,
    label_path=None,
    load_label_fn=np.load,
    name=None,
):
    return ImageClassificationSample.create(
        image_data=image_data,
        image_path=image_path,
        load_image_fn=load_image_fn,
        label_data=label_data,
        label_path=label_path,
        load_label_fn=load_label_fn,
        name=name,
    )


lookup = {"create_image_classification_sample": create_image_classification_sample}
