"""Configuration file handler"""

import yaml
from pathlib import Path
from loguru import logger


class ConfigController:
    """Handles loading and parsing of config.yaml"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {self.config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing config file: {e}")
            raise
    
    @property
    def account_phone(self) -> str:
        """Get account phone number"""
        return self.config.get('account_phone', '')
    
    @property
    def api_id(self) -> int:
        """Get Telegram API ID"""
        return self.config.get('api_id', 0)
    
    @property
    def api_hash(self) -> str:
        """Get Telegram API hash"""
        return self.config.get('api_hash', '')
    
    @property
    def delay(self) -> int:
        """Get delay between checks in seconds"""
        return self.config.get('delay', 5)
    
    @property
    def edit_message_checker_limit(self) -> int:
        """Get limit for edit tracking"""
        return self.config.get('edit_message_checker_limit', 10000)
    
    @property
    def max_initial_messages(self) -> int:
        """Get max messages to download on first run"""
        return self.config.get('max_initial_messages', 0)
    
    @property
    def download_path(self) -> str:
        """Get download path for media files"""
        return self.config.get('download_path', 'downloads')
    
    @property
    def groups(self) -> list:
        """Get list of groups configuration"""
        return self.config.get('groups', [])
