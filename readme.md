# 钉钉机器人智能助手
   	本项目使用Python3语言编写，使用 Sanic + Redis + RQ 实现钉钉中智能聊天助手，调用chatGPT API实现问答。

## 安装部署

钉钉机器人是一种功能强大的告警工具，它可以通过Webhook将告警消息发送到指定的钉钉群或个人。本项目使用Sanic作为Web框架，Redis作为消息队列，RQ作为任务调度工具，结合钉钉机器人实现了高效可靠的告警功能。

1. 克隆代码库到本地：

```shell
git clone https://github.com/zming/chatgpt-robot.git
cd chatgpt-robot
```
2. 安装依赖：

   ```shell
pip install -r requirements.txt
   ```
3. 配置文件：

   在工程下创建环境变量配置文件 .env

   ```shell
export PORT=7070
export APPKEY=应用KEY
export APPSECRET=应用秘钥
export OPENAI_MODEL=gpt-3.5-turbo
export OPENAI_API_KEY=OPNEAI-KEY
   ```

4. 启动应用：

   启动server服务端
   ```shell
   source .env
   python3 server.py
   ```

   启动worker端, 确保能科学上网
   ```shell
   source .env
   rq worker
   ```

## 使用方法

1. 其他接口：
   
   将服务地址 http://<server_host>:<server_port>/message 配置到钉钉微应用的机器人Webhook地址即可。
   
2. 其他接口：

    - `/status`：查看系统状态。

## 联系我们

如果您有任何问题或建议，请随时联系我们。

- 邮箱：qinzming@foxmail.com
- QQ：757731294