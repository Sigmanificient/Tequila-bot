import discord

from app.exceptions import MemberAlreadyExists, MemberNotFound
from app.utils import word_capitalize
from app.classes.abc.message_manager import MessageManager


class MemberList(MessageManager):

    def __init__(self, message):
        self.message = message
        fields = message.embeds[0].fields

        self.member_list = {
            'people': fields[0].value.splitlines(),
            'company': fields[1].value.splitlines()
        }

    async def update(self):
        await self.message.edit(
            embed=discord.Embed(
                description=get_embed_description()
            ).add_field(
                name='__Adhérents__:',
                value='\n'.join(
                    map(str.capitalize, self.member_list['people'])
                )
            ).add_field(
                name='__Entreprises__:',
                value='\n'.join(
                    map(str.capitalize, self.member_list['company'])
                )
            )
        )

    async def add(self, member_name, member_type):
        member_name = word_capitalize(member_name)

        if member_name in self.member_list[member_type]:
            raise MemberAlreadyExists(member_name, member_type)

        self.member_list[member_type].append(member_name)
        await self.update()

    async def remove(self, member_name, member_type):
        member_name = word_capitalize(member_name)

        if member_name not in self.member_list[member_type]:
            raise MemberNotFound(member_name, member_type)

        self.member_list[member_type].remove(member_name)
        await self.update()


def get_embed_description() -> str:
    with open('assets/members_description.txt', encoding='utf-8') as f:
        return f.read()
