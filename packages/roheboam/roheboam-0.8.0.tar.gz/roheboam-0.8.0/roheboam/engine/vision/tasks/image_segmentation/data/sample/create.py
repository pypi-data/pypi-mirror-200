import torch
import torch.utils

from ......vision.utils.image import imread_grayscale, imread_rgb
from .sample import ImageSegmentationSample


def create_image_segmentation_sample(
    image_data=None,
    image_path=None,
    load_image_fn=imread_rgb,
    mask_data=None,
    mask_path=None,
    load_mask_fn=imread_grayscale,
    weight_map_data=None,
    weight_map_path=None,
    load_weight_map_fn=None,
    name=None,
):
    return ImageSegmentationSample.create(
        image_data=image_data,
        image_path=image_path,
        load_image_fn=load_image_fn,
        mask_data=mask_data,
        mask_path=mask_path,
        load_mask_fn=load_mask_fn,
        weight_map_data=weight_map_data,
        weight_map_path=weight_map_path,
        load_weight_map_fn=load_weight_map_fn,
        name=name,
    )


lookup = {"create_image_segmentation_sample": create_image_segmentation_sample}
