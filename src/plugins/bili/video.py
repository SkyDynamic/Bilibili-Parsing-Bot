from bilibili_api import video
import asyncio
import nest_asyncio
nest_asyncio.apply()
class Video():
    def __init__(self, bvid):
        asyncio.get_event_loop().run_until_complete(self.main(bvid))

    async def main(self, bvid):
        try:
            v = video.Video(str(bvid))
            self.data = await v.get_info()
            self.status = True
        except Exception as e:
            self.status = False
            self.data = str(e)