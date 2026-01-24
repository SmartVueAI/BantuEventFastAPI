"""
Image Processing Service
"""
import os
from fastapi import UploadFile
from loguru import logger

from app.utils.image_utils import (
    ensure_image_directory,
    generate_unique_filename,
    validate_image_type,
    resize_and_convert_image,
    delete_old_profile_image,
)
from app.exceptions import InvalidFileTypeException, FileTooLargeException
from app.core.config import settings


class ImageService:
    """Image processing service"""
    
    def __init__(self):
        ensure_image_directory()
    
    async def process_profile_image(
        self,
        file: UploadFile,
        user_id: int,
        old_filename: str | None = None
    ) -> str:
        """
        Process and save profile image
        
        Returns:
            URL path to saved image
        """
        try:
            # Validate file type
            filename = file.filename or "unknown"
            if not validate_image_type(filename):
                raise InvalidFileTypeException(
                    f"Invalid file type. Allowed types: {', '.join(settings.allowed_image_types_list)}"
                )
            
            # Check file size
            file.file.seek(0, 2)
            file_size = file.file.tell()
            file.file.seek(0)
            
            max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
            if file_size > max_size:
                raise FileTooLargeException(
                    f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB"
                )
            
            # Generate filename
            new_filename = generate_unique_filename(filename, user_id)
            temp_path = f"/tmp/{new_filename}_temp"
            final_path = f"static/profile_images/{new_filename}"
            
            # Save temporary file
            with open(temp_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            # Resize and convert to WebP
            resize_and_convert_image(temp_path, final_path)
            
            # Delete temporary file
            os.remove(temp_path)
            
            # Delete old image if exists
            if old_filename:
                old_path = f"static/profile_images/{old_filename}"
                delete_old_profile_image(old_path)
            
            # Return URL
            image_url = f"/static/profile_images/{new_filename}"
            logger.info(f"Profile image processed: {image_url}")
            
            return image_url
            
        except Exception as e:
            logger.error(f"Image processing error: {str(e)}")
            raise