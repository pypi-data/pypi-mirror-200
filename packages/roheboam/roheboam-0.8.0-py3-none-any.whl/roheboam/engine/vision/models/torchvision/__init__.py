from torchvision.models.detection import fasterrcnn_resnet50_fpn, fcos_resnet50_fpn, retinanet_resnet50_fpn_v2

lookup = {
    "fasterrcnn_resnet50_fpn": fasterrcnn_resnet50_fpn,
    "fcos_resnet50_fpn": fcos_resnet50_fpn,
    "retinanet_resnet50_fpn_v2": retinanet_resnet50_fpn_v2,
}
