import datetime
import platform
import psutil
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, Application
from telegram.helpers import escape_markdown
import os
import httpx


def get_language():
    return os.environ.get('LANGUAGE', 'en')


def get_message(key, **kwargs):
    messages = {
        'en': {
            'help': "👋 Use /status to get system information",
            'boot': "🎮 *Genshin Impact started\!*",
            'cpu_warning': "⚠️ *Warning*: CPU usage has reached *{usage}%*\! Threshold set to *{threshold}%*\.",
            'url_warning': "⚠️ *Warning*: {url} status code is *{status_code}*",
            'url_access_failed': "⚠️ *Warning*: {url} access failed",
            'memory_warning': "⚠️ *Warning*: Memory usage has reached *{usage}%*\! Threshold set to *{threshold}%*\.",
            'disk_warning': "⚠️ *Warning*: Disk usage has reached *{usage}%*\! Threshold set to *{threshold}%*\.",
            'system_info': """
📊 **System Information**\n
🌍 *System Name:* {system_name}
📌 *Hostname:* {hostname}
🖥️ *CPU Usage:* {cpu_usage}%
🧠 *Memory Usage:* {memory_usage}%
💽 *Disk Usage:* {disk_usage}%
👾 *Process Count:* {process_count}
🕰️ *Uptime:* {uptime}
🌐 *Network Info:*
    📤 Bytes Sent: {bytes_sent} GB
    📥 Bytes Recv: {bytes_recv} GB
🔗 *Monitor URL:*
{urls_info}
        """
        },
        'cn': {
            'help': "👋 使用 /status 来获取系统信息",
            'boot': "🎮 *原神启动\!*",
            'cpu_warning': "⚠️ *警告*: CPU 使用率已经达到 *{usage}%*\! 阈值设置为 *{threshold}%*\.",
            'url_warning': "⚠️ *警告*: {url} 状态码为 *{status_code}*",
            'url_access_failed': "⚠️ *警告*: {url} 访问失败",
            'memory_warning': "⚠️ *警告*: 内存使用率已经达到 *{usage}%*\! 阈值设置为 *{threshold}%*\.",
            'disk_warning': "⚠️ *警告*: 磁盘使用率已经达到 *{usage}%*\! 阈值设置为 *{threshold}%*\.",
            'system_info': """
📊 **系统信息**\n
🌍 *系统名称:* {system_name}
📌 *主机名:* {hostname}
🖥️ *CPU使用率:* {cpu_usage}%
🧠 *内存使用率:* {memory_usage}%
💽 *磁盘使用率:* {disk_usage}%
👾 *进程数量:* {process_count}
🕰️ *开机时间:* {uptime}
🌐 *网络信息:*
    📤 已发送: {bytes_sent} GB
    📥 已接收: {bytes_recv} GB
🔗 *监控URL:*
{urls_info}
        """
        }
    }
    language = get_language()
    return messages[language].get(key, '').format(**kwargs)


async def monitor_cpu_usage(context: ContextTypes.DEFAULT_TYPE):
    cpu_percent = int(context.job.data)
    cpu_usage = int(psutil.cpu_percent(interval=1))
    if cpu_usage >= cpu_percent:
        message = get_message('cpu_warning', usage=cpu_usage,
                              threshold=cpu_percent)
        await context.bot.send_message(chat_id=context.job.chat_id, text=message, parse_mode="MarkdownV2")


async def monitor_url(context: ContextTypes.DEFAULT_TYPE):
    url_list = context.job.data.split(',')
    for url in url_list:
        try:
            response = httpx.get(url)
            url = escape_markdown(url, version=2)
            if response.status_code != 200:
                message = get_message('url_warning', url=url,
                                      status_code=response.status_code)
                await context.bot.send_message(chat_id=context.job.chat_id, text=message, parse_mode="MarkdownV2",
                                               disable_web_page_preview=True)
        except Exception as e:
            message = get_message('url_access_failed', url=url)
            await context.bot.send_message(chat_id=context.job.chat_id, text=message, parse_mode="MarkdownV2",
                                           disable_web_page_preview=True)


async def monitor_memory_usage(context: ContextTypes.DEFAULT_TYPE):
    memory_percent = int(context.job.data)
    memory_info = psutil.virtual_memory()
    memory_usage = int(memory_info.percent)
    if memory_usage >= memory_percent:
        message = get_message('memory_warning', usage=memory_usage,
                              threshold=memory_percent)
        await context.bot.send_message(chat_id=context.job.chat_id, text=message, parse_mode="MarkdownV2")


async def monitor_disk_usage(context: ContextTypes.DEFAULT_TYPE):
    disk_path = os.environ.get('DISK_PATH', '/host')
    disk_percent = int(context.job.data)
    disk_info = psutil.disk_usage(disk_path)
    disk_usage = int(disk_info.percent)
    if disk_usage >= disk_percent:
        message = get_message('disk_warning', usage=disk_usage,
                              threshold=disk_percent)
        await context.bot.send_message(chat_id=context.job.chat_id, text=message, parse_mode="MarkdownV2")


def get_systeminfo():
    disk_path = os.environ.get('DISK_PATH', '/host')
    # Get CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)

    # Get memory usage
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent

    # Get disk usage
    disk_info = psutil.disk_usage(disk_path)
    disk_usage = disk_info.percent

    # Get network info
    net_info = psutil.net_io_counters()
    bytes_sent = net_info.bytes_sent / (1024 ** 3)  # Convert to GB
    bytes_recv = net_info.bytes_recv / (1024 ** 3)  # Convert to GB

    # Get process info
    process_count = len(list(psutil.process_iter()))

    # Get boot time
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    current_time = datetime.datetime.now()
    uptime = current_time - boot_time
    uptime = str(uptime).split('.')[0]  # Remove the microseconds

    # Get system name and hostname
    system_name = platform.platform()  # e.g., "Linux", "Windows", "macOS"
    hostname = platform.node()  # e.g., "hostname.domain.com"

    return cpu_usage, memory_usage, disk_usage, bytes_sent, bytes_recv, process_count, uptime, system_name, hostname


async def reply_systeminfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the system information
    cpu_usage, memory_usage, disk_usage, bytes_sent, bytes_recv, process_count, uptime, system_name, hostname = get_systeminfo()
    system_name = escape_markdown(system_name, version=2)
    hostname = escape_markdown(hostname, version=2)
    cpu_usage = int(cpu_usage)
    memory_usage = int(memory_usage)
    disk_usage = int(disk_usage)
    bytes_sent = int(bytes_sent)
    bytes_recv = int(bytes_recv)
    url_list = os.environ.get('URL_LIST', 'https://www.baidu.com').split(',')
    urls_info = ""
    for url in url_list:
        url = escape_markdown(url, version=2)
        urls_info = urls_info + f"\- {url}\n"
    message = get_message( 'system_info',
                          cpu_usage=cpu_usage, memory_usage=memory_usage, disk_usage=disk_usage,
                          bytes_sent=bytes_sent, bytes_recv=bytes_recv, process_count=process_count,
                          uptime=uptime, system_name=system_name, hostname=hostname, urls_info=urls_info)
    await update.message.reply_text(message, parse_mode="MarkdownV2", disable_web_page_preview=True)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = get_message( 'help')
    await update.message.reply_text(message, parse_mode="MarkdownV2")


async def boot(context: ContextTypes.DEFAULT_TYPE):
    message = get_message('boot')
    await context.bot.send_message(chat_id=context.job.chat_id, text=message, parse_mode="MarkdownV2")


def main() -> None:
    tg_api_token = os.environ['TG_API_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']
    cpu_percent = os.environ.get('CPU_PERCENT', '80')
    memory_percent = os.environ.get('MEMORY_PERCENT', '80')
    disk_percent = os.environ.get('DISK_PERCENT', '80')
    monitor_interval = int(os.environ.get('MONITOR_INTERVAL', '60'))
    tg_api_base_url = os.environ.get('TG_API_BASE_URL', 'https://api.telegram.org/bot')
    url_list = os.environ.get('URL_LIST', 'https://www.baidu.com')
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().connect_timeout(30).read_timeout(30).base_url(
        base_url=tg_api_base_url).token(tg_api_token).build()
    job_queue = application.job_queue
    job_queue.run_repeating(monitor_cpu_usage, interval=monitor_interval, first=10, chat_id=tg_chat_id,
                            data=cpu_percent)
    job_queue.run_repeating(monitor_disk_usage, interval=monitor_interval, first=10, chat_id=tg_chat_id,
                            data=memory_percent)
    job_queue.run_repeating(monitor_memory_usage, interval=monitor_interval, first=10, chat_id=tg_chat_id,
                            data=disk_percent)
    job_queue.run_repeating(monitor_url, interval=monitor_interval, first=10, chat_id=tg_chat_id, data=url_list)
    job_queue.run_once(boot, chat_id=tg_chat_id, when=2)
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], help))
    application.add_handler(CommandHandler("status", reply_systeminfo))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
