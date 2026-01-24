"""
Image Processing Utilities
"""
import os
from pathlib import Path
from datetime import datetime
from PIL import Image
from typing import Tuple

from app.core.constants import MAX_IMAGE_DIMENSION, IMAGE_QUALITY, PROFILE_IMAGE_DIRECTORY
from app.core.config import settings


def ensure_image_directory():
    """Ensure the profile image directory exists"""
    Path(PROFILE_IMAGE_DIRECTORY).mkdir(parents=True, exist_ok=True)


def generate_unique_filename(original_filename: str, user_id: int) -> str:
    """
    Generate a unique filename for uploaded image
    
    Args:
        original_filename: Original file name
        user_id: User ID
    
    Returns:
        Unique filename with .webp extension
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    return f"user_{user_id}_{timestamp}.webp"


def validate_image_type(filename: str) -> bool:
    """
    Validate if file is an allowed image type
    
    Args:
        filename: File name to validate
    
    Returns:
        True if valid, False otherwise
    """
    extension = filename.rsplit(".", 1)[-1].lower()
    return extension in settings.allowed_image_types_list


def resize_and_convert_image(
    image_path: str,
    output_path: str,
    max_dimension: int = MAX_IMAGE_DIMENSION,
    quality: int = IMAGE_QUALITY
) -> Tuple[int, int]:
    """
    Resize and convert image to WebP format
    
    Args:
        image_path: Path to source image
        output_path: Path to save converted image
        max_dimension: Maximum width or height
        quality: WebP quality (1-100)
    
    Returns:
        Tuple of (width, height) of the output image
    """
    with Image.open(image_path) as img:
        # Convert RGBA to RGB if necessary
        if img.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
            img = background
        
        # Calculate new dimensions maintaining aspect ratio
        width, height = img.size
        if width > max_dimension or height > max_dimension:
            if width > height:
                new_width = max_dimension
                new_height = int((max_dimension / width) * height)
            else:
                new_height = max_dimension
                new_width = int((max_dimension / height) * width)
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save as WebP
        img.save(output_path, "WEBP", quality=quality, optimize=True)
        
        return img.size


def delete_old_profile_image(image_path: str):
    """
    Delete old profile image if it exists
    
    Args:
        image_path: Path to image file
    """
    if image_path and os.path.exists(image_path):
        try:
            os.remove(image_path)
        except Exception:
            pass  # Silently fail if unable to delete