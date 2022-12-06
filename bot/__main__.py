from bs4 import BeautifulSoup
from signal import signal, SIGINT
from requests import get as rget
from urllib.parse import quote as q
from random import choice as rchoice
from os import path as ospath, remove as osremove, execl as osexecl
from subprocess import run as srun, check_output
from datetime import datetime, timedelta
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
from time import time
from sys import executable
from telegram import ParseMode
from telegram.ext import CommandHandler
from pytz import timezone
from bot import *
from .helper.ext_utils.fs_utils import start_cleanup, clean_all, exit_clean_up
from .helper.ext_utils.telegraph_helper import telegraph
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.ext_utils.db_handler import DbManger
from .helper.telegram_helper.bot_commands import BotCommands
from .helper.telegram_helper.message_utils import sendMessage, sendMarkup, editMessage, sendLogFile, sendPhoto
from .helper.telegram_helper.filters import CustomFilters
from .helper.telegram_helper.button_build import ButtonMaker
from bot.modules.wayback import getRandomUserAgent
from .modules import authorize, list, cancel_mirror, mirror_status, mirror_leech, clone, ytdlp, shell, eval, bot_settings, \
                     delete, count, users_settings, search, rss, wayback, speedtest, anilist, imdb, bt_select, mediainfo, hash, \
                     scraper, pictures
from datetime import datetime

def progress_bar(percentage):
    p_used = config_dict['FINISHED_PROGRESS_STR']
    p_total = config_dict['UN_FINISHED_PROGRESS_STR']
    if isinstance(percentage, str):
        return 'NaN'
    try:
        percentage=int(percentage)
    except:
        percentage = 0
    return ''.join(
        p_used if i <= percentage // 10 else p_total for i in range(1, 11)
    )


timez = config_dict['TIMEZONE']
now=datetime.now(timezone(f'{timez}'))

def stats(update, context):
    if ospath.exists('.git'):
        if config_dict['EMOJI_THEME']:
            last_commit = check_output(["git log -1 --date=short --pretty=format:'%cd \n<b>├</b> 🛠<b>From:</b> %cr'"], shell=True).decode()
            botVersion = check_output(["git log -1 --date=format:v%y.%m%d.%H%M --pretty=format:%cd"], shell=True).decode()
        else:
            last_commit = check_output(["git log -1 --date=short --pretty=format:'%cd \n<b>├  From:</b> %cr'"], shell=True).decode()
            botVersion = check_output(["git log -1 --date=format:v%y.%m%d.%H%M --pretty=format:%cd"], shell=True).decode()
    else:
        botVersion = 'No UPSTREAM_REPO'
        last_commit = 'No UPSTREAM_REPO'
    currentTime = get_readable_time(time() - botStartTime)
    current = now.strftime('%m/%d %I:%M:%S %p')
    osUptime = get_readable_time(time() - boot_time())
    total, used, free, disk= disk_usage('/')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(net_io_counters().bytes_sent)
    recv = get_readable_file_size(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    swap = swap_memory()
    swap_p = swap.percent
    swap_t = get_readable_file_size(swap.total)
    swap_u = get_readable_file_size(swap.used)
    memory = virtual_memory()
    mem_p = memory.percent
    mem_t = get_readable_file_size(memory.total)
    mem_a = get_readable_file_size(memory.available)
    mem_u = get_readable_file_size(memory.used)
    if config_dict['EMOJI_THEME']:
            stats = f'<b>╭─《🌐 BOT STATISTICS 🌐》</b>\n' \
                    f'<b>├ 🛠 Updated On: </b>{last_commit}\n'\
                    f'<b>├ ⌛ Uptime: </b>{currentTime}\n'\
                    f'<b>├ 🟢 OS Uptime: </b>{osUptime}\n'\
                    f'<b>├ 🖥️ CPU:</b> [{progress_bar(cpuUsage)}] {cpuUsage}%\n'\
                    f'<b>├ 🎮 RAM:</b> [{progress_bar(mem_p)}] {mem_p}%\n'\
                    f'<b>├ 💾 Disk:</b> [{progress_bar(disk)}] {disk}%\n'\
                    f'<b>├ 💿 Disk Free:</b> {free}\n'\
                    f'<b>├ 🔺 Upload Data:</b> {sent}\n'\
                    f'<b>╰ 🔻 Download Data:</b> {recv}\n\n'

    else:
            stats = f'<b>╭─《🌐 BOT STATISTICS 🌐》</b>\n' \
                    f'<b>├  Updated On: </b>{last_commit}\n'\
                    f'<b>├  Uptime: </b>{currentTime}\n'\
                    f'<b>├  OS Uptime: </b>{osUptime}\n'\
                    f'<b>├  CPU:</b> [{progress_bar(cpuUsage)}] {cpuUsage}%\n'\
                    f'<b>├  RAM:</b> [{progress_bar(mem_p)}] {mem_p}%\n'\
                    f'<b>├  Disk:</b> [{progress_bar(disk)}] {disk}%\n'\
                    f'<b>├  Disk Free:</b> {free}\n'\
                    f'<b>├  Upload Data:</b> {sent}\n'\
                    f'<b>╰  Download Data:</b> {recv}\n\n'



    if config_dict['SHOW_LIMITS_IN_STATS']:

        TORRENT_DIRECT_LIMIT = config_dict['TORRENT_DIRECT_LIMIT']
        CLONE_LIMIT = config_dict['CLONE_LIMIT']
        MEGA_LIMIT = config_dict['MEGA_LIMIT']
        LEECH_LIMIT = config_dict['LEECH_LIMIT']
        ZIP_UNZIP_LIMIT = config_dict['ZIP_UNZIP_LIMIT']
        TOTAL_TASKS_LIMIT = config_dict['TOTAL_TASKS_LIMIT']
        USER_TASKS_LIMIT = config_dict['USER_TASKS_LIMIT']

        torrent_direct = 'No Limit Set' if TORRENT_DIRECT_LIMIT == '' else f'{TORRENT_DIRECT_LIMIT}GB/Link'
        clone_limit = 'No Limit Set' if CLONE_LIMIT == '' else f'{CLONE_LIMIT}GB/Link'
        mega_limit = 'No Limit Set' if MEGA_LIMIT == '' else f'{MEGA_LIMIT}GB/Link'
        leech_limit = 'No Limit Set' if LEECH_LIMIT == '' else f'{LEECH_LIMIT}GB/Link'
        zip_unzip = 'No Limit Set' if ZIP_UNZIP_LIMIT == '' else f'{ZIP_UNZIP_LIMIT}GB/Link'
        total_task = 'No Limit Set' if TOTAL_TASKS_LIMIT == '' else f'{TOTAL_TASKS_LIMIT} Total Tasks/Time'
        user_task = 'No Limit Set' if USER_TASKS_LIMIT == '' else f'{USER_TASKS_LIMIT} Tasks/user'

        if config_dict['EMOJI_THEME']: 
            stats += f'<b>╭─《 ⚠️ BOT LIMITS ⚠️ 》</b>\n'\
                     f'<b>├ 🧲 Torrent/Direct: </b>{torrent_direct}\n'\
                     f'<b>├ 🔐 Zip/Unzip: </b>{zip_unzip}\n'\
                     f'<b>├ 🔷 Leech: </b>{leech_limit}\n'\
                     f'<b>├ ♻️ Clone: </b>{clone_limit}\n'\
                     f'<b>├ 🔰 Mega: </b>{mega_limit}\n'\
                     f'<b>├ 💣 Total Tasks: </b>{total_task}\n'\
                     f'<b>╰ 🔫 User Tasks: </b>{user_task}\n\n'
        else: 
            stats += f'<b>╭─《 ⚠️ BOT LIMITS ⚠️ 》</b>\n'\
                     f'<b>├  Torrent/Direct: </b>{torrent_direct}\n'\
                     f'<b>├  Zip/Unzip: </b>{zip_unzip}\n'\
                     f'<b>├  Leech: </b>{leech_limit}\n'\
                     f'<b>├  Clone: </b>{clone_limit}\n'\
                     f'<b>├  Mega: </b>{mega_limit}\n'\
                     f'<b>├  Total Tasks: </b>{total_task}\n'\
                     f'<b>╰  User Tasks: </b>{user_task}\n\n'

    if PICS:
        sendPhoto(stats, context.bot, update.message, rchoice(PICS))
    else:
        sendMessage(stats, context.bot, update.message)

def start(update, context):
    buttons = ButtonMaker()
    if config_dict['EMOJI_THEME']:
        buttons.buildbutton(f"😎 {config_dict['START_BTN1_NAME']}", f"{config_dict['START_BTN1_URL']}")
        buttons.buildbutton(f"🔥 {config_dict['START_BTN2_NAME']}", f"{START_BTN2_URL}")
    else:
        buttons.buildbutton(f"{config_dict['START_BTN1_NAME']}", f"{config_dict['START_BTN1_URL']}")
        buttons.buildbutton(f"{config_dict['START_BTN2_NAME']}", f"{config_dict['START_BTN2_URL']}")
    reply_markup = buttons.build_menu(2)
    if CustomFilters.authorized_user(update) or CustomFilters.authorized_chat(update):
        start_string = f'''This bot can mirror all your links to Google Drive!
Type /{BotCommands.HelpCommand} to get a list of available commands
'''
        if PICS:
            sendPhoto(start_string, context.bot, update.message, rchoice(PICS), reply_markup)
        else:
            sendMarkup(start_string, context.bot, update.message, reply_markup)
    else:
        text = f"Not Authorized user, deploy your own mirror bot"
        if PICS:
            sendPhoto(text, context.bot, update.message, rchoice(PICS), reply_markup)
        else:
            sendMarkup(text, context.bot, update.message, reply_markup)


def restart(update, context):
    restart_message = sendMessage("Restarting...", context.bot, update.message)
    if Interval:
        Interval[0].cancel()
        Interval.clear()
    if QbInterval:
        QbInterval[0].cancel()
        QbInterval.clear()
    clean_all()
    srun(["pkill", "-9", "-f", "gunicorn|aria2c|qbittorrent-nox|ffmpeg"])
    srun(["python3", "update.py"])
    with open(".restartmsg", "w") as f:
        f.truncate(0)
        f.write(f"{restart_message.chat.id}\n{restart_message.message_id}\n")
    osexecl(executable, executable, "-m", "bot")


def ping(update, context):
    if config_dict['EMOJI_THEME']:
        start_time = int(round(time() * 1000))
        reply = sendMessage("Starting_Ping ⛔", context.bot, update.message)
        end_time = int(round(time() * 1000))
        editMessage(f'{end_time - start_time} ms 🔥', reply)
    else:
        start_time = int(round(time() * 1000))
        reply = sendMessage("Starting_Ping ", context.bot, update.message)
        end_time = int(round(time() * 1000))
        editMessage(f'{end_time - start_time} ms ', reply)

def log(update, context):
    sendLogFile(context.bot, update.message)


help_string = '''
<b>𝔗𝔥𝔢 𝔘𝔩𝔱𝔦𝔪𝔞𝔱𝔢 𝔗𝔢𝔩𝔢𝔤𝔯𝔞𝔪 𝔐ℑ𝔯𝔯𝔬𝔯-𝔏𝔢𝔢𝔠𝔥 𝔅𝔬𝔱 𝔱𝔬 𝔘𝔭𝔩𝔬𝔞𝔡 𝔜𝔬𝔲𝔯 𝔉𝔦𝔩𝔢 & 𝔏𝔦𝔫𝔨 𝔦𝔫 𝔊𝔬𝔬𝔤𝔩𝔢 𝔇𝔯𝔦𝔳𝔢 & 𝔗𝔢𝔩𝔢𝔤𝔯𝔞𝔪 \t<a href='https://t.me/HombaleCinemas'>HombaleCinemas</a></b>
Choose a help category:
'''

help_string_telegraph_user = f'''
<b><u>👤 𝒰𝓈ℯ𝓇 𝒞ℴ𝓂𝓂𝒶𝓃𝒹𝓈</u></b>
<br><br>
• <b>/{BotCommands.HelpCommand}</b>: To get this message
<br><br>
• <b>/{BotCommands.MirrorCommand[0]}</b> [download_url][magnet_link]: Start mirroring to Google Drive. Send <b>/{BotCommands.MirrorCommand[0]}</b> for more help
<br><br>
• <b>/{BotCommands.ZipMirrorCommand[0]}</b> [download_url][magnet_link]: Start mirroring and upload the file/folder compressed with zip extension
<br><br>
• <b>/{BotCommands.UnzipMirrorCommand[0]}</b> [download_url][magnet_link]: Start mirroring and upload the file/folder extracted from any archive extension
<br><br>
• <b>/{BotCommands.QbMirrorCommand[0]}</b> [magnet_link][torrent_file][torrent_file_url]: Start Mirroring using qBittorrent, Use <b>/{BotCommands.QbMirrorCommand[0]} s</b> to select files before downloading
<br><br>
• <b>/{BotCommands.QbZipMirrorCommand[0]}</b> [magnet_link][torrent_file][torrent_file_url]: Start mirroring using qBittorrent and upload the file/folder compressed with zip extension
<br><br>
• <b>/{BotCommands.QbUnzipMirrorCommand[0]}</b> [magnet_link][torrent_file][torrent_file_url]: Start mirroring using qBittorrent and upload the file/folder extracted from any archive extension
<br><br>
• <b>/{BotCommands.LeechCommand[0]}</b> [download_url][magnet_link]: Start leeching to Telegram, Use <b>/{BotCommands.LeechCommand[0]} s</b> to select files before leeching
<br><br>
• <b>/{BotCommands.ZipLeechCommand[0]}</b> [download_url][magnet_link]: Start leeching to Telegram and upload the file/folder compressed with zip extension
<br><br>
• <b>/{BotCommands.UnzipLeechCommand[0]}</b> [download_url][magnet_link][torent_file]: Start leeching to Telegram and upload the file/folder extracted from any archive extension
<br><br>
• <b>/{BotCommands.QbLeechCommand[0]}</b> [magnet_link][torrent_file][torrent_file_url]: Start leeching to Telegram using qBittorrent, Use <b>/{BotCommands.QbLeechCommand[0]} s</b> to select files before leeching
<br><br>
• <b>/{BotCommands.QbZipLeechCommand[0]}</b> [magnet_link][torrent_file][torrent_file_url]: Start leeching to Telegram using qBittorrent and upload the file/folder compressed with zip extension
<br><br>
• <b>/{BotCommands.QbUnzipLeechCommand[0]}</b> [magnet_link][torrent_file][torrent_file_url]: Start leeching to Telegram using qBittorrent and upload the file/folder extracted from any archive extension
<br><br>
• <b>/{BotCommands.CloneCommand[0]}</b> [drive_url][gdtot_url]: Copy file/folder to Google Drive
<br><br>
• <b>/{BotCommands.CountCommand}</b> [drive_url][gdtot_url]: Count file/folder of Google Drive
<br><br>
• <b>/{BotCommands.DeleteCommand}</b> [drive_url]: Delete file/folder from Google Drive (Only Owner & Sudo)
<br><br>
• <b>/{BotCommands.YtdlCommand[0]}</b> [yt-dlp supported link]: Mirror yt-dlp supported link. Send <b>/{BotCommands.YtdlCommand[0]}</b> for more help
<br><br>
• <b>/{BotCommands.YtdlZipCommand[0]}</b> [yt-dlp supported link]: Mirror yt-dlp supported link as zip
<br><br>
• <b>/{BotCommands.YtdlLeechCommand[0]}</b> [yt-dlp supported link]: Leech yt-dlp supported link
<br><br>
• <b>/{BotCommands.YtdlZipLeechCommand[0]}</b> [yt-dlp supported link]: Leech yt-dlp supported link as zip
<br><br>
• <b>/{BotCommands.UserSetCommand[0]}</b>: Users settings
<br><br>
• <b>/{BotCommands.RssListCommand}</b>: List all subscribed rss feed info
<br><br>
• <b>/{BotCommands.RssGetCommand}</b>: [Title] [Number](last N links): Force fetch last N links
<br><br>
• <b>/{BotCommands.RssSubCommand}</b>: [Title] [Rss Link] f: [filter]: Subscribe new rss feed
<br><br>
• <b>/{BotCommands.RssUnSubCommand}</b>: [Title]: Unubscribe rss feed by title
<br><br>
• <b>/{BotCommands.RssSettingsCommand}</b>: Rss Settings
<br><br>
• <b>/{BotCommands.CancelMirror}</b>: Reply to the message by which the download was initiated and that download will be cancelled
<br><br>
• <b>/{BotCommands.CancelAllCommand}</b>: Cancel all downloading tasks
<br><br>
• <b>/{BotCommands.ListCommand}</b> [query]: Search in Google Drive(s)
<br><br>
• <b>/{BotCommands.SearchCommand}</b> [query]: Search for torrents with API
<br>sites: <code>rarbg, 1337x, yts, etzv, tgx, torlock, piratebay, nyaasi, ettv</code><br><br>
• <b>/{BotCommands.StatusCommand}</b>: Shows a status of all the downloads
<br><br>
• <b>/{BotCommands.StatsCommand}</b>: Show Stats of the machine the bot is hosted on
<br><br>
• <b>/{BotCommands.SpeedCommand[0]}</b>: Speedtest of server
<br><br>
• <b>/weebhelp</b>: Okatu helper
'''

help_user = telegraph.create_page(
    title=f"{config_dict['TITLE_NAME']} Help",
    content=help_string_telegraph_user)["path"]

help_string_telegraph_admin = f'''
<b><u>👩‍💻𝒪𝓌𝓃ℯ𝓇 𝒞ℴ𝓂𝓂𝒶𝓃𝒹𝓈</u></b>
<br><br>
• <b>/{BotCommands.PingCommand}</b>: Check how long it takes to Ping the Bot
<br><br>
• <b>/{BotCommands.AuthorizeCommand}</b>: Authorize a chat or a user to use the bot (Can only be invoked by Owner & Sudo of the bot)
<br><br>
• <b>/{BotCommands.UnAuthorizeCommand}</b>: Unauthorize a chat or a user to use the bot (Can only be invoked by Owner & Sudo of the bot)
<br><br>
• <b>/{BotCommands.UsersCommand}</b>: show users settings (Only Owner & Sudo).
<br><br>
• <b>/{BotCommands.AddSudoCommand}</b>: Add sudo user (Only Owner)
<br><br>
• <b>/{BotCommands.RmSudoCommand}</b>: Remove sudo users (Only Owner)
<br><br>
• <b>/{BotCommands.PaidUsersCommand}</b>: Show Paid users (Only Owner & Sudo)
<br><br>
• <b>/{BotCommands.AddPaidCommand}</b>: Authorize Paid users (Only Owner)
<br><br>
• <b>/{BotCommands.RmPaidCommand}</b>: Unauthorize Paid users (Only Owner)
<br><br>
• <b>/{BotCommands.RestartCommand}</b>: Restart and update the bot (Only Owner & Sudo)
<br><br>
• <b>/{BotCommands.LogCommand}</b>: Get a log file of the bot. Handy for getting crash reports
'''

help_admin = telegraph.create_page(
    title=f"{config_dict['TITLE_NAME']} Help",
    content=help_string_telegraph_admin)["path"]


def bot_help(update, context):
    button = ButtonMaker()
    if config_dict['EMOJI_THEME']:
        button.buildbutton("👤 User", f"https://telegra.ph/{help_user}")
        button.buildbutton("🛡️ Admin", f"https://telegra.ph/{help_admin}")
    else:
        button.buildbutton("𝔘𝔰𝔢𝔯", f"https://telegra.ph/{help_user}")
        button.buildbutton("𝔒𝔴𝔫𝔢𝔯", f"https://telegra.ph/{help_admin}")
    sendMarkup(help_string, context.bot, update.message, button.build_menu(2))


if config_dict['SET_BOT_COMMANDS']:
    botcmds = [
        (f'{BotCommands.StartCommand[0]}', 'Start'),
        (f'{BotCommands.MirrorCommand[0]}', 'Mirror'),
        (f'{BotCommands.ZipMirrorCommand[0]}','Mirror and upload as zip'),
        (f'{BotCommands.UnzipMirrorCommand[0]}','Mirror and extract files'),
        (f'{BotCommands.QbMirrorCommand[0]}','Mirror torrent using qBittorrent'),
        (f'{BotCommands.QbZipMirrorCommand[0]}','Mirror torrent and upload as zip using qb'),
        (f'{BotCommands.QbUnzipMirrorCommand[0]}','Mirror torrent and extract files using qb'),
        (f'{BotCommands.YtdlCommand[0]}','Mirror yt-dlp supported link'),
        (f'{BotCommands.YtdlZipCommand[0]}','Mirror yt-dlp supported link as zip'),
        (f'{BotCommands.CloneCommand[0]}','Copy file/folder to Drive'),
        (f'{BotCommands.LeechCommand[0]}','Leech'),
        (f'{BotCommands.ZipLeechCommand[0]}','Leech and upload as zip'),
        (f'{BotCommands.UnzipLeechCommand[0]}','Leech and extract files'),
        (f'{BotCommands.QbLeechCommand[0]}','Leech torrent using qBittorrent'),
        (f'{BotCommands.QbZipLeechCommand[0]}','Leech torrent and upload as zip using qb'),
        (f'{BotCommands.QbUnzipLeechCommand[0]}','Leech torrent and extract using qb'),
        (f'{BotCommands.YtdlLeechCommand[0]}','Leech yt-dlp supported link'),
        (f'{BotCommands.YtdlZipLeechCommand[0]}','Leech yt-dlp supported link as zip'),
        (f'{BotCommands.ScrapeCommand[0]}','Scrape Links from Website'),
        (f'{BotCommands.CountCommand}','Count file/folder of Drive'),
        (f'{BotCommands.DeleteCommand}','Delete file/folder from Drive'),
        (f'{BotCommands.CancelMirror}','Cancel a task'),
        (f'{BotCommands.CancelAllCommand}','Cancel all downloading tasks'),
        (f'{BotCommands.ListCommand}','Search in Drive'),
        (f'{BotCommands.SearchCommand}','Search in Torrent'),
        (f'{BotCommands.UserSetCommand[0]}','Users settings'),
        (f'{BotCommands.BotSetCommand[0]}','BOT settings'),
        (f'{BotCommands.StatusCommand}','Get mirror status message'),
        (f'{BotCommands.SpeedCommand[0]}','Speedtest'),
        (f'{BotCommands.WayBackCommand}','Internet Archive'),
        (f'{BotCommands.MediaInfoCommand[0]}','Get Information of telegram Files'),
        (f'{BotCommands.HashCommand}','Get Hash of telegram Files'),
        (f'{BotCommands.PingCommand}','Ping the bot'),
        (f'{BotCommands.RestartCommand}','Restart the bot'),
        (f'{BotCommands.LogCommand}','Get the bot Log'),
        (f'{BotCommands.HelpCommand}','Get detailed help')
    ]


def main():

    if config_dict['WALLCRAFT_CATEGORY']:
        for page in range(1,20):
            r2 = rget(f"https://wallpaperscraft.com/catalog/{config_dict['WALLCRAFT_CATEGORY']}/1280x720/page{page}")
            soup2 = BeautifulSoup(r2.text, "html.parser")
            x = soup2.select('img[src^="https://images.wallpaperscraft.com/image/single"]')
            for img in x:
              PICS.append((img['src']).replace("300x168", "1280x720"))

    if config_dict['WALLTIP_SEARCH']:
        for page in range(1,3):
            r2 = rget(f"https://www.wallpapertip.com/s/{config_dict['WALLTIP_SEARCH']}/{page}")
            soup2 = BeautifulSoup(r2.text, "html.parser")
            divTag = soup2.select('#flex_grid div.item')
            aTag = [x.find('a') for x in divTag]
            imgsrc = [x.find('img') for x in aTag]
            scrList =  [img['data-original'] for img in imgsrc]
            for o in scrList:
                PICS.append(o)

    if config_dict['WALLFLARE_SEARCH']:
        try:
            for page in range(1,20):
                r2 = rget(f"https://www.wallpaperflare.com/search?wallpaper={config_dict['WALLFLARE_SEARCH']}&width=1280&height=720&page={page}")
                soup2 = BeautifulSoup(r2.text, "html.parser")
                x = soup2.select('img[data-src^="https://c4.wallpaperflare.com/wallpaper"]')  
                for img in x:
                    PICS.append(img['data-src'])
        except Exception as err:
            LOGGER.info(f"WallFlare Error: {err}")

    if config_dict['PIXABAY_API_KEY']:
        try:
            PIXABAY_ENDPOINT = f"https://pixabay.com/api/?key={config_dict['PIXABAY_API_KEY']}&image_type=all&orientation=horizontal&min_width=1280&min_height=720&per_page=200&safesearch=true&editors_choice=true"
            if config_dict['PIXABAY_CATEGORY']: PIXABAY_ENDPOINT += f"&category={config_dict['PIXABAY_CATEGORY']}"
            if config_dict['PIXABAY_SEARCH']: PIXABAY_ENDPOINT += f"&q={q(config_dict['PIXABAY_SEARCH'])}"
            resp = rget(PIXABAY_ENDPOINT)
            jdata = resp.json()
            for x in range(0, 200):
                largeImageURL = jdata['hits'][x]['largeImageURL']
                PICS.append(largeImageURL)
        except Exception as err:
            LOGGER.info(f"Pixabay API Error: {err}")

    if config_dict['SET_BOT_COMMANDS']:
        bot.set_my_commands(botcmds)
    start_cleanup()
    date = now.strftime('%d/%m/%y')
    time = now.strftime('%I:%M:%S %p')
    notifier_dict = False
    if config_dict['INCOMPLETE_TASK_NOTIFIER'] and DATABASE_URL:
        if notifier_dict := DbManger().get_incomplete_tasks():
            for cid, data in notifier_dict.items():
                if ospath.isfile(".restartmsg"):
                    with open(".restartmsg") as f:
                        chat_id, msg_id = map(int, f)
                    msg = f"😎Restarted successfully❗\n"
                    msg += f"📅DATE: {date}\n"
                    msg += f"⌚TIME: {time}\n"
                    msg += f"🌐TIMEZONE: {timez}\n"
                else:
                    msg = f"ℛℯ𝓈𝓉𝒶𝓇𝓉ℯ𝒹 𝓈𝓊𝒸𝒸ℯ𝓈𝓈𝒻𝓊𝓁𝓁𝓎"

                for tag, links in data.items():
                    msg += f"\n{tag}: "
                    for index, link in enumerate(links, start=1):
                        msg += f" <a href='{link}'>{index}</a> |"
                        if len(msg.encode()) > 4000:
                            if 'ℛℯ𝓈𝓉𝒶𝓇𝓉ℯ𝒹 𝓈𝓊𝒸𝒸ℯ𝓈𝓈𝒻𝓊𝓁𝓁𝓎' in msg and cid == chat_id:
                                try:
                                    bot.editMessageText(msg, chat_id, msg_id, parse_mode='HTML', disable_web_page_preview=True)
                                except:
                                    pass
                                osremove(".restartmsg")
                            else:
                                try:
                                    bot.sendMessage(cid, msg, parse_mode='HTML', disable_web_page_preview=True)
                                except Exception as e:
                                    LOGGER.error(e)
                            msg = ''
                if 'ℛℯ𝓈𝓉𝒶𝓇𝓉ℯ𝒹 𝓈𝓊𝒸𝒸ℯ𝓈𝓈𝒻𝓊𝓁𝓁𝓎' in msg and cid == chat_id:
                    try:
                        bot.editMessageText(msg, chat_id, msg_id, parse_mode='HTML', disable_web_page_preview=True)
                    except:
                        pass
                    osremove(".restartmsg")
                else:
                    try:
                        bot.sendMessage(cid, msg, parse_mode='HTML', disable_web_page_preview=True)
                    except Exception as e:
                        LOGGER.error(e)

    if ospath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        try:
            msg = f"ℛℯ𝓈𝓉𝒶𝓇𝓉ℯ𝒹 𝓈𝓊𝒸𝒸ℯ𝓈𝓈𝒻𝓊𝓁𝓁𝓎\n"
            bot.edit_message_text(msg, chat_id, msg_id)
        except:
            pass        
        osremove(".restartmsg")



    start_handler = CommandHandler(BotCommands.StartCommand, start, run_async=True)
    log_handler = CommandHandler(BotCommands.LogCommand, log,
                               filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                               filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    help_handler = CommandHandler(BotCommands.HelpCommand, bot_help,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    stats_handler = CommandHandler(BotCommands.StatsCommand, stats,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)


    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    updater.start_polling(drop_pending_updates=IGNORE_PENDING_REQUESTS)
    LOGGER.info("ℬℴ𝓉 ℛℯ𝓈𝓉𝒶𝓇𝓉ℯ𝒹")
    signal(SIGINT, exit_clean_up)

app.start()
main()

main_loop.run_forever()
