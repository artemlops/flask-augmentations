from collections import namedtuple
from typing import Dict

import albumentations as A
import numpy as np
import PIL.Image
import pytest

from mymodel.image_augmentations import (
    apply_augmentation,
    apply_random_augmentations,
    create_transform,
    get_composite_transform_info,
    get_random_transform_classes,
)


_Transform = namedtuple("_Transform", "name, typ, p, kwargs")


@pytest.fixture()
def image() -> PIL.Image.Image:
    img_np = np.ones((128, 128, 3), dtype=np.uint8)
    img = PIL.Image.fromarray(img_np)
    return img


@pytest.mark.parametrize(
    "name, typ, p, kwargs",
    [
        _Transform(
            name="Rotate",
            typ=A.Rotate,
            p=0.6,
            kwargs={"limit": (-50, 40)},
        ),
        _Transform(
            name="ShiftScaleRotate",
            typ=A.ShiftScaleRotate,
            p=0.6,
            kwargs={},
        ),
        _Transform(
            name="HorizontalFlip",
            typ=A.HorizontalFlip,
            p=0.5,
            kwargs={},
        ),
        _Transform(name="VerticalFlip", typ=A.VerticalFlip, p=0.7, kwargs={}),
        _Transform(
            name="RandomBrightnessContrast",
            typ=A.RandomBrightnessContrast,
            p=0.8,
            kwargs={"brightness_limit": (-40, 40)},
        ),
    ],
)
def test_create_transform__ok(name: str, typ, p: float, kwargs: Dict):
    """
    This test checks that the function `create_transform` actually
    creates a proper augmentation transform and that the parameters
    passed in `p` and `kwargs` are actually passed to the constructor.
    """
    t = create_transform(name, p=p, **kwargs)
    assert isinstance(t, typ)
    assert t.get_base_init_args() == {"always_apply": False, "p": p}
    init_args = t.get_transform_init_args()
    # print(init_args)
    for k, v in kwargs.items():
        assert init_args[k] == v, (k, v)


def test_create_transform__invalid_name():
    with pytest.raises(ValueError, match="Invalid transform name"):
        create_transform("invalid", p=1.0)


def test_create_transform__invalid_p_too_big():
    with pytest.raises(ValueError, match="must be a valid probability"):
        create_transform("Rotate", p=100500)


def test_create_transform__invalid_p_too_small():
    with pytest.raises(ValueError, match="must be a valid probability"):
        create_transform("Rotate", p=-1)


def get_random_transform_classes__ok():
    classes = get_random_transform_classes(n_max=4)
    assert len(classes) <= 4
    assert all(isinstance(t, A.BaseTransform) for t in classes)


def test_apply_augmentation__ok_shape(image: PIL.Image.Image):
    t = A.Compose([create_transform("GaussNoise", p=1.0)])
    image2 = apply_augmentation(image, t)
    assert isinstance(image2, PIL.Image.Image)
    assert image2.size == image.size


def test_apply_random_augmentations__ok_shape(image: PIL.Image.Image):
    N = 4
    image2, info = apply_random_augmentations(image, n=N)

    assert isinstance(image2, PIL.Image.Image)
    assert image2.size == image.size

    assert len(info) == N
    assert all(t["name"] for t in info)


def test_get_composite_transform_info__ok():
    t = A.Compose([create_transform("GaussNoise", p=1.0)])
    info = get_composite_transform_info(t)
    assert info == [
        {
            "name": "GaussNoise",
            "always_apply": False,
            "p": 1.0,
            "var_limit": (50, 150),
            "per_channel": True,
            "mean": 0,
        }
    ], info
