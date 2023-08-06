from itertools import repeat

import numpy as np
from p_tqdm import p_map

from ..data import create_image_segmentation_sample


def create_image_segmentation_samples_data_from_paths(
    image_paths, mask_paths=None, weight_map_paths=None
):
    stringify = lambda l: [str(e) for e in l]
    image_paths = stringify(image_paths)
    mask_paths = repeat(None) if mask_paths is None else stringify(mask_paths)
    weight_map_paths = (
        repeat(None) if weight_map_paths is None else stringify(weight_map_paths)
    )
    return np.array(
        [
            {
                "image_path": image_path,
                "mask_path": mask_path,
                "weight_map_path": weight_map_path,
            }
            for image_path, mask_path, weight_map_path in zip(
                image_paths, mask_paths, weight_map_paths
            )
        ]
    )


def create_image_segmentation_samples_from_paths(
    image_paths, mask_paths=None, weight_map_paths=None
):
    samples = p_map(
        _create_image_segmentation_sample_lambda,
        create_image_segmentation_samples_data_from_paths(
            image_paths, mask_paths, weight_map_paths
        ),
    )
    return np.array(samples)


def _create_image_segmentation_sample_lambda(sample_data):
    return create_image_segmentation_sample(**sample_data)


lookup = {
    "create_image_segmentation_samples_data_from_paths": create_image_segmentation_samples_data_from_paths,
    "create_image_segmentation_samples_from_paths": create_image_segmentation_samples_from_paths,
}
