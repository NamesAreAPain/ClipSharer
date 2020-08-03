import discord
from PIL import ImageGrab
import win32clipboard as wclip
import time
import asyncio

class GameClipper(discord.Client):
    def __init__(self,*args,post_to=None,**kwargs):
        super().__init__(*args,**kwargs)
        self.post_to = post_to
        self.bg_task = self.loop.create_task(self.my_bg_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        channel = self.get_channel(self.post_to)
        print("Sent")

    async def my_bg_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(self.post_to)
        while not self.is_closed():
            im = ImageGrab.grabclipboard()
            if im != None:
                print("Got An Image!");
                now = int(round(time.time() * 1000))
                filename = f"{now}.png"
                im.save(filename,"PNG")
                print("Image Saved")
                wclip.OpenClipboard()
                wclip.EmptyClipboard()
                wclip.CloseClipboard()
                print("Clipboard cleared")
                print(f"Sending Image to channel {channel.name}...")
                if channel != None:
                    await channel.send(now,file=discord.File(filename))
                print("Image Sent!")
            await asyncio.sleep(1)

with open("token.txt","r") as tokenfile, open("channel.txt","r") as channelfile:
    token = tokenfile.read()
    post_to = int(channelfile.read())
client = GameClipper(post_to=post_to)
client.run(token)
