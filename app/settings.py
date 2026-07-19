import json
import os

SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "rate_limit": {
        "requests": 20,
        "window": 60
    },
    "retention_days": 30
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    
    with open(SETTINGS_FILE, "r") as f:
        try:
            settings = json.load(f)
            # Merge defaults for any missing keys
            for key, val in DEFAULT_SETTINGS.items():
                if key not in settings:
                    settings[key] = val
            return settings
        except Exception:
            return DEFAULT_SETTINGS

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)
