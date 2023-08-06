from pathlib import Path

import numpy as np
import torch
from tqdm import tqdm

from ..vendored.ngp_pl.datasets.color_utils import read_image
from ..vendored.ngp_pl.datasets.nsvf import NSVFDataset as ngp_pl_NSVFDataset
from ..vendored.ngp_pl.datasets.ray_utils import get_ray_directions


class NSVFDataset(ngp_pl_NSVFDataset):
    @staticmethod
    def create_shift_and_scale_from_bbox_path(bbox_path):
        xyz_min, xyz_max = np.loadtxt(str(bbox_path))[:6].reshape(2, 3)
        shift = (xyz_max + xyz_min) / 2
        scale = (xyz_max - xyz_min).max() / 2 * 1.05  # enlarge a little
        return shift, scale

    @staticmethod
    def create_rays_and_poses_from_paths(
        image_paths, pose_paths, shift, scale, image_width, image_height, downsample
    ):
        rays = []
        poses = []
        for img_path, pose in tqdm(zip(image_paths, pose_paths)):
            c2w = np.loadtxt(pose)[:3]
            c2w[:, 3] -= shift
            c2w[:, 3] /= 2 * scale  # to bound the scene inside [-0.5, 0.5]
            poses.append(c2w)
            img = read_image(
                img_path,
                (int(image_width * downsample), int(image_height * downsample)),
            )
            rays.append(img)
        rays = torch.FloatTensor(np.stack(rays))  # (N_images, hw, ?)
        poses = torch.FloatTensor(np.stack(poses))  # (N_images, 3, 4)

        return rays, poses

    @staticmethod
    def create_intrinsic_camera_matrix_from_path(
        path, image_width, image_height, downsample
    ):
        with Path(path).open("r") as f:
            fx = fy = float(f.readline().split()[0]) * downsample
        image_width *= downsample
        image_height *= downsample
        K = np.float32([[fx, 0, image_width / 2], [0, fy, image_height / 2], [0, 0, 1]])
        return K

    def __init__(
        self,
        rays,
        poses,
        K,
        image_width,
        image_height,
        batch_size,
        ray_sampling_strategy,
        split,
    ):
        self.rays = rays
        self.poses = poses
        self.K = torch.FloatTensor(K)
        self.directions = get_ray_directions(image_height, image_width, self.K)
        self.img_wh = (image_width, image_height)
        self.batch_size = batch_size
        self.ray_sampling_strategy = ray_sampling_strategy
        self.split = split


lookup = {"NSVFDataset": NSVFDataset}
