from PIL import Image
import numpy as np
import albumentations as A


# Note: albumentations have made a similar API but via Streamlit
# not via Flask: https://albumentations-demo.herokuapp.com/

def get_transform() -> A.Compose:
    # TODO: expose some parameters
    return A.Compose([
        A.HorizontalFlip(p=0.2),
        A.VerticalFlip(p=0.2),
        #A.RandomBrightnessContrast(p=0.1),
        A.RGBShift(p=0.5, r_shift_limit=(-20, 20), g_shift_limit=(-20, 20), b_shift_limit=(-20, 20)),
        A.HueSaturationValue(p=0.5, hue_shift_limit=(-20, 20), sat_shift_limit=(-30, 30), val_shift_limit=(-20, 20)),
        A.RandomBrightnessContrast(p=1.0, brightness_limit=1, contrast_limit=1),
    ])


def random_augmentation(image: Image) -> Image:
    transform = get_transform()
    # TODO: print out the chosen random transformation to index.html
    image_np = np.array(image)
    augmented = transform(image=image_np)
    image = Image.fromarray(augmented['image'])
    image = image.convert('RGB')
    return image

# def do_nothing(image: Image):
#     return image

# def fliplr(image: Image):
#     return A.transpose(p=1)

# def rotate(image: Image):
#     return A.Rotate(p=1)


