import logging
from http.client import InvalidURL

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_actionrow
from discord_slash.utils.manage_components import create_button

from job_boards_scrapers import LinkedIn
from utils import Colors


_LOGGER = logging.getLogger(__name__)


class Descriptions:
    POST_JOB = "Parse a job post's information beautifully in the channel"
    HELP = "Display the list of commands and their usages"


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.linkedin_job_api = LinkedIn()

    @cog_ext.cog_slash(name="post-job", description=Descriptions.POST_JOB)
    async def _post_job(self, ctx: SlashContext, url_or_jobid: str):
        job = int(url_or_jobid) if url_or_jobid.isnumeric() else url_or_jobid

        try:
            data = self.linkedin_job_api.get_job_info(job)
        except InvalidURL:
            await ctx.send(
                (
                    "Hi there! Seems like your URL is invalid. "
                    "Make sure that the URL is linking to a job post. "
                    "And keep in mind that currently Janus only supports LinkedIn job posts."
                ),
                hidden=True,
            )
            _LOGGER.info("Sent private message to user notifying given url is invalid.")
            return

        colors = Colors()
        random_color = colors.random_color()
        final_color = discord.Colour(random_color)

        description = (
            f"**{data.company}**\n*{data.title}*\n\n"
            f"Location: {data.location}.\n\n"
            f"This job was posted __{data.posted_time_ago}__.\n\n"
        )

        embed_content = discord.Embed(
            title="Check out this job on LinkedIn!",
            type="rich",
            description=description,
            color=final_color,
        )
        embed_content.set_thumbnail(url=f"{data.company_pic_url}")

        apply_button = create_button(
            style=ButtonStyle.URL, label="Apply Now", url=data.url
        )
        action_row = create_actionrow(apply_button)

        await ctx.send(embed=embed_content, components=[action_row])

    @cog_ext.cog_slash(name="help", description=Descriptions.HELP)
    async def _help(self, ctx: SlashContext):
        help_msg = f"""
        `post-job` - {Descriptions.POST_JOB}
        `help` - {Descriptions.HELP}
        """
        embed_content = discord.Embed(
            title="Here's what you can do with this bot!",
            type="rich",
            description=help_msg,
        )
        await ctx.send(embed=embed_content)


def setup(bot):
    bot.add_cog(Slash(bot))
