# TeleMonitor

TeleMonitor 是一个使用 Python 编写的系统监控工具，它可以监控 CPU、内存和磁盘的使用情况，并通过 Telegram 发送警告。

## 使用

首先，你需要创建一个 Telegram bot，然后获取 API token。你可以参考 [Telegram 官方文档](https://core.telegram.org/bots/features#botfather) 来创建一个 Telegram bot。

然后，你需要获取你希望接收警告的 Telegram chat ID。你可以使用 [@userinfobot](https://t.me/userinfobot) 来获取你的 chat ID。

接下来clone这个项目：

```bash
git clone https://github.com/bboysoulcn/telemonitor.git
```

你可以使用docker compose 来运行 Telemonitor：

```bash
docker-compose up -d
```

或者你可以使用 k8s 来运行 Telemonitor：
    
```bash
kubectl apply -f deployment.yaml
```


下面是 Telemonitor 的环境变量：

- `TG_API_TOKEN`: 你的 Telegram bot 的 API token。
- `TG_CHAT_ID`: 你希望接收警告的 Telegram chat ID。
- `CPU_PERCENT`: CPU 使用率的阈值，超过这个阈值时，Telemonitor 会发送警告。
- `MEMORY_PERCENT`: 内存使用率的阈值，超过这个阈值时，Telemonitor 会发送警告。
- `DISK_PERCENT`: 磁盘使用率的阈值，超过这个阈值时，Telemonitor 会发送警告。
- `MONITOR_INTERVAL`: 监控的间隔时间（秒）。

下面是机器人的命令：

- /start - 获取帮助
- /help - 获取帮助
- /status - 获取系统状态

## 许可证

这个项目使用 MIT 许可证，详情请见 [LICENSE](LICENSE) 文件。
