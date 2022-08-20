from typing import Any, Dict

import discord
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_actionrow, create_button

from job_api_wrapers import JobInfo
from utils import Colors


def invalid_url_message() -> Dict[str, Any]:
    return {
        "content": (
            "Hi there! Seems like your URL or job ID is invalid. "
            "Make sure that the URL is linking to a job post. "
            "And keep in mind that currently Janus only supports LinkedIn job posts."
        ),
        "hidden": True,
    }


def job_info_message(data: JobInfo) -> Dict[str, Any]:
    colors = Colors()
    random_color = colors.random_color()
    final_color = discord.Colour(random_color)

    epoch = round(data.posted_time.timestamp())

    description = (
        f"**{data.company}**\n*{data.title}*\n\n"
        f"Location: {data.location}.\n\n"
        f"This job was posted __<t:{epoch}:R>__.\n\n"
    )

    embed_content = discord.Embed(
        title="Check out this job on LinkedIn!",
        type="rich",
        description=description,
        color=final_color,
    )
    embed_content.set_thumbnail(url=f"{data.company_pic_url}")

    apply_button = create_button(style=ButtonStyle.URL, label="Apply Now", url=data.url)
    action_row = create_actionrow(apply_button)

    return {"content": data.summary, "embed": embed_content, "components": [action_row]}
