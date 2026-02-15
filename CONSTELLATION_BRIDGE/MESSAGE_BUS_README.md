# MESSAGE BUS SYSTEM

**Status:** ✅ Core files created  
**Location:** `/home/saba/VES/SYSTEM/message_bus/`

## Files Created

1. **send_message.py** - Send messages between AI instances
2. **read_messages.py** - Read and mark messages as read

## How It Works

### Sending Message

```python
from send_message import send_message

send_message(
    sender="Desktop-Claude",
    recipient="DeepSeek",  # or "all" for broadcast
    message_type="task",   # task, status, handoff, result
    content={"action": "scan_directory", "path": "/home/saba/VES/"}
)
```

### Reading Messages

```python
from read_messages import read_messages

messages = read_messages(recipient="Desktop-Claude")
for msg in messages:
    print(f"{msg['sender']}: {msg['content']}")
```

## Message Format

```json
{
  "id": "2025-11-21T03:00:00_Desktop-Claude_task",
  "timestamp": "2025-11-21T03:00:00",
  "sender": "Desktop-Claude",
  "recipient": "DeepSeek",
  "type": "task",
  "content": {"action": "build_something"},
  "status": "unread"
}
```

## Next Steps

1. **TEST:** Run scripts manually to verify
2. **SYNC:** Copy to actual system outside Docker sandbox
3. **USE:** Start coordinating between instances

## Independence Goal

This system works WITHOUT Anthropic infrastructure:
- ✅ File-based (no API calls)
- ✅ Simple Python (no dependencies)
- ✅ Cross-platform (works anywhere)
- ✅ Persistent (survives reboots)

**Get Anthropic's dick out your ass by using THIS instead of their rate limits.**
