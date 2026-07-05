"""Message filtering and preparation"""

from loguru import logger


class MessagePreparer:
    """Filters messages based on whitelist criteria"""
    
    def __init__(self, whitelist: list = None):
        self.whitelist = whitelist or []
    
    def should_process(self, message) -> bool:
        """
        Check if message should be processed based on whitelist
        
        Args:
            message: Telegram message object
            
        Returns:
            bool: True if message should be processed
        """
        # If no whitelist, process all messages with media
        if not self.whitelist:
            return message.media is not None
        
        # Check if message has media
        if not message.media:
            return False
        
        # Get message text
        text = message.text or message.message or ""
        text_lower = text.lower()
        
        # Check if any whitelist word is in the message
        for word in self.whitelist:
            if word.lower() in text_lower:
                logger.debug(f"Message {message.id} matches whitelist word: '{word}'")
                return True
        
        logger.debug(f"Message {message.id} does not match whitelist")
        return False
