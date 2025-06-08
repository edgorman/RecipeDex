from dotenv import load_dotenv
import os


env_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", ".env")
)
loaded = load_dotenv(env_path)
if not loaded:
    raise RuntimeError("Could not find .env file")
