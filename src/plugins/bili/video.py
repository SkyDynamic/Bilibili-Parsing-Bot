from bilibili_api import video

class Video():
    async def __new__(self, bvid):
        await self.main(self, bvid)
        return self

    async def main(self, bvid):
        try:
            v = video.Video(str(bvid))
            self.data = await v.get_info()
            self.status = True
        except Exception as e:
            self.status = False
            self.data = str(e)
