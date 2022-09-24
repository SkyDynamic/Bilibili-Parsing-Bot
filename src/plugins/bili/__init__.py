from nonebot import on_command, on_keyword
from nonebot.adapters.onebot.v11 import Bot, GROUP
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from .video import Video
from .config import *

import re

helpmessage = '''/video + BV号 解析视频
/bilitool off 关闭自动解析
/bilitool on 开启自动解析
注：
当自动解析开启后，会自动解析信息中第一个BV号的视频
'''

video_msg = on_command('video', permission=GROUP, priority=50)
@video_msg.handle()
async def video_main(bot: Bot, mathcer: Matcher, event: GroupMessageEvent ,args: Message = CommandArg()):
    info = Video(args)
    data = info.data
    reply = MessageSegment.reply(event.message_id)
    if info.status == True:
        bvid = args
        avid = data.get('aid')
        pic = MessageSegment.image(data.get('pic'))
        tname = data.get('tname')
        title = data.get('title')
        desc = data.get('desc')
        author = data.get('owner').get('name')
        msg = f'视频号：{bvid}  av{avid}\n标题：{title}\n简介：\n{desc}\n\n类型：{tname}\n作者：{author}\n视频链接：\nhttps://bilibili.com/video/{bvid}\nhttps://bilibili.com/video/av{avid}'
        await video_msg.send(reply + pic + msg)
    if info.status == False:
        await video_msg.send(reply + data)

auto_analysis = on_keyword(['BV','bv','bV','Bv'],permission=GROUP,priority=49)
@auto_analysis.handle()
async def analysis(bot: Bot, mathcer: Matcher, event: GroupMessageEvent):
    group_json = Config_Read().group
    if str(event.group_id) not in group_json:
        group_json[str(event.group_id)] = True
        Config_Write(group_json)
    if group_json[str(event.group_id)] == False:
        pass
    if group_json[str(event.group_id)] == True:
        bvnum = re.search('BV|bv|bV|Bv', str(event.get_message())).span()
        start_num = int(bvnum[0])
        bvid = str(event.get_message())[start_num: start_num + 12]
        info = Video(bvid)
        data = info.data
        reply = MessageSegment.reply(event.message_id)
        if info.status == True:
            avid = data.get('aid')
            pic = MessageSegment.image(data.get('pic'))
            tname = data.get('tname')
            title = data.get('title')
            desc = data.get('desc')
            author = data.get('owner').get('name')
            msg = f'视频号：{bvid}  av{avid}\n标题：{title}\n简介：\n{desc}\n\n类型：{tname}\n作者：{author}\n视频链接：\nhttps://bilibili.com/video/{bvid}\nhttps://bilibili.com/video/av{avid}'
            await auto_analysis.send(reply + pic + msg)
        if info.status == False:
            pass

function = on_command('bilitool',permission=GROUP,priority=49)
@function.handle()
async def function(bot: Bot, mathcer: Matcher, event: GroupMessageEvent ,args: Message = CommandArg()):
    arg = str(args)
    if arg == 'off':
        group_json = Config_Read().group
        group_json[str(event.group_id)] = False
        Config_Write(group_json)
        await auto_analysis.send('此群的BV号自动解析已关闭')
    if arg == 'on':
        group_json = Config_Read().group
        group_json[str(event.group_id)] = True
        Config_Write(group_json)
        await auto_analysis.send('此群的BV号自动解析已开启')
    if arg == 'help' or arg == '':
        await auto_analysis.send(helpmessage)