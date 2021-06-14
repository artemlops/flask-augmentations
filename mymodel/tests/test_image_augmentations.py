import albumentations as A
from typing import Dict
from PIL import Image
import io
import numpy as np
from mymodel.image_augmentations import (
    create_transform,
    get_composite_transform,
    TransformRequest,
    DEFAULT_TRANSFORMS,
)
import pytest
from collections import namedtuple


_Transform = namedtuple("Transform", "name, typ, p, kwargs")

# @pytest.fixture()
# def image() -> Image:
#     img = np.ones((100, 100, 3), dtype=np.uint8) * 128
#     img = Image.fromarray()
# assert
#     img = Image.fromarray()
#     img = np.ones((100, 100, 3), dtype=np.uint8) * 128

#     img = F.brightness_contrast_adjust(img, alpha=1.5)
#     expected_brightness = 192
#     expected = np.ones((100, 100, 3), dtype=np.uint8) * expected_multiplier
#     assert np.array_equal(img, expected)


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
        _Transform(
            name="RGBShift",
            typ=A.RGBShift,
            p=1.0,
            kwargs={
                "r_shift_limit": (-40, 40),
                "g_shift_limit": (-40, 40),
            },
        ),
        _Transform(
            name="HueSaturationValue",
            typ=A.HueSaturationValue,
            p=1.0,
            kwargs={
                "hue_shift_limit": (-40, 40),
                "sat_shift_limit": (-40, 40),
            },
        ),
        _Transform(
            name="GaussNoise",
            typ=A.GaussNoise,
            p=1.0,
            kwargs={},
        ),
        _Transform(
            name="InvertImg",
            typ=A.InvertImg,
            p=1.0,
            kwargs={},
        ),
        _Transform(name="CoarseDropout", typ=A.CoarseDropout, p=1.0, kwargs={}),
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


def test_get_composite_transform__ok():
    requests = [TransformRequest("Rotate", 0.7), TransformRequest("GaussNoise", 0.5)]
    t = get_composite_transform(requests)
    assert isinstance(t, A.Compose)
    children = t.get_dict_with_id()["transforms"]
    assert len(children) == len(requests), str(children)


def test_get_composite_transform__ok_defaults():
    t = get_composite_transform()
    assert isinstance(t, A.Compose)
    children = t.get_dict_with_id()["transforms"]
    assert len(children) == len(DEFAULT_TRANSFORMS), str(children)
