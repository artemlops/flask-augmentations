import albumentations as A
from typing import Dict
from PIL import Image
import PIL.Image
import io
import numpy as np
from mymodel.image_augmentations import (
    create_transform,
    DEFAULT_TRANSFORMS,
    get_random_transform_classes,
    get_composite_transform_info,
    apply_augmentation,
    apply_random_augmentations,
)
import pytest
from collections import namedtuple


_Transform = namedtuple("Transform", "name, typ, p, kwargs")


@pytest.fixture()
def image() -> Image:
    img_np = np.ones((128, 128, 3), dtype=np.uint8)
    img = Image.fromarray(img_np)
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
def test_create_transform__ok(name: str, typ: "Type", p: float, kwargs: Dict):
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
    transforms = get_random_transform_classes(n_max=4, p=0.75)
    assert len(names) <= 4
    assert all(isinstance(t, A.BaseTransform) for t in transforms)


def test_apply_augmentation__ok_shape(image: Image):
    t = A.Compose([create_transform("GaussNoise", p=1.0)])
    image2 = apply_augmentation(image, t)
    assert isinstance(image2, PIL.Image.Image)
    assert image2.size == image.size


def test_apply_random_augmentations__ok_shape(image: Image):
    N = 4
    image2, transform = apply_random_augmentations(image, n=N)

    assert isinstance(image2, PIL.Image.Image)
    assert image2.size == image.size

    assert isinstance(transform, A.Compose)
    assert len(transform.get_dict_with_id()["transforms"]) <= N


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
