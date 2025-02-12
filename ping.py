

from datetime import datetime
from telethon.tl.functions.messages import GetPeerDialogsRequest
from telethon.tl.types import PeerUser
from .. import loader, utils

class UserPingMod(loader.Module):
    strings = {
        "name": "UserPingMod",
        "pinging": "🔄 Проверяю пинг...",
        "ping_result": "🏓 Пинг {}: {} ms",
        "user_not_found": "⚠ Не удалось найти пользователя!"
    }

    async def pingscmd(self, message):
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)

        user = None

        if reply:
            user = reply.sender_id
        elif args:
            try:
                if args.isnumeric():
                    user = int(args)
                else:
                    user_entity = await message.client.get_entity(args)
                    user = user_entity.id
            except Exception:
                pass

        if not user:
            await message.edit(self.strings["user_not_found"])
            return
        
        start = datetime.now()
        await message.edit(self.strings["pinging"])
        
        try:
            await message.client(GetPeerDialogsRequest(peers=[PeerUser(user)]))
        except Exception:
            await message.edit(self.strings["user_not_found"])
            return
        
        end = datetime.now()
        ping_time = (end - start).microseconds // 1000  

        await message.edit(self.strings["ping_result"].format(user, ping_time))
