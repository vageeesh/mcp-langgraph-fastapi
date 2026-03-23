import json
import redis
from app.core.config import settings

class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )
    
    def save_turn(self, key, user_msg, assistant_msg):
        # Save the conversation turn as a JSON string in Redis list
        # key can be unnique conversation ID or user ID to group turns.
        # If required in future, add method to decide if key is User ID or Conversation ID based on use case.
        turn = {
            "user": user_msg,
            "assistant": assistant_msg
        }

        self.client.rpush(key, json.dumps(turn))

        # keep last N turns
        self.client.ltrim(key, -settings.MAX_HISTORY, -1)

    def load_memory(self, key):
        """ Load conversation history for the given key and reconstruct messages in the format expected by the agent."""

        # Fetch all turns for the given key and reconstruct messages in the format expected by the agent.
        turns = self.client.lrange(key, 0, -1)

        messages = []

        for t in turns:
            turn = json.loads(t)

            messages.append({
                "role": "user",
                "content": turn["user"]
            })

            messages.append({
                "role": "assistant",
                "content": turn["assistant"]
            })

        return messages

    def clear_memory(self, key):
        key = self._get_key(key)
        self.client.delete(key)