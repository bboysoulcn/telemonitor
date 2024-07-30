[中文](README_CN.md) | [English](README.md)

# TeleMonitor

TeleMonitor is a system monitoring tool written in Python that can monitor CPU, memory, and disk usage and send alerts via Telegram.

## Usage

First, you need to create a Telegram bot and get the API token. You can refer to the [Telegram official documentation](https://core.telegram.org/bots/features#botfather) to create a Telegram bot.

Then, you need to get the Telegram chat ID where you want to receive alerts. You can use [@userinfobot](https://t.me/userinfobot) to get your chat ID.

Next, clone this project:

```bash
git clone https://github.com/bboysoulcn/telemonitor.git
```

You can use docker compose to run TeleMonitor:

```bash
docker-compose up -d
```

Or you can use k8s to run TeleMonitor:

```bash
kubectl apply -f deployment.yaml
```

Here are the environment variables for TeleMonitor:

- `TG_API_TOKEN`: The API token of your Telegram bot.
- `TG_CHAT_ID`: The Telegram chat ID where you want to receive alerts.
- `TG_API_BASE_URL`: The base URL of the Telegram API, default is `https://api.telegram.org`.
- `CPU_PERCENT`: The threshold for CPU usage. TeleMonitor will send an alert if the usage exceeds this value. Default is 80.
- `MEMORY_PERCENT`: The threshold for memory usage. TeleMonitor will send an alert if the usage exceeds this value. Default is 80.
- `DISK_PERCENT`: The threshold for disk usage. TeleMonitor will send an alert if the usage exceeds this value. Default is 80.
- `MONITOR_INTERVAL`: The interval time (in seconds) for monitoring. Default is 60.
- `DISK_PATH`: The path of the disk. Default is `/host`.
- `URL_LIST`: The list of URLs to monitor, separated by commas. Default is empty.
- `LANGUAGE`: The language. Default is `en`. Options are `en` and `cn`.

Here are the commands for the bot:

- /start - Get help
- /help - Get help
- /status - Get system status

### If you cannot access the Telegram API

You can use the following project to create an API proxy and modify the environment variable `TG_API_BASE_URL`:

[teleproxy](https://github.com/bboysoulcn/teleproxy)

### Demo

![](./images/img1.webp)
![](./images/img2.webp)

## Contributors

- [SimonGino](https://github.com/SimonGino)

## Telegram Channel

My telegram channel: [https://t.me/bboysoulcn](https://t.me/bboysoulcn)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.