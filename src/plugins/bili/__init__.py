from ast import Or
from nonebot import on_command, on_keyword
from nonebot.adapters.onebot.v11 import Bot, GROUP
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from .video import Video
from .config import *

import requests
import re

helpmessage = '''/video + BV号 解析视频
/bilitool off 关闭自动解析
/bilitool on 开启自动解析
注：
当自动解析开启后，会自动解析信息中第一个BV号的视频
'''

video_msg = on_command('video', permission=GROUP, priority=0, block=True)
@video_msg.handle()
async def video_main(bot: Bot, mathcer: Matcher, event: GroupMessageEvent ,args: Message = CommandArg()):
    info = await Video(args)
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
        await video_msg.finish(reply + pic + msg)
    if info.status == False:
        await video_msg.finish(reply + data)

auto_analysis = on_keyword(['BV','bv','bV','Bv','b23.tv'],permission=GROUP,priority=49)
@auto_analysis.handle()
async def analysis(bot: Bot, mathcer: Matcher, event: GroupMessageEvent):
    group_json = Config_Read().group
    if str(event.group_id) not in group_json:
        group_json[str(event.group_id)] = False
        Config_Write(group_json)
    if group_json[str(event.group_id)] == False:
        pass
    if group_json[str(event.group_id)] == True:
        Original_Msg = str(event.get_message())
        if 'http://b23.tv/' or 'https://b23.tv/' in Original_Msg:
            try:
                urlnum = re.search('https://b23.tv/', Original_Msg, re.IGNORECASE).span()
            except AttributeError:
                urlnum = re.search('http://b23.tv/', Original_Msg, re.IGNORECASE).span()
            url = Original_Msg[int(urlnum[0]) : int(urlnum[1] + 7)]
            resp = requests.get(url)
            bvid = get_bvid(str(resp.url))
        else:
            bvid = get_bvid(Original_Msg)
        info = await Video(bvid)
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
            await auto_analysis.finish(reply + pic + msg)
        if info.status == False:
            pass

def get_bvid(msg):
        bvnum = re.search('BV', msg, re.IGNORECASE).span()
        start_num = int(bvnum[0])
        bvid = msg[start_num: start_num + 12]
        return bvid

function = on_command('bilitool',permission=GROUP,priority=49)
@function.handle()
async def function(bot: Bot, mathcer: Matcher, event: GroupMessageEvent ,args: Message = CommandArg()):
    arg = str(args)
    if arg == 'off':
        group_json = Config_Read().group
        group_json[str(event.group_id)] = False
        Config_Write(group_json)
        await auto_analysis.finish('此群的BV号自动解析已关闭')
    if arg == 'on':
        group_json = Config_Read().group
        group_json[str(event.group_id)] = True
        Config_Write(group_json)
        await auto_analysis.finish('此群的BV号自动解析已开启')
    if arg == 'help' or arg == '':
        await auto_analysis.finish(helpmessage)
