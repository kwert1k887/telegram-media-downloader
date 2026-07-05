"""Main downloader class - coordinates all operations"""

import asyncio
from loguru import logger
from .config_controller import ConfigController
from .client import Client
from .source_channel import SourceChannel
from .message_preparer import MessagePreparer
from .media_downloader import MediaDownloader


class Duplicator:
    """Main class that coordinates media downloading from Telegram"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = ConfigController(config_path)
        self.client_wrapper = None
        self.client = None
        self.downloader = MediaDownloader(self.config.download_path)
        self.sources = []
        self.last_message_ids = {}  # Track last processed message per source
    
    async def _initialize_client(self):
        """Initialize and authenticate Telegram client"""
        logger.info("Initializing Telegram client...")
        
        self.client_wrapper = Client(
            api_id=self.config.api_id,
            api_hash=self.config.api_hash,
            phone=self.config.account_phone
        )
        
        self.client = await self.client_wrapper.start()
        logger.success("✓ Telegram client ready")
    
    async def _initialize_sources(self):
        """Initialize all source channels/chats"""
        logger.info("Initializing sources...")
        
        for group in self.config.groups:
            group_name = group.get('name', 'Unnamed group')
            source_names = group.get('sources', [])
            
            if not source_names:
                logger.warning(f"Group '{group_name}' has no sources")
                continue
            
            logger.info(f"Processing group: {group_name}")
            
            for source_name in source_names:
                source = SourceChannel(self.client, source_name)
                if await source.initialize():
                    self.sources.append({
                        'source': source,
                        'preparer': MessagePreparer(group.get('whitelist', [])),
                        'group_name': group_name
                    })
                    # Initialize with 0 to download all messages on first run
                    self.last_message_ids[source.entity_id] = 0
        
        if not self.sources:
            logger.error("No valid sources found!")
            return False
        
        logger.success(f"✓ Initialized {len(self.sources)} source(s)")
        return True
    
    async def _process_initial_messages(self):
        """Download messages on first run"""
        logger.info("=" * 60)
        logger.info("INITIAL DOWNLOAD")
        logger.info("=" * 60)
        
        max_messages = self.config.max_initial_messages
        
        for source_config in self.sources:
            source = source_config['source']
            preparer = source_config['preparer']
            
            logger.info(f"\nProcessing source: {source.name}")
            
            # Get messages
            limit = max_messages if max_messages > 0 else None
            messages = await source.get_messages(limit=limit)
            
            if not messages:
                logger.warning(f"No messages found in {source.name}")
                continue
            
            logger.info(f"Found {len(messages)} message(s)")
            
            # Process messages
            downloaded_count = 0
            for message in messages:
                if preparer.should_process(message):
                    if await self.downloader.download_media(message, source.name):
                        downloaded_count += 1
                
                # Update last message ID
                if message.id > self.last_message_ids.get(source.entity_id, 0):
                    self.last_message_ids[source.entity_id] = message.id
            
            logger.info(f"Downloaded {downloaded_count} media file(s) from {source.name}")
    
    async def _monitor_new_messages(self):
        """Monitor sources for new messages"""
        logger.info("=" * 60)
        logger.info("MONITORING FOR NEW MESSAGES")
        logger.info("=" * 60)
        logger.info(f"Checking every {self.config.delay} seconds...")
        logger.info("Press Ctrl+C to stop")
        
        while True:
            try:
                await asyncio.sleep(self.config.delay)
                
                for source_config in self.sources:
                    source = source_config['source']
                    preparer = source_config['preparer']
                    
                    # Get new messages since last check
                    last_id = self.last_message_ids.get(source.entity_id, 0)
                    messages = await source.get_messages(min_id=last_id)
                    
                    if not messages:
                        continue
                    
                    logger.info(f"Found {len(messages)} new message(s) in {source.name}")
                    
                    # Process new messages
                    for message in messages:
                        if preparer.should_process(message):
                            await self.downloader.download_media(message, source.name)
                        
                        # Update last message ID
                        if message.id > self.last_message_ids.get(source.entity_id, 0):
                            self.last_message_ids[source.entity_id] = message.id
            
            except asyncio.CancelledError:
                logger.info("Monitoring stopped")
                break
            except Exception as e:
                logger.error(f"Error during monitoring: {e}")
                await asyncio.sleep(self.config.delay)
    
    async def start(self):
        """Start the downloader"""
        try:
            # Initialize
            await self._initialize_client()
            
            if not await self._initialize_sources():
                logger.error("Failed to initialize sources. Exiting...")
                return
            
            # Download initial messages
            await self._process_initial_messages()
            
            # Monitor for new messages
            await self._monitor_new_messages()
            
        except KeyboardInterrupt:
            logger.info("\n\nStopping downloader...")
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            raise
        finally:
            if self.client_wrapper:
                await self.client_wrapper.disconnect()
            logger.info("Downloader stopped")
