from PIL import Image
from typing import List
import numpy as np
import albumentations as A
import logging


# Note: albumentations have made a similar API but via Streamlit
# not via Flask: https://albumentations-demo.herokuapp.com/


def create_transform(name: str, p: float, **kwargs):
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


# def get_transforms(probs: List[float]) -> List[A.BasicTransform]:
#     # TODO: expose more parameters
#     err = "Invalid argument 'probs'"
#     if not probs:
#         raise ValueError(f"{err}: expect at least one item")
#     max_len = len(GET_TRANSFORM)

#     if len(probs) >= max_len:
#         raise ValueError(f"{err}: expect at most {max_len} items")
#     if not all(0.0 <= p <= 1.0 for p in probs):
#         raise ValueError(f"{err}: all items must be valid probabilities")

#     diff_len = max_len - len(probs)
#     all_probs = probs
#     if diff_len > 0:
#         all_probs += [0.0] * diff_len

#     transforms = [
#         GET_TRANSFORM[i](p)
#         for i, p in enumerate(all_probs)
#     ]
#     return transforms

#     # return A.Compose(transforms, p=1.0, always_apply=True)

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
