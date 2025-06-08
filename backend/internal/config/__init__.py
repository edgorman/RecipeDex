from dotenv import load_dotenv
import os


# Only for local development
env_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", ".env")
)
load_dotenv(env_path)
