# TeleMonitor

TeleMonitor 是一个使用 Python 编写的系统监控工具，它可以监控 CPU、内存和磁盘的使用情况，并通过 Telegram 发送警告。

## 安装

首先，你需要在你的系统上安装 Docker。然后，你可以使用以下命令来构建和运行 Docker 镜像：

pass

## 使用

你可以通过设置环境变量来配置 Telemonitor：

- `TG_API_TOKEN`: 你的 Telegram bot 的 API token。
- `TG_CHAT_ID`: 你希望接收警告的 Telegram chat ID。
- `CPU_PERCENT`: CPU 使用率的阈值，超过这个阈值时，Telemonitor 会发送警告。
- `MEMORY_PERCENT`: 内存使用率的阈值，超过这个阈值时，Telemonitor 会发送警告。
- `DISK_PERCENT`: 磁盘使用率的阈值，超过这个阈值时，Telemonitor 会发送警告。
- `MONITOR_INTERVAL`: 监控的间隔时间（秒）。

在 Telegram 中，你可以使用 `/status` 命令来获取系统的当前状态。

## 许可证

这个项目使用 MIT 许可证，详情请见 [LICENSE](LICENSE) 文件。
