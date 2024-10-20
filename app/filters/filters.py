from aiogram import types
from aiogram.filters import BaseFilter

import app.localdata.load as localdata


class check_ban(BaseFilter):

    def __init__(self, banlist_users) -> None:
        self.banlist_users = localdata.localBannedUsers

    async def __call__(self, message: types.Message) -> bool:
        for row in range(len(self.banlist_users)):
            if self.banlist_users[row]["uid"] == message.from_user.id:
                return True
        else:
            return False