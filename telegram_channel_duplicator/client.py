"""Telegram client wrapper"""

from telethon import TelegramClient
from loguru import logger
import os


class Client:
    """Telegram client wrapper for authentication and connection"""
    
    def __init__(self, api_id: int, api_hash: str, phone: str):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.session_name = f"sessions/{phone.replace('+', '')}"
        
        # Create sessions directory if it doesn't exist
        os.makedirs("sessions", exist_ok=True)
        
        self.client = TelegramClient(
            self.session_name,
            self.api_id,
            self.api_hash
        )
    
    async def start(self):
        """Start the Telegram client and authenticate"""
        logger.info("Starting Telegram client...")
        
        await self.client.start(phone=self.phone)
        
        if await self.client.is_user_authorized():
            me = await self.client.get_me()
            logger.info(f"Authenticated as: {me.first_name} (@{me.username})")
        else:
            logger.error("Authentication failed!")
            raise Exception("Failed to authenticate with Telegram")
        
        return self.client
    
    async def disconnect(self):
        """Disconnect from Telegram"""
        await self.client.disconnect()
        logger.info("Disconnected from Telegram")
