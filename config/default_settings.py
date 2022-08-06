import os

from config.local_settings import DISCORD_TOKEN


class OSEnvKeys:
    """
    Containing the names of the OS environment keys
    """

    DISCORD_TOKEN = "DISCORD_TOKEN"
    TRIDENT_IMG_URL = "TRIDENT_IMG_URL"
    LINKEDIN_IMG_URL = "LINKEDIN_IMG_URL"
    GLASSDOOR_IMG_URL = "GLASSDOOR_IMG_URL"

    @classmethod
    def to_list(cls):
        """Return a list of the OS environment keys"""
        condition = lambda x: not callable(getattr(cls, x)) and not x.startswith("__")
        return [getattr(cls, attr) for attr in dir(cls) if condition(attr)]


# Discord credentials
DISCORD_TOKEN = os.environ.get(OSEnvKeys.DISCORD_TOKEN)

# Images URLs
TRIDENT_IMG_URL = os.environ.get(OSEnvKeys.TRIDENT_IMG_URL)
LINKEDIN_IMG_URL = os.environ.get(OSEnvKeys.LINKEDIN_IMG_URL)
GLASSDOOR_IMG_URL = os.environ.get(OSEnvKeys.GLASSDOOR_IMG_URL)
