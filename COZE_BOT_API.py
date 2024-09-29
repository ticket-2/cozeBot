# -*- coding:utf-8 -*-
"""
作者：Ulquiorra
日期：2024年09月29日
"""

import aiohttp
import asyncio
import ssl
import json
from quart import Quart, websocket, render_template

COZE_BOT_API = Quart(__name__)

API_URL = 'https://api.coze.cn/v3/chat'
API_KEY = 'pat_***********************************'
BOT_ID = '*************************'
USER_ID = 'test_user_001'

# 创建不验证 SSL 证书的上下文
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# 流式获取 Bot 的消息
async def fetch_stream(message):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        "bot_id": BOT_ID,
        "user_id": USER_ID,
        "stream": True,
        "auto_save_history": True,
        "additional_messages": [
            {
                "role": "user",
                "content": message,
                "content_type": "text"
            }
        ]
    }

    bot_response = ""
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=payload, ssl=ssl_context) as resp:
            async for line in resp.content:
                if line:
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line.startswith('data:'):
                        try:
                            json_data = json.loads(decoded_line[5:])
                            if 'content' in json_data and 'msg_type' not in json_data:
                                content = json_data['content']
                                if "{" not in content and "}" not in content:
                                    # 检查新内容是否与上一次添加的内容相同
                                    if not bot_response.endswith(content):
                                        bot_response += content
                        except json.JSONDecodeError:
                            continue
    return bot_response

# 渲染首页 HTML
@COZE_BOT_API.route('/')
async def index():
    return await render_template('index.html')

# WebSocket 路由，用于处理消息的发送和接收
@COZE_BOT_API.websocket('/ws')
async def ws():
    while True:
        message = await websocket.receive()  # 接收前端发送的消息
        bot_response = await fetch_stream(message)  # 从流式 API 获取 Bot 响应
        await websocket.send(bot_response)  # 将响应发送回前端

if __name__ == '__main__':
    #app.run(debug=True, port=8080)
    COZE_BOT_API.run(debug = True, port = 8080)
