import logging
from http.client import InvalidURL

from discord.ext import commands
from discord_slash import SlashContext, cog_ext

from disc.message_generators import Descriptions, help_message, server_error_message
from disc.message_generators.job_posting import invalid_url_message, job_info_message
from disc.message_generators.linkedin_profile import (
    linkedin_profile_info_message,
    something_wrong_message,
)
from job_api_wrapers import get_linkedin_job_info
from linkedin_profile_api_wrappers import get_profile

_LOGGER = logging.getLogger(__name__)


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="post-job", description=Descriptions.POST_JOB)
    async def _post_job(self, ctx: SlashContext, url_or_jobid: str):
        job = int(url_or_jobid) if url_or_jobid.isnumeric() else url_or_jobid

        try:
            data = get_linkedin_job_info(job)
        except InvalidURL:
            await ctx.send(**invalid_url_message())
            _LOGGER.info("Sent private message to user notifying given url is invalid.")
            return

        if data is None:
            await ctx.send(**server_error_message())

        await ctx.send(**job_info_message(data))

    @cog_ext.cog_slash(
        name="view-profile", description=Descriptions.VIEW_LINKEDIN_PROFILE
    )
    async def _view_profile(self, ctx: SlashContext, profile: str):
        await ctx.send("Hang on, grabbing details for you...", hidden=True)

        profile = get_profile(profile)
        if not profile:
            await ctx.send(**something_wrong_message())
            return

        await ctx.send(**linkedin_profile_info_message(profile))

    @cog_ext.cog_slash(name="help", description=Descriptions.HELP)
    async def _help(self, ctx: SlashContext):
        await ctx.send(**help_message())


def setup(bot):
    bot.add_cog(Slash(bot))
