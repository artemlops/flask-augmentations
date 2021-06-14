import logging
import random
from typing import Any, Dict, List, Tuple

import albumentations as A
import numpy as np
import PIL.Image


# Fun fact: albumentations have made a similar API but via Streamlit
# not via Flask: https://albumentations-demo.herokuapp.com/


TRANSFORMS: Dict[A.BasicTransform, Dict] = {
    A.Rotate: {},
    A.ShiftScaleRotate: {
        "shift_limit": (-0.06, 0.06),
        "scale_limit": (-0.1, 0.1),
        "rotate_limit": (-90, 90),
        "interpolation": 0,
    },
    A.HorizontalFlip: {},
    A.VerticalFlip: {},
    A.RandomBrightnessContrast: {},
    A.RGBShift: {
        "r_shift_limit": (-20, 20),
        "g_shift_limit": (-20, 20),
        "b_shift_limit": (-20, 20),
    },
    A.HueSaturationValue: {
        "hue_shift_limit": (-20, 20),
        "sat_shift_limit": (-30, 30),
        "val_shift_limit": (-20, 20),
    },
    A.GaussNoise: {
        "var_limit": (50, 150),
    },
    A.InvertImg: {},
    A.CoarseDropout: {"max_holes": 15},
}


DEFAULT_N_TRANSFORMS = len(TRANSFORMS)


def _get_transform_name(t: A.BasicTransform) -> str:
    return t.get_class_fullname().split(".")[-1]


def create_transform(name: str, p: float, **kwargs: Any):
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"Invalid argument p={p}: must be a valid prob")

    for transform, kw in TRANSFORMS.items():
        t_name = _get_transform_name(transform)
        if t_name == name:
            all_kwargs: Dict = {**kw, **kwargs}
            return transform(p=p, **all_kwargs)

    raise ValueError(f"Invalid transform name: '{name}'")


def get_random_transform_classes(*, n: int = DEFAULT_N_TRANSFORMS) -> List[str]:
    logging.info(f"Generating {n} random transform classes")
    transform_names = list(TRANSFORMS)
    random.shuffle(transform_names)
    transforms = transform_names[:n]
    logging.info(f"Randomly chosen {n} transforms: {transforms}")
    return [_get_transform_name(t) for t in transforms]


def apply_augmentation(
    image: PIL.Image.Image, transform: A.BasicTransform
) -> PIL.Image.Image:
    # TODO: print out the chosen random transformation to index.html
    image_np = np.array(image)
    augmented = transform(image=image_np)
    image = PIL.Image.fromarray(augmented["image"])
    image = image.convert("RGB")
    return image


def apply_random_augmentations(
    image: PIL.Image.Image, *, n: int = DEFAULT_N_TRANSFORMS, p: float = 0.75
) -> Tuple[PIL.Image.Image, List[Dict]]:
    transform = A.Compose(
        [create_transform(n, p) for n in get_random_transform_classes(n=n)]
    )
    result = apply_augmentation(image, transform)
    info = get_composite_transform_info(transform)
    return result, info


def get_composite_transform_info(transform: A.Compose) -> List[Dict]:
    children = transform.get_dict_with_id()["transforms"]
    result = []
    for c in children:
        c.pop("id")
        result.append(
            {
                "name": c.pop("__class_fullname__"),
                **c,
            }
        )
    return result
