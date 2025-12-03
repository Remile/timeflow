"""Clipboard handling utilities."""
import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime

import pyperclip
from PIL import ImageGrab, Image


class ClipboardHandler:
    """Handle clipboard operations for text and images."""
    
    def __init__(self, image_storage_path: str):
        """Initialize clipboard handler.
        
        Args:
            image_storage_path: Directory to store clipboard images
        """
        self.image_storage_path = Path(image_storage_path)
        self.image_storage_path.mkdir(parents=True, exist_ok=True)
    
    def get_text(self) -> Optional[str]:
        """Get text from clipboard.
        
        Returns:
            Text content from clipboard, or None if no text is available
        """
        try:
            text = pyperclip.paste()
            if text and text.strip():
                return text.strip()
        except Exception as e:
            print(f"Warning: Failed to get text from clipboard: {e}")
        return None
    
    def get_image(self) -> Optional[str]:
        """Get image from clipboard and save it to storage.
        
        Returns:
            Path to saved image file, or None if no image is available
        """
        try:
            # Try to get image from clipboard
            image = ImageGrab.grabclipboard()
            
            if image is not None:
                # If it's a PIL Image
                if isinstance(image, Image.Image):
                    return self._save_image(image)
                
                # If it's a list of file paths (e.g., copied files)
                elif isinstance(image, list) and len(image) > 0:
                    # Try to open the first file as an image
                    try:
                        img = Image.open(image[0])
                        return self._save_image(img)
                    except Exception:
                        pass
        
        except Exception as e:
            print(f"Warning: Failed to get image from clipboard: {e}")
        
        return None
    
    def _save_image(self, image: Image.Image) -> str:
        """Save an image to storage.
        
        Args:
            image: PIL Image object
            
        Returns:
            Path to saved image file
        """
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"clipboard_{timestamp}.png"
        filepath = self.image_storage_path / filename
        
        # Save image
        image.save(filepath, "PNG")
        
        return str(filepath)
    
    def get_content(self) -> Tuple[Optional[str], Optional[str]]:
        """Get both text and image from clipboard.
        
        Returns:
            Tuple of (text, image_path)
        """
        text = self.get_text()
        image_path = self.get_image()
        return text, image_path
    
    def has_content(self) -> bool:
        """Check if clipboard has any content.
        
        Returns:
            True if clipboard has text or image content
        """
        text = self.get_text()
        
        # Check for image without actually saving it
        try:
            image = ImageGrab.grabclipboard()
            has_image = image is not None
        except Exception:
            has_image = False
        
        return bool(text) or has_image


