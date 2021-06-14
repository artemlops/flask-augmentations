from PIL import Image
import io
import numpy as np
from mymodel.image_augmentations import get_transform
import pytest


@pytest.fixture()
def image() -> Image:
    img = np.ones((100, 100, 3), dtype=np.uint8) * 128
    img = Image.fromarray()

def test_get_transform():
    t = get_transform()
    img = Image.fromarray()
    img = np.ones((100, 100, 3), dtype=np.uint8) * 128
    
    img = F.brightness_contrast_adjust(img, alpha=1.5)
    expected_brightness = 192
    expected = np.ones((100, 100, 3), dtype=np.uint8) * expected_multiplier
    assert np.array_equal(img, expected)