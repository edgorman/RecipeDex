from dotenv import load_dotenv
import os


CONFIG_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Only for local development
env_path = os.path.abspath(
    os.path.join(CONFIG_DIRECTORY, "..", "..", ".env")
)
load_dotenv(env_path)
