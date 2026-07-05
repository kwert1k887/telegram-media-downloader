"""
Helper script to list all your Telegram chats and channels
Use this to find the exact names to put in config.yaml
"""

import asyncio
from telethon import TelegramClient
from telethon.tl.types import Channel, Chat, User
import yaml

async def main():
    # Load config
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    api_id = config['api_id']
    api_hash = config['api_hash']
    phone = config['account_phone']
    session_name = f"sessions/{phone.replace('+', '')}"
    
    # Create client
    client = TelegramClient(session_name, api_id, api_hash)
    
    print("\n" + "="*70)
    print("LISTING ALL YOUR TELEGRAM CHATS AND CHANNELS")
    print("="*70 + "\n")
    
    await client.start(phone=phone)
    
    # Get all dialogs
    dialogs = await client.get_dialogs()
    
    channels = []
    groups = []
    users = []
    
    for dialog in dialogs:
        entity = dialog.entity
        name = dialog.name
        entity_id = entity.id
        
        if isinstance(entity, Channel):
            if entity.broadcast:
                channels.append((name, entity_id))
            else:
                groups.append((name, entity_id))
        elif isinstance(entity, Chat):
            groups.append((name, entity_id))
        elif isinstance(entity, User):
            users.append((name, entity_id))
    
    # Print results
    if channels:
        print("📢 CHANNELS (use these names in config.yaml):")
        print("-" * 70)
        for name, entity_id in sorted(channels):
            print(f"  • {name}")
            print(f"    ID: {entity_id}\n")
    
    if groups:
        print("\n👥 GROUPS (use these names in config.yaml):")
        print("-" * 70)
        for name, entity_id in sorted(groups):
            print(f"  • {name}")
            print(f"    ID: {entity_id}\n")
    
    if users:
        print("\n💬 PRIVATE CHATS (use these names in config.yaml):")
        print("-" * 70)
        for name, entity_id in sorted(users)[:20]:  # Show first 20
            print(f"  • {name}")
            print(f"    ID: {entity_id}\n")
        
        if len(users) > 20:
            print(f"  ... and {len(users) - 20} more private chats\n")
    
    print("="*70)
    print("\n💡 HOW TO USE:")
    print("   1. Copy the EXACT name from above")
    print("   2. Paste it into config.yaml under 'sources:'")
    print("   3. Example:")
    print("      sources:")
    print('        - "My Channel Name"  # Must match exactly!')
    print("\n" + "="*70 + "\n")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())