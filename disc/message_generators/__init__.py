from typing import Any, Dict

import discord


class Descriptions:
    POST_JOB = "Parse a job post's information beautifully in the channel"
    HELP = "Display the list of commands and their usages"


def help_message() -> Dict[str, Any]:
    help_msg = f"""
        `post-job` - {Descriptions.POST_JOB}
        `help` - {Descriptions.HELP}
        """
    embed_content = discord.Embed(
        title="Here's what you can do with this bot!",
        type="rich",
        description=help_msg,
    )
    return {"embed": embed_content, "hidden": True}


def server_error_message() -> Dict[str, Any]:
    return {
        "content": (
            "Seems like we have an internal server error." "Please try again later :("
        ),
        "hidden": True,
    }
