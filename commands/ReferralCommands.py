from discord import Embed, Colour, User
from discord.ext.commands import Cog
from discord_slash.cog_ext import cog_slash
from discord_slash.utils import manage_commands as mc
from discord.utils import get
from utils.config import *
from utils.utils import *
from utils.event_util import get_embed_time_string
from discord.errors import Forbidden
from discord.ext import tasks

from database.referrals import *
from logging import info

"""
Used this article as a guide for tracking invites:
https://medium.com/@tonite/finding-the-invite-code-a-user-used-to-join-your-discord-server-using-discord-py-5e3734b8f21f
"""

# TODO: add check in the database method to see if the user has already been referred, in which case return False and handle it here
# TODO: add referrals leaderboard
# TODO: issue prizes to those who refer players
# TODO: implement has_user_played

class ReferralCommands(Cog, name="Referral Commands"):
    def __init__(self, bot):
        self.bot = bot
        self.invite_cache = {}

    @Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            self.bot_channel = self.bot.get_channel(BOT_OUTPUT_CHANNEL)
            self.invite_cache[guild.id] = await guild.invites()

    @Cog.listener()
    async def on_member_join(self, member):
        invites_before_join = self.invite_cache[member.guild.id]
        invites_after_join = await member.guild.invites()
        for invite in invites_before_join:
            if invite.uses < self.find_invite_by_code(invites_after_join, invite.code).uses:
                self.invite_cache[member.guild.id] = invites_after_join
                if log_referral(invite.code, member.id, invite.inviter.id):
                    info(f"Logged new referral of member '{member.name}' who was referred by '{invite.inviter.name}'")
                    await self.bot_channel.send(
                        f"Logged new referral of member {member.mention} who was referred by {invite.inviter.mention}"
                    )
                else:
                    info(f"{member.name} joined the server, but was already referred")
                    await self.bot_channel.send(
                        f"{member.mention} joined using invite code {invite.code} created by {invite.inviter.name}. "
                        f"No referral logged - they have been referred before."
                    )

    @Cog.listener()
    async def on_member_remove(self, member):
        self.invite_cache[member.guild.id] = await member.guild.invites()

    
    @staticmethod
    def find_invite_by_code(invite_list, code):
        for invite in invite_list:
            if invite.code == code:
                return invite