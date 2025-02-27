from tgju import tgju
import asyncio

arz=tgju()

async def main():
    try:
        await arz.req()
        arz.is_jalai
        res=arz.extract_multi(["price_eur","price_dollar_rl"])
        print(res)
    except Exception as e:
        arz.logger(e)
while True:
    asyncio.run(main())