from dotenv import load_dotenv
import os


CONFIG_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Only for local development
env_path = os.path.abspath(
    os.path.join(CONFIG_DIRECTORY, "..", "..", ".env")
)
load_dotenv(env_path)


def str_to_bool(value: str) -> bool:
    return value.strip().lower() == "true"
