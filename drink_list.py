from exceptions import DrinkAlreadyExists, DrinkNotFound


def get_int(string):
    return int(''.join(ch for ch in string if ch.isdigit()))


def parse_from_message(content):
    lines = content.splitlines()

    d = {}
    for line in lines[1:]:
        line_elements = line.split('`')
        d[line_elements[1]] = get_int(line_elements[2])

    return d


class DrinkList:

    def __init__(self, message):
        self.drink_list_message = message
        self.drink_list = parse_from_message(message.content)

    async def update(self):
        await self.drink_list_message.edit(
            content='**Liste des boissons:**\n' + '\n'.join(
                f"- `{key}` **x{val:,}**"
                for key, val in self.drink_list.items()
            )
        )

    async def create(self, drink_name):
        if drink_name in self.drink_list:
            raise DrinkAlreadyExists(drink_name)

        self.drink_list[drink_name] = 1
        await self.update()

    async def add(self, drink_name, n=1):
        if drink_name not in self.drink_list:
            raise DrinkNotFound(drink_name)

        self.drink_list[drink_name] += n
        await self.update()

    async def remove(self, drink_name, n=1):
        if drink_name not in self.drink_list:
            raise DrinkNotFound(drink_name)

        self.drink_list[drink_name] = max(self.drink_list[drink_name] - n, 0)
        await self.update()

    async def delete(self, drink_name):
        if drink_name not in self.drink_list:
            raise DrinkNotFound(drink_name)

        self.drink_list.pop(drink_name)
        await self.update()
