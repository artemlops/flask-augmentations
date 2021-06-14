# Model package

This package is supposed to contain the ML model code, which includes image augmentations.

- The package is organized as a proper Python package installable via `pip` (so that no hacks like `sys.append` or `export PYTHONPATH` are needed).
- Augmentations defined in [image_augmentations.py](image_augmentations.py) in a *testible* and *extensible* way:
  - to support a new augmentation from `albumentations`, just add it to `TRANSFORMS` and method `create_transform` will automatically plug it in,
  - method `get_random_transform_classes` uses albumentations names, which allows us to unit-test it separately,
  - method `apply_augmentation` uses inputs/outputs of the level of `PIL.Image` and `albumentations`, which makes it understandable for regular data scientists,
  - 
