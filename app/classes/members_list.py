from app.exceptions import MemberAlreadyExists, MemberNotFound
from app.utils import word_capitalize
from app.classes.abc.message_manager import MessageManager


def parse_from_message(content):
    return content.splitlines()[1:]


class MemberList(MessageManager):

    def __init__(self, people_message, company_message):
        self.people_message = people_message
        self.company_message = company_message

        self.member_list = {
            'people': parse_from_message(people_message.content),
            'company': parse_from_message(company_message.content)
        }

    async def update(self):
        await self.people_message.edit(
            content='> __Adhérents :__\n' + '\n'.join(
                map(str.capitalize, self.member_list['people'])
            )
        )

        await self.company_message.edit(
            content='> __Entreprises :__\n' + '\n'.join(
                map(str.capitalize, self.member_list['company'])
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
