from pathlib import Path

import numpy as np
from p_tqdm import p_map

from .....vision.utils.image import imread_rgb
from ..data import create_image_classification_sample


def create_image_classification_samples_data_for_label_per_folder(
    root_label_folder, label_map, load_image_fn=imread_rgb
):
    arguments = []
    for label_folder in Path(root_label_folder).glob("*"):
        for image_path in Path(label_folder).glob("*"):
            arguments.append(
                {
                    "image_path": image_path,
                    "load_image_fn": load_image_fn,
                    "label_data": label_map[label_folder.name],
                }
            )

    return np.array(arguments)


def create_labels_from_sample_arguments_for_label_per_folder(sample_arguments):
    return sample_arguments, [s["label_data"] for s in sample_arguments]


def create_labels_from_samples(samples):
    return [s.label.data for s in samples]


def create_image_classification_samples_for_label_per_folder(
    root_label_folder, label_map, load_image_fn=imread_rgb
):
    samples = p_map(
        _create_image_classification_sample_lambda,
        create_image_classification_samples_data_for_label_per_folder(
            root_label_folder, label_map, load_image_fn
        ),
    )
    return np.array(samples)


def _create_image_classification_sample_lambda(sample_data):
    return create_image_classification_sample(**sample_data)


lookup = {
    "create_labels_from_samples": create_labels_from_samples,
    "create_image_classification_samples_for_label_per_folder": create_image_classification_samples_for_label_per_folder,
    "create_image_classification_samples_data_for_label_per_folder": create_image_classification_samples_data_for_label_per_folder,
    "create_labels_from_sample_arguments_for_label_per_folder": create_labels_from_sample_arguments_for_label_per_folder,
}
