COZE BOT
1.BOT API： python COZE_BOT_API.py

2.web sdk(加入到body中)：
<script src="https://lf-cdn.coze.cn/obj/unpkg/flow-platform/chat-app-sdk/0.1.0-beta.6/libs/cn/index.js"></script>
      <script>
          new CozeWebSDK.WebChatClient({
            config: {
              bot_id: '***********',
            },
            componentProps: {
              title: 'Coze',
            },
          });
      </script>