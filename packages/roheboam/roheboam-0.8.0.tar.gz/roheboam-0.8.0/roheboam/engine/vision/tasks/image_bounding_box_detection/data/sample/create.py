from ......vision.utils import imread_rgb
from .sample import ImageBoundingBoxDetectionSample


def create_image_bboxes_detection_sample(
    image_data=None,
    image_path=None,
    load_image_fn=imread_rgb,
    labels_data=None,
    labels_path=None,
    load_labels_fn=None,
    bboxes_data=None,
    bboxes_path=None,
    load_bboxes_fn=None,
    bboxes_format=None,
    transform_to_bboxes_format=None,
    labels_to_keep=None,
    transform_label_map=None,
    name=None,
):
    """Filtering is done first, hence the label map should be using the original labels

    Args:
        image_data (_type_, optional): _description_. Defaults to None.
        image_path (_type_, optional): _description_. Defaults to None.
        load_image_fn (_type_, optional): _description_. Defaults to imread_rgb.
        labels_data (_type_, optional): _description_. Defaults to None.
        labels_path (_type_, optional): _description_. Defaults to None.
        load_labels_fn (_type_, optional): _description_. Defaults to None.
        bboxes_data (_type_, optional): _description_. Defaults to None.
        bboxes_path (_type_, optional): _description_. Defaults to None.
        load_bboxes_fn (_type_, optional): _description_. Defaults to None.
        bboxes_format (_type_, optional): _description_. Defaults to None.
        transform_to_bboxes_format (_type_, optional): _description_. Defaults to None.
        labels_to_keep (_type_, optional): _description_. Defaults to None.
        transform_label_map (_type_, optional): _description_. Defaults to None.
        name (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    sample = ImageBoundingBoxDetectionSample.create(
        image_data,
        image_path,
        load_image_fn,
        labels_data,
        labels_path,
        load_labels_fn,
        bboxes_data,
        bboxes_path,
        load_bboxes_fn,
        bboxes_format,
        name,
    )

    if transform_to_bboxes_format == "PASCAL_VOC":
        sample.convert_to_pascal_voc_bboxes(lazy=True)

    if labels_to_keep is not None:
        sample.filter_labels_and_bboxes_to_keep(labels_to_keep, lazy=True)

    if transform_label_map is not None:
        sample.transform_labels(transform_label_map, lazy=True)

    return sample


lookup = {"create_image_bboxes_detection_sample": create_image_bboxes_detection_sample}
