"""Media file downloader for Telegram messages"""

import os
from pathlib import Path
from datetime import datetime
from telethon.tl.types import (
    MessageMediaPhoto,
    MessageMediaDocument,
    DocumentAttributeVideo,
    DocumentAttributeAudio,
    DocumentAttributeSticker,
    DocumentAttributeAnimated,
    DocumentAttributeFilename
)
from loguru import logger


class MediaDownloader:
    """Handles downloading media files from Telegram messages"""
    
    def __init__(self, base_path: str = "downloads"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
    
    def _sanitize_filename(self, text: str) -> str:
        """Remove invalid characters from filename"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            text = text.replace(char, '_')
        return text[:200]  # Limit filename length
    
    def _get_file_extension(self, message) -> str:
        """Determine file extension based on media type"""
        media = message.media
        
        if isinstance(media, MessageMediaPhoto):
            return '.jpg'
        
        if isinstance(media, MessageMediaDocument):
            document = media.document
            
            # Check document attributes
            for attr in document.attributes:
                if isinstance(attr, DocumentAttributeFilename):
                    # Extract extension from original filename
                    ext = Path(attr.file_name).suffix
                    if ext:
                        return ext
                
                if isinstance(attr, DocumentAttributeVideo):
                    if attr.round_message:
                        return '.mp4'  # Video note (кружок)
                    return '.mp4'
                
                if isinstance(attr, DocumentAttributeAudio):
                    if attr.voice:
                        return '.ogg'  # Voice message
                    return '.mp3'
                
                if isinstance(attr, DocumentAttributeSticker):
                    return '.webp'
                
                if isinstance(attr, DocumentAttributeAnimated):
                    return '.gif'
            
            # Fallback to MIME type
            mime = document.mime_type
            if mime:
                if 'video' in mime:
                    return '.mp4'
                elif 'audio' in mime:
                    return '.mp3'
                elif 'image' in mime:
                    if 'gif' in mime:
                        return '.gif'
                    return '.jpg'
            
            return '.bin'  # Unknown type
        
        return '.unknown'
    
    def _get_media_type(self, message) -> str:
        """Determine media type name for filename"""
        media = message.media
        
        if isinstance(media, MessageMediaPhoto):
            return 'photo'
        
        if isinstance(media, MessageMediaDocument):
            document = media.document
            
            for attr in document.attributes:
                if isinstance(attr, DocumentAttributeVideo):
                    if attr.round_message:
                        return 'video_note'
                    return 'video'
                
                if isinstance(attr, DocumentAttributeAudio):
                    if attr.voice:
                        return 'voice'
                    return 'audio'
                
                if isinstance(attr, DocumentAttributeSticker):
                    return 'sticker'
                
                if isinstance(attr, DocumentAttributeAnimated):
                    return 'gif'
            
            return 'document'
        
        return 'unknown'
    
    async def download_media(self, message, source_name: str) -> bool:
        """
        Download media from message to disk
        
        Args:
            message: Telegram message object
            source_name: Name of source channel/chat
            
        Returns:
            bool: True if downloaded successfully, False otherwise
        """
        if not message.media:
            return False
        
        try:
            # Create source-specific directory
            source_dir = os.path.join(self.base_path, self._sanitize_filename(source_name))
            os.makedirs(source_dir, exist_ok=True)
            
            # Generate filename
            media_type = self._get_media_type(message)
            extension = self._get_file_extension(message)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            filename = f"{media_type}_{message.id}_{timestamp}{extension}"
            filepath = os.path.join(source_dir, filename)
            
            # Download the media
            logger.info(f"Downloading {media_type} from message {message.id}...")
            await message.download_media(file=filepath)
            
            logger.success(f"✓ Downloaded: {filename}")
            
            # Save caption if exists
            if message.text or message.message:
                caption = message.text or message.message
                caption_file = filepath.replace(extension, '_caption.txt')
                with open(caption_file, 'w', encoding='utf-8') as f:
                    f.write(caption)
                logger.debug(f"  Saved caption to {os.path.basename(caption_file)}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to download media from message {message.id}: {e}")
            return False
