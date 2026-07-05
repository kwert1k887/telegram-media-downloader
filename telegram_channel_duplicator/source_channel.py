"""Source channel/chat handler"""

from telethon import TelegramClient
from telethon.tl.types import Channel, Chat, User
from loguru import logger


class SourceChannel:
    """Represents a source channel, group, or private chat"""
    
    def __init__(self, client: TelegramClient, name: str):
        self.client = client
        self.name = name
        self.entity = None
        self.entity_id = None
    
    async def initialize(self):
        """Initialize and fetch the entity from Telegram"""
        try:
            self.entity = await self.client.get_entity(self.name)
            self.entity_id = self.entity.id
            
            # Determine entity type
            if isinstance(self.entity, Channel):
                entity_type = "Channel"
            elif isinstance(self.entity, Chat):
                entity_type = "Group"
            elif isinstance(self.entity, User):
                entity_type = "Private Chat"
            else:
                entity_type = "Unknown"
            
            logger.info(f"Source '{self.name}' found: {entity_type} (ID: {self.entity_id})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to find source '{self.name}': {e}")
            return False
    
    async def get_messages(self, limit: int = None, min_id: int = 0):
        """
        Get messages from the source
        
        Args:
            limit: Maximum number of messages to fetch (None = all)
            min_id: Only get messages with ID greater than this
            
        Returns:
            List of messages
        """
        if not self.entity:
            logger.error(f"Source '{self.name}' not initialized")
            return []
        
        try:
            messages = []
            async for message in self.client.iter_messages(
                self.entity,
                limit=limit,
                min_id=min_id,
                reverse=False
            ):
                messages.append(message)
            
            return messages
            
        except Exception as e:
            logger.error(f"Failed to fetch messages from '{self.name}': {e}")
            return []
