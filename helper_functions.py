from PIL import Image, ImageCms
import io
from pathlib import Path
from constants import *


def save_file(img: Image, canvas_path: Path):
    img = set_image_gamma(img, DECODING_GAMMA)
    save_image_path = canvas_path.with_name(
        canvas_path.name.split(".")[0] + f"OUTPUT.{FILE_FORMAT}")
    check_if_path_exists(save_image_path)
    img.save(save_image_path, FILE_FORMAT)


def set_image_gamma(img: Image, gamma):
    # this is the Callable[[int], float] being passed to img.point
    lookup_table = lambda x: ((x / 255) ** gamma) * 255
    return img.point(lookup_table)


def get_icc_profile(image):
    icc = image.info.get('icc_profile')
    if icc is None:
        print("No ICC profile found in image.")
        return
    f = io.BytesIO(icc)
    prf = ImageCms.ImageCmsProfile(f)
    print(f"Custom ICC profile detected {prf.profile.profile_description}")
    return prf


def is_srgb_image(image):
    if "srgb" in image.info:
        return True
    prf = get_icc_profile(image)
    if prf is None:
        return False
    elif "srgb" in prf.profile.profile_description.lower():
        return True
    return False


def check_if_path_exists(savepath: Path):
    if savepath.exists():
        savepath.unlink()
