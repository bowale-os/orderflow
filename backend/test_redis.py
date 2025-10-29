import redis
import os
from dotenv import load_dotenv

load_dotenv()
r = redis.Redis.from_url(os.getenv("REDIS_URL"))
r.set("test_key", "hello")
print(r.get("test_key"))  # Should print: b'hello'
