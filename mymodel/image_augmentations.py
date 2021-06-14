from PIL import Image
from typing import List, Dict, Any, Tuple
import numpy as np
import albumentations as A
import logging


# Note: albumentations have made a similar API but via Streamlit
# not via Flask: https://albumentations-demo.herokuapp.com/

from collections import namedtuple


TransformRequest = namedtuple("TransformRequest", "name, p, kwargs", defaults=[{}])

DEFAULT_TRANSFORMS = (
    TransformRequest("ShiftScaleRotate", 0.75),
    TransformRequest("HorizontalFlip", 0.3),
    TransformRequest("VerticalFlip", 0.3),
    TransformRequest("HueSaturationValue", 0.5),
    TransformRequest("GaussNoise", 0.5),
    TransformRequest("CoarseDropout", 0.3),
)


def create_transform(name: str, p: float, **kwargs):
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"Invalid argument p={p}: must be a valid probability")
    if name == "Rotate":
        return A.Rotate(p=p, **kwargs)
    if name == "ShiftScaleRotate":
        return A.ShiftScaleRotate(
            p=p,
            shift_limit=kwargs.pop("shift_limit", (-0.06, 0.06)),
            scale_limit=kwargs.pop("scale_limit", (-0.1, 0.1)),
            rotate_limit=kwargs.pop("rotate_limit", (-90, 90)),
            interpolation=kwargs.pop("interpolation", 0),
            **kwargs,
        )
    if name == "HorizontalFlip":
        return A.HorizontalFlip(p=p, **kwargs)
    if name == "VerticalFlip":
        return A.VerticalFlip(p=p, **kwargs)
    if name == "RandomBrightnessContrast":
        return A.RandomBrightnessContrast(p=p, **kwargs)
    if name == "RGBShift":
        return A.RGBShift(
            p=p,
            r_shift_limit=kwargs.pop("r_shift_limit", (-20, 20)),
            g_shift_limit=kwargs.pop("g_shift_limit", (-20, 20)),
            b_shift_limit=kwargs.pop("b_shift_limit", (-20, 20)),
            **kwargs,
        )
    if name == "HueSaturationValue":
        return A.HueSaturationValue(
            p=p,
            hue_shift_limit=kwargs.pop("hue_shift_limit", (-20, 20)),
            sat_shift_limit=kwargs.pop("sat_shift_limit", (-30, 30)),
            val_shift_limit=kwargs.pop("val_shift_limit", (-20, 20)),
            **kwargs,
        )
    if name == "GaussNoise":
        return A.GaussNoise(
            p=p,
            var_limit=kwargs.pop("var_limit", (50, 150)),
            **kwargs,
        )
    if name == "InvertImg":
        return A.InvertImg(
            p=p,
            **kwargs,
        )
    if name == "CoarseDropout":
        return A.CoarseDropout(
            p=p,
            max_holes=kwargs.pop("max_holes", 10),
            **kwargs,
        )

    raise ValueError(f"Invalid transform name: '{name}'")


def get_composite_transform(
    requests: List[TransformRequest] = DEFAULT_TRANSFORMS,
) -> A.Compose:
    # TODO: expose more parameters
    err = "Invalid argument 'requests'"
    if not requests:
        raise ValueError(f"Invalid argument 'requests': expect at least one item")
    transforms = [create_transform(req.name, req.p, **req.kwargs) for req in requests]
    return A.Compose(transforms, p=1.0)


# def random_augmentation(image: Image) -> Image:
#     transform = get_transform()
#     # TODO: print out the chosen random transformation to index.html
#     image_np = np.array(image)
#     augmented = transform(image=image_np)
#     image = Image.fromarray(augmented['image'])
#     image = image.convert('RGB')
#     return image

# # def do_nothing(image: Image):
# #     return image

# # def fliplr(image: Image):
# #     return A.transpose(p=1)

# # def rotate(image: Image):
# #     return A.Rotate(p=1)
