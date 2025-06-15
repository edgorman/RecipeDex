import os
from internal.config import CONFIG_DIRECTORY


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
FIREBASE_CONFIG_FILEPATH = os.path.join(CONFIG_DIRECTORY, "firebase.json")
