import asyncio

import motiondev


async def main() -> None:
    token = 'gYqbfzfumDYAYzwRuZMVYleXkeQpMpQNpXwSqDpa.IwNESQeMUb.EddEWpRwpwkQCpMeCXSvbDNLNQKSdTHKxCJ.WZiSoyvKbDzGkWD'
    client = motiondev.Client(token)

    async with client:
        bot = await client.get_bot(741592089342640198)
        print(bot.id)
        print(bot.name)
        print(bot.avatar_url)
        print(bot.status)
        print(bot.discord)
        print(bot.invite)
        print(bot.library)
        print(bot.list_date)
        print(bot.prefix)
        print(bot.servers)
        print(bot.site)
        print(bot.public_flags)
        print(bot.topics)
        print(bot.vanity_url)
        print(bot.big_description)
        print(bot.small_description)
        print(bot.owner)
        print(bot.co_owners)
        print(bot.public_flags)

asyncio.get_event_loop().run_until_complete(main())
