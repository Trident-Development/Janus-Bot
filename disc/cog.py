import logging
from http.client import InvalidURL

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_actionrow
from discord_slash.utils.manage_components import create_button
from linkedin_api import Linkedin as LinkedInProfileAPI

from config import LINKEDIN_ACCOUNT
from config import LINKEDIN_PASSWORD
from job_boards_scrapers import LinkedIn as LinkedInJobAPI
from utils import Colors


_LOGGER = logging.getLogger(__name__)


class Descriptions:
    POST_JOB = "Parse a job post's information beautifully in the channel"
    HELP = "Display the list of commands and their usages"


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.linkedin_job_api = LinkedInJobAPI()
        self.linkedin_profile_api = LinkedInProfileAPI(
            LINKEDIN_ACCOUNT, LINKEDIN_PASSWORD
        )

    @cog_ext.cog_slash(name="view-profile", description=Descriptions.POST_JOB)
    async def _view_profile(self, ctx: SlashContext, profile):

        await ctx.send("Hang on, grabbing details for you...", hidden=True)

        get_profile = self.linkedin_profile_api.get_profile(profile)

        time_string = ""
        for job in get_profile["experience"]:
            time_period = job["timePeriod"]
            if "endDate" in time_period:
                time_string += (
                    f"**🚀 {job['companyName']}** ({time_period['startDate']['month']},"
                    f"{time_period['startDate']['year']} to {time_period['endDate']['month']}, "
                    f"{time_period['endDate']['year']})\n*{job['title']}*\n\n"
                )
            else:
                time_string += (
                    f"**🚀 {job['companyName']}** ({time_period['startDate']['month']}, "
                    f"{time_period['startDate']['year']} to Present)\n*{job['title']}*\n\n"
                )

        school_string = ""
        for education in get_profile["education"]:
            school_string += (
                f"**🎖 {education['schoolName']}** - {education['fieldOfStudy']}\n\n"
            )

        description = (
            f"**{get_profile['headline']}**\n\n"
            f"Based in {get_profile['geoLocationName']}, {get_profile['location']['basicLocation']['countryCode'].upper()}, "
            f"{get_profile['firstName']} is currently working in the **{get_profile['industryName']}** industry.\n\n"
            f"__Here's where {get_profile['firstName']} worked:__\n\n"
            f"{time_string}__Here's where {get_profile['firstName']} studied:__\n\n{school_string}"
        )

        colors = Colors()
        random_color = colors.random_color()
        final_color = discord.Colour(random_color)

        embed_content = discord.Embed(
            title=f"A look at {get_profile['firstName']} {get_profile['lastName']}'s profile.",
            type="rich",
            description=description,
            color=final_color,
        )

        embed_content.set_thumbnail(
            url=get_profile["displayPictureUrl"] + get_profile["img_100_100"]
        )

        await ctx.send(embed=embed_content)

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
