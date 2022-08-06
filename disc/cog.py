import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashContext

from job_boards_scrapers import LinkedIn
from utils import Colors

class Descriptions:
    POST_JOB = "Parse a job post's information beautifully in the channel"
    HELP = "Display the list of commands and their usages"


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="post-job", description=Descriptions.POST_JOB)
    async def _post_job(self, ctx: SlashContext, job):
        linkedin = LinkedIn()
        data = linkedin.get_job_info(job)

        colors = Colors()
        random_color = colors.random_color()
        final_color = discord.Colour(random_color)

        description = f"**{data.company}**\n*{data.title}*\n\n\
                Location: {data.location}.\n\n\
                This job was posted __{data.posted_time_ago}__.\n\
                {data.summary}\n\nApply Now: {data.url}\n"

        embed_content = discord.Embed(
            title="Check out this job on LinkedIn!",
            type="rich",
            description=description,
            color=final_color
        )
        embed_content.set_image(url=f"{data.company_pic_url}")
        
        await ctx.send(embed=embed_content)

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
