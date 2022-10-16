import discord
from utils import Colors
from typing import Dict, Any
from linkedin_profile_api_wrappers import LinkedinProfile
from discord_slash.utils.manage_components import create_actionrow, create_button
from discord_slash.model import ButtonStyle


def something_wrong_message():
    return {
        "content": (
            "Hi there! Seems like something wrong has occured :( "
            "Please try again!"
        ),
        "hidden": True,
    }


def linkedin_profile_info_message(profile: LinkedinProfile) -> Dict[str, Any]:
    experience = {exp.company_name: [] for exp in profile.experience}
    [experience[exp.company_name].append(exp) for exp in profile.experience]
    
    exp_string = ""
    for company_name, positions in experience.items():
        exp_string += (
            f"**🚀 [{company_name}]({positions[0].company_url})**\n"
        )
        for position in positions:
            exp_string += (
                f"{position.title} | "
                f"*{position.start_date} - {position.end_date}*\n"
            )
        exp_string += "\n"

    school_string = "".join(
        [f"**🎖 [{ed.school}]({ed.school_url})**\n\n" for ed in profile.education]
    )

    description = (
        f"**{profile.headline}**\n\n"
        + (f"*{profile.about}*\n\n" if profile.about else "")
        + (
            f"**__Here's {profile.name}'s experience so far:__**\n\n{exp_string}\n"
            if exp_string
            else ""
        )
        + (
            f"**__Here's where {profile.name} studied:__**\n\n{school_string}"
            if school_string
            else ""
        )
    )

    colors = Colors()
    random_color = colors.random_color()
    final_color = discord.Colour(random_color)

    embed_content = discord.Embed(
        title=f"A look at {profile.name}'s profile.",
        type="rich",
        color=final_color,
        description=description
    )
    embed_content.set_thumbnail(url=profile.profile_image_url)

    view_button = create_button(style=ButtonStyle.URL, label=f"View on LinkedIn", url=profile.linkedin_url)
    action_row = create_actionrow(view_button)

    return {"embed": embed_content, "components": [action_row]}
