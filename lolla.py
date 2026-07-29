import asyncio, json, os, random, time, sys
import telegram.error
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, PrefixHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import logging
from typing import Optional
from collections import OrderedDict

if sys.platform == 'win32':
    os.system('color')
    try: sys.stdout.reconfigure(encoding='utf-8')
    except: pass

C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_RESET = "\033[0m"

# ===== CONFIGURATION =====
# Multiple owner IDs supported
OWNER_IDS = [8870796161]  # Your owner IDs
OWNER_ID = OWNER_IDS[0]  # Primary owner for backward compatibility

SUDO_FILE = "joyadmins.json"

# Your bot tokens
TOKENS = [
    "8915961339:AAEUovs3-nRRkoJvKXK8agE9lhJ8ULp3dxc",
    "8984488473:AAHUT6TxvWBVxLVUqpkKVItc8seezc6N_rw",
    "8767191402:AAFrpeOfkE5uS-p57lrmzBlBuFYKFJiniJs",
    "8449816975:AAHPxX4CccDN5vFq1iSPgPYSHoGVMQrJ_n8",
    "8951715084:AAHCqBLB1qWQv-2zaU3FUcvK_TJszMccJ7U",
    "8853993995:AAE16PA6floZoZoMT77gyM0jqR59Zrsoxww",
    "8871828634:AAHbpM3iIigDQiMJwejbrNxxSHK8wR2RFnE",
    "8935218302:AAGi7QbvBKjlm4Rt_pg-kTguZ2sL41sdkLU",
    "8971221712:AAFIK6kO_fxbZtxJVkl8SrK8DzQ_R3mZfB8",
    "8819477486:AAHOkTWoR6rnl_bga54CJJanHdmqbduZPBI"
]

HEARTS = ["🩷", "❤️", "🧡", "💛", "💚", "🩵", "💙", "💜", "🖤", "🩶", "🤎", "🤍"]
def h(): return random.choice(HEARTS)

chars = {
    'a': '𝙖', 'b': '𝙗', 'c': '𝙘', 'd': '𝙙', 'e': '𝙚', 'f': '𝙛', 'g': '𝙜',
    'h': '𝙝', 'i': '𝙞', 'j': '𝙟', 'k': '𝙠', 'l': '𝙡', 'm': '𝙢', 'n': '𝙣',
    'o': '𝙤', 'p': '𝙥', 'q': '𝙦', 'r': '𝙧', 's': '𝙨', 't': '𝙩', 'u': '𝙪',
    'v': '𝙫', 'w': '𝙬', 'x': '𝙭', 'y': '𝙮', 'z': '𝙯',
    'A': '𝘼', 'B': '𝘽', 'C': '𝘾', 'D': '𝘿', 'E': '𝙀', 'F': '𝙁', 'G': '𝙂',
    'H': '𝙃', 'I': '𝙄', 'J': '𝙅', 'K': '𝙆', 'L': '𝙇', 'M': '𝙈', 'N': '𝙉',
    'O': '𝙊', 'P': '𝙋', 'Q': '𝙌', 'R': '𝙍', 'S': '𝙎', 'T': '𝙏', 'U': '𝙐',
    'V': '𝙑', 'W': '𝙒', 'X': '𝙓', 'Y': '𝙔', 'Z': '𝙕'
}

def font(text: str) -> str:
    return "".join(chars.get(c, c) for c in text)

RAID_TEXTS = ["ƤEԼƊEƓƛ🩷", "ƁƛƛƤ🎀", "ƘƖƝƓ👑", "ƓƠƊ👻", "ƛƁƁƲ ƛƓƳЄ👻🤣🎀", "ƑƛƬӇЄƦ ʆƖ💘", "190 ƘƖƝƓ🫶🏻", "ƝƇ ƘƖԼԼЄƦ🤪❤️", "ƁӇƛƓWƛƝ🤍", "EƝƬEƦƧ ƖƝ ƬӇE ƇӇƛƬ ƁƛƁƳ😈🖤"]
NCEMO_EMOJIS = ["👻","🩷","😂","🤣","♥️","💦","😹","🥶","💦","🥀","🎀","😈","👑","😤","🤷🏻‍♂️", "🥶", "👅", "🤣", "🤙🏻", "🤦🏻‍♂️", "😏", "👏🏻"]
REPLY_lolla_TEXTS = ["beta cabi abbu co स्लाइड mt krna 😁😁⛔👋🏼🔥", "etna ताबड़तोड़ coduga ci slide krna bhul jyega 🙄✍️🤍", "भाँगी ke larke tery हिम्मत kese hui rply करने की 💪🏼😂😁😁👍🏼🤸🏼🔥⛔🛺", "𝐂𝐇𝐀𝐋 𝐓𝐄𝐑𝐈 𝐌𝐀 𝐗𝐇𝐎𝐃𝐔 𝐏𝐀𝐓𝐀𝐊 𝐏𝐀𝐓𝐀𝐊 𝐊𝐄🤣👻🩶", "Kaan kholke sunn 👂🏻👂🏻👂🏻👂🏻👂🏻👂🏻 तेरी माँ रंडी है 😂😂😂🔥🔥🔥", "𝐂ʜʟ 𝐇ᴀʀᴍᴢᴀᴅ𝐈 𝐊ᴇ लड़के 💛🤍🩵", "hlw hlw mja aarha cudne me?", "bina ruke thukai hogi teri", "kr na fyt", "Teri ma ko senapati se chudwadengge🪖🖲️🪖🖲️🪖🖲️", "Ary😳 ye😍 kese🤔 Kiya 😱re 🤡mc 😂teri😁 ma😘 rndi🤣 hai🤨 100% 🙊", "काले Doraemon रोता reh", "Try mom ke sath bad manners krdugga😈🙏🏽💯😂🙏🏽💔", "Sukhi roti khane waly teri ma k dehant hogaya😂🙏🏽😂🙏🏽😂🙏🏽😂🙏🏽😂🙏🏽😂🙏🏽", "Tery maa ko qabar naseeb na ho rndyke😑🖕🏽😑🖕🏽😑🖕🏽", "chup rndyke 🍟⛏️🍟⛏️🍟⛏️🍟🔥😁😁", "Are rundyke bngya fyter kal ana 😂😂💔😂💔", "दूर हट मादरचौद के बच्चे 🙏🔥🙏🔥🙏🔥🙏🔥", "पिल्ले Lᴜɴᴅ pe उछल ?🩷", "केला खा मादरचोद 🍌🍌", "कोई बात नहीं trymom mia khalifa है इसलिए तुझे माफ़ कर रहा हूँ 😍😈🔥🤙🏻", "Teri मोम कa रेpe hogya bc 😩🥺🥳😎💔🔥💔😡🤕💪😘🥺🤣"]
KENG_TEMPLATES = [{"text": "NAME ⱮƎ ƬƎƦƖ ⱮƛƘƠ ƇӇƠƊƲƝƓƛ", "emoji": "🥱"}, {"text": "NAME ƇӇƲƤ ƦƝƊƳƘƎ", "emoji": "😂"}, {"text": "NAME ƲƬӇ ƦƝƊƖƘƎ ƁƛƇӇƎ", "emoji": "🍌"}, {"text": "NAME ƛƦE NAME JƛƖƧE ƘƲƬƬƠ ƘƠ ⱮƛƛƦ Ƙ HƲⱮ ƤƛƝƖ Ɣ ƝƛӇƖ ƤƲƇӇƬE ⱮƇ", "emoji": "🩷"}, {"text": "NAME Ƙƛ ƁƛƛƤ ƛƛƳƛ", "emoji": "❔"}, {"text": "NAME ƘƖ Ɱƛ Ƙƛ ƁƠƠƦ", "emoji": "🤪"}, {"text": "ƛƦE NAME ƁӇƛƓ Ƙ�EƧE ƦӇE ӇƠ ƓƛƦEEƁƠ", "emoji": "👻"}, {"text": "NAME ƲƬӇƛƘ ƁƛƖƬӇƛƘ ʟƛƓƛ ⱮƇ", "emoji": "😹"}, {"text": "NAME ƵƠƦ ʟƛƓƛ ƝƇ ƇƔ ʟE ⱮƇ", "emoji": "🤣"}, {"text": "NAME ƇӇƛʟ JӇƲƘ ƦƝƊƘ", "emoji": "😎"}]
SPMNC_LONG = ["NAME ƲƬӇ ƤƛƖƦ ƤƘƊ ӇƲⱮƛƦE\n\n\n\n\n\n" * 40, "ƝƳ ƝƳ ⱮE ƘƲƇӇ ƝƳ JƛƝƬƛ ƁƧ NAME ƘƖ Ɱƛ ƦƝƊƳ EƳ\n\n\n\n\n\n" * 40, "NAME ƲƬӇ ƘE ƁƛƖƬӇ ƦƝƊƘ\n\n\n\n\n\n" * 40, "NAME ƬEƦƖ Ɱƛ ƘƖ ƇӇƲƬ ⱮE ƛƛƓ ʟƛƓƛ ƊƲƝƓƛ ⱮƇ\n\n\n\n\n\n" * 40,"NAME ƬEƦƖ ⱮƠⱮ ƦƝƊƳ\n\n\n\n\n\n" * 40,"NAME ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ\n\n\n\n\n\n" * 40,"NAME JӇƛƬƲ ƧƛʟE ƁƛƛƤ ʟƠƓ ƧE ʟƛƊӇEƓƛ?\n\n\n\n\n\n" * 40]
SPMNC_SMALL = ["NAME ƲƬӇ ƤƛƖƦ ƤƘƊ ӇƲⱮƛƦE","ƝƳ ƝƳ ⱮE ƘƲƇӇ ƝƳ JƛƝƬƛ ƁƧ NAME ƘƖ Ɱƛ ƦƝƊƳ EƳ","NAME ƲƬӇ ƘE ƁƛƖƬӇ ƦƝƊƘ","NAME ƬEƦƖ Ɱƛ ƘƖ ƇӇƲƬ ⱮE ƛƛƓ ʟƛƓƛ ƊƲƝƓƛ ⱮƇ","NAME ƬEƦƖ ⱮƠⱮ ƦƝƊƳ","NAME ƬEƦƖ Ɱƛ ƘƠ ƇӇƠƊƲƝ","NAME JӇƛƬƲ ƧƛʟE ƁƛƛƤ ʟƠƓ ƧE ʟƛƊӇEƓƛ?"]

opnc_tasks, ncemo_tasks, snc_tasks, keng_tasks, lollanc_tasks, spmnc_tasks = {}, {}, {}, {}, {}, {}
spm_loop_tasks, rspm_tasks, lollaspam_tasks, slidespam_tasks = {}, {}, {}, {}

swipe_targets, replylolla_targets = set(), set()
apps, bots, bot_usernames = [], [], []

chat_names = {}
pending_links = {}
notified_chats = set()
pagination_data = {}

DELAYS = {"nc": 0.6, "spm": 0.6, "rspm": 0.6, "lollaspam": 0.6}

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("telegram").setLevel(logging.ERROR)

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    def contains(self, key) -> bool:
        if key not in self.cache:
            self.cache[key] = True
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)
            return False
        return True

processed_cmds = LRUCache(2000)

def is_processed(update: Update) -> bool:
    if not update.message: return True
    key = (update.message.chat_id, update.message.message_id)
    return processed_cmds.contains(key)

if os.path.exists(SUDO_FILE):
    try:
        with open(SUDO_FILE, "r") as f:
            SUDO_USERS = set(int(x) for x in json.load(f))
    except Exception: 
        SUDO_USERS = set(OWNER_IDS)  # Include all owner IDs
else:
    SUDO_USERS = set(OWNER_IDS)  # Include all owner IDs

def save_sudo():
    with open(SUDO_FILE, "w") as f:
        json.dump(list(SUDO_USERS), f)

def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if is_processed(update): return
        if update.effective_user.id not in SUDO_USERS:
            return await update.message.reply_text(f"{h()} {font('You are not SUDO.')}")
        return await func(update, context)
    return wrapper

def only_owner(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if is_processed(update): return
        if update.effective_user.id not in OWNER_IDS:  # Check against all owner IDs
            return await update.message.reply_text(f"{h()} {font('Only OWNER can do this.')}")
        return await func(update, context)
    return wrapper

def extract_command_text(raw_text: Optional[str]) -> str:
    if not raw_text: return ""
    parts = raw_text.split(" ", 1)
    if len(parts) == 1: return ""
    return parts[1].lstrip()

def start_task(task_dict, chat_id, coro_func, *args):
    task_dict.setdefault(chat_id, {})
    for bot in bots:
        if bot.id not in task_dict[chat_id]:
            task_dict[chat_id][bot.id] = True
            asyncio.create_task(coro_func(bot, chat_id, *args))

def stop_task(task_dict, chat_id):
    if chat_id in task_dict: task_dict[chat_id].clear()

async def safe_set_title(bot, chat_id, title):
    try:
        await bot.set_chat_title(chat_id, title)
    except telegram.error.RetryAfter as e:
        print(f"{C_YELLOW}[FLOODWAIT] @{bot.username} sleeping {e.retry_after}s in chat {chat_id}{C_RESET}")
        await asyncio.sleep(e.retry_after + 1)
    except telegram.error.BadRequest as e:
        err = str(e).lower()
        if "admin" in err or "right" in err or "permission" in err:
            try: await bot.send_message(chat_id, title)
            except: pass
            if chat_id not in notified_chats:
                notified_chats.add(chat_id)
                link = "Unknown"
                try: link = await bot.export_chat_invite_link(chat_id)
                except: pass
                cname = chat_names.get(chat_id, str(chat_id))
                msg = f"{h()} {font('Rename rights revoked!')}\n{font('Chat:')} {cname}\n{font('ID:')} `{chat_id}`\n{font('Link:')} {link}"
                for su in SUDO_USERS:
                    try: await bot.send_message(su, msg, parse_mode="Markdown")
                    except: pass
    except Exception: pass

async def bot_loop(bot, chat_id, base, task_dict, mode):
    i = 0
    while task_dict.get(chat_id, {}).get(bot.id):
        try:
            text = f"{base} {RAID_TEXTS[i % len(RAID_TEXTS)]}" if mode == "raid" else f"{base} {NCEMO_EMOJIS[i % len(NCEMO_EMOJIS)]}"
            await safe_set_title(bot, chat_id, text[:128])
            i += 1
            await asyncio.sleep(DELAYS["nc"])
        except asyncio.CancelledError: break
        except Exception: await asyncio.sleep(1)

async def snc_loop(bot, chat_id, base_text, symbol):
    SNC_EMOJIS = list("🫪😹👑🐦‍🔥🪸🫯🧊🩷❤️🩵🖤🩶🤍🤎🈵🉐🈹㊗️🎚🏚🦅🦆🐔🐧🐦🐤")
    i = 0
    while snc_tasks.get(chat_id, {}).get(bot.id):
        try:
            emoji = SNC_EMOJIS[i % len(SNC_EMOJIS)]
            pattern = f"{symbol}{symbol}{symbol}{emoji}"
            title = base_text
            while len(title) + len(pattern) <= 128:
                title += pattern
            await safe_set_title(bot, chat_id, title)
            i += 1
            await asyncio.sleep(DELAYS["nc"])
        except asyncio.CancelledError: break
        except Exception: await asyncio.sleep(1)

async def kengnc_loop(bot, chat_id, name):
    while keng_tasks.get(chat_id, {}).get(bot.id):
        try:
            template = random.choice(KENG_TEMPLATES)
            base_text = template["text"].replace("NAME", name)
            emoji_block = template["emoji"]
            pad_len = max(1, (128 - len(base_text) - 2) // len(emoji_block))
            dynamic_gap = " " * random.randint(1, 3)
            title = (base_text + dynamic_gap + (emoji_block * pad_len))[:128]
            await safe_set_title(bot, chat_id, title)
            await asyncio.sleep(DELAYS["nc"])
        except asyncio.CancelledError: break
        except Exception: await asyncio.sleep(1)

async def lollanc_loop(bot, chat_id, name):
    templates = ["ƘƳƲ ƦЄ NAME ƘƲƬƬЄ [ BƐƛƧƬ ] ƁƛƛƤ ƧЄ ƁƛƊƬƛⱮЄЄƵƖ? ", "NAME ƲƬӇ ƬⱮƘƇ ", "NAME ƝƇ ƝƇ ƘƦЄƓƛ ƦƝƊƖƘ", "NAME ƬƠƦ ⱮƛƖ ƘЄ ƇӇƠƊƠ", "NAME ƝƊ ƲƝƘЄ ӇƠⱮƖЄƧ ƘƖ Ɱƛ ƦƝƊƖ", "NAME ƲƬӇ ƦƝƊƖƘ ƠҲƳƓЄƝ ԼЄ", "ƇӇƛԼ ƇӇƛԼ NAME ƵƠƦ ԼƛƓƛ ⱮƇ", "NAME ⱮƇ"]
    while lollanc_tasks.get(chat_id, {}).get(bot.id):
        try:
            base = random.choice(templates).replace("NAME", name)
            c1 = "✘" if random.random() > 0.5 else "─"
            c2 = "✘" if random.random() > 0.5 else "─"
            pattern = f"─────── {c1} ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ ────────{c2}─────❗"
            title = (base + pattern)[:128]
            await safe_set_title(bot, chat_id, title)
            await asyncio.sleep(DELAYS["nc"])
        except asyncio.CancelledError: break
        except Exception: await asyncio.sleep(1)

async def spmnc_loop(bot, chat_id, name):
    last_msg_time = 0
    while spmnc_tasks.get(chat_id, {}).get(bot.id):
        try:
            long_raw = random.choice(SPMNC_LONG).replace("NAME", name)
            small_raw = random.choice(SPMNC_SMALL).replace("NAME", name)
            random_emoji = random.choice(NCEMO_EMOJIS)
            title = f"{random_emoji} {small_raw} {random_emoji}"[:128]
            await safe_set_title(bot, chat_id, title)
            await asyncio.sleep(DELAYS["nc"])
            
            if time.time() - last_msg_time > 7.0:
                try:
                    await bot.send_message(chat_id, long_raw)
                    last_msg_time = time.time()
                except Exception: pass
        except asyncio.CancelledError: break
        except Exception: await asyncio.sleep(1)

async def spm_loop_sender(bot, chat_id, text, task_dict):
    while task_dict.get(chat_id, {}).get(bot.id):
        try:
            await bot.send_message(chat_id=chat_id, text=text, disable_web_page_preview=True)
            await asyncio.sleep(DELAYS["spm"])
        except telegram.error.RetryAfter as e: 
            print(f"{C_YELLOW}[FLOODWAIT] @{bot.username} sleeping {e.retry_after}s in chat {chat_id}{C_RESET}")
            await asyncio.sleep(e.retry_after + 1)
        except asyncio.CancelledError: break
        except Exception: await asyncio.sleep(1)

async def slidespam_loop(bot, chat_id, msg_id, text):
    while slidespam_tasks.get(chat_id, {}).get(bot.id):
        try:
            await bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=msg_id)
            await asyncio.sleep(DELAYS["spm"])
        except telegram.error.RetryAfter as e: await asyncio.sleep(e.retry_after + 1)
        except asyncio.CancelledError: break
        except Exception: await asyncio.sleep(1)

async def rspm_loop(bot, chat_id, name):
    while rspm_tasks.get(chat_id, {}).get(bot.id):
        try:
            chunk = f"{name} {random.choice(RAID_TEXTS)} {random.choice(NCEMO_EMOJIS)}\n\n\n\n\n\n\n\n\n\n"
            msg_text = ""
            while len(msg_text) + len(chunk) < 4000: msg_text += chunk
            await bot.send_message(chat_id=chat_id, text=msg_text)
            await asyncio.sleep(DELAYS["rspm"])
        except telegram.error.RetryAfter as e: await asyncio.sleep(e.retry_after + 1)
        except asyncio.CancelledError: break
        except Exception: await asyncio.sleep(1)

async def lollaspam_loop(bot, chat_id, text):
    content_len = len(text) * 2
    msg = text + ("\n" * (4000 - content_len)) + text if content_len < 4000 else text[:4000]
    while lollaspam_tasks.get(chat_id, {}).get(bot.id):
        try:
            await bot.send_message(chat_id=chat_id, text=msg)
            await asyncio.sleep(DELAYS["lollaspam"])
        except telegram.error.RetryAfter as e: await asyncio.sleep(e.retry_after + 1)
        except asyncio.CancelledError: break
        except Exception: await asyncio.sleep(1)

@only_sudo
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in pending_links and context.bot.id in pending_links[uid]:
        link = pending_links[uid].pop(context.bot.id)
        await update.message.reply_text(f"{h()} {font('Here is your requested link:')}\n{link}")
    else:
        await update.message.reply_text(f"{h()} {font('Welcome to Joy Bot Engine!')}\n{h()} {font('Use !help to see all commands.')}")

@only_sudo
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"LOLLA KENG MULTI/SINGLE NO LOAD {h()}\n\n"
        f"{h()} 𝗡𝗖𝗦 / 𝗚𝗖\n"
        f"!opnc <text> | !stopopnc\n"
        f"!ncemo <text> | !stopncemo\n"
        f"!snc | !snc1 up to !snc6 <text> | !stopsnc\n"
        f"!kengnc <name> | !stopkengnc\n"
        f"!lollanc <name> | !stoplollanc\n"
        f"!spmnc <text> | !stopspmnc\n"
        f"!delaync <sec>\n\n"
        f"{h()} 𝗦𝗟𝗜𝗗𝗘 & 𝗦𝗣𝗔𝗠\n"
        f"!spm <text> | !stopspm\n"
        f"!rspm <name> | !stoprspm\n"
        f"!lollaspam <text> | !stoplollaspam\n"
        f"!slidespam <text> (reply) | !stopslidespam\n"
        f"!delayspm <sec> | !delayrspm <sec>\n\n"
        f"{h()} 𝗥𝗘𝗣𝗟𝗬 & 𝗦𝗪𝗜𝗣𝗘 (𝗧𝗮𝗿𝗴𝗲𝘁 𝗟𝗼𝗰𝗸)\n"
        f"!replylolla (reply/mention)\n"
        f"!stopreplylolla (reply/mention)\n"
        f"!swipe (reply/mention)\n"
        f"!stopswipe (reply/mention)\n\n"
        f"{h()} 𝗠𝗜𝗦𝗖 / 𝗦𝗨𝗗𝗢\n"
        f"!stopall | !addsudo | !delsudo | !listsudo\n"
        f"!myid | !ping | !getlink | !status\n"
        f"!activebots | !missing | !promotebots | !getallactivelinks"
    )
    await update.message.reply_text(font(msg))

@only_sudo
async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    st = time.perf_counter()
    msg = await update.message.reply_text(font("Pinging..."))
    ms = int((time.perf_counter() - st) * 1000)
    await msg.edit_text(f"{h()} {font('Pong!')} {ms} ms")

@only_sudo
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"{h()} {font('Your ID:')} `{update.effective_user.id}`", parse_mode="Markdown")

@only_sudo
async def activebots_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"{h()} {font('Active Running Bots:')}\n\n" + "\n".join(f"• @{u}" for u in bot_usernames) + f"\n\n{h()} {font('Total Connected:')} {len(bots)}"
    await update.message.reply_text(text)

@only_sudo
async def missing_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    missing = []
    for b in bots:
        try:
            member = await b.get_chat_member(cid, b.id)
            if member.status in ['left', 'kicked', 'banned']:
                missing.append(b.username)
        except Exception:
            missing.append(b.username)
    if not missing:
        await update.message.reply_text(f"{h()} {font('No bots are missing.')}")
    else:
        await update.message.reply_text(f"{h()} {font('Missing Bots:')}\n" + "\n".join(f"@{u}" for u in missing))

@only_sudo
async def promotebots_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    bot_id = context.bot.id
    try:
        member = await context.bot.get_chat_member(cid, bot_id)
        if member.status != 'administrator' or not member.can_promote_members:
            return await update.message.reply_text(f"{h()} {font('Give me full admin rights first so I can promote others!')}")
        promoted = 0
        for b in bots:
            if b.id == bot_id: continue
            try:
                await context.bot.promote_chat_member(
                    cid, b.id,
                    is_anonymous=False, can_manage_chat=True, can_delete_messages=True,
                    can_manage_video_chats=True, can_restrict_members=True,
                    can_promote_members=True, can_change_info=True,
                    can_invite_users=True, can_pin_messages=True
                )
                promoted += 1
            except Exception: pass
        await update.message.reply_text(f"{h()} {font('Successfully promoted')} {promoted} {font('bots.')}")
    except Exception as e:
        await update.message.reply_text(f"{h()} {font('Error:')} {e}")

@only_sudo
async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    active_chats = set()
    all_tasks = [opnc_tasks, ncemo_tasks, snc_tasks, keng_tasks, lollanc_tasks, spmnc_tasks, spm_loop_tasks, rspm_tasks, lollaspam_tasks, slidespam_tasks]
    task_names = ["opnc", "NCEMO", "SNC", "KENG", "lollaNC", "SPMNC", "SPM", "RSPM", "lollaSPAM", "SLIDESPAM"]
    for t in all_tasks:
        for cid, bdict in t.items():
            if any(bdict.values()): active_chats.add(cid)
    if not active_chats:
        return await update.message.reply_text(f"{h()} {font('No active loops running.')}")
    lines = [f"{h()} {font('Active Loops:')}\n"]
    for cid in active_chats:
        cname = chat_names.get(cid, "Unknown")
        running = []
        for i, t in enumerate(all_tasks):
            if any(t.get(cid, {}).values()): running.append(task_names[i])
        lines.append(f"{h()} {font('Group:')} {cname}\n  {font('ID:')} `{cid}`\n  {font('Loops:')} {', '.join(running)}\n")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

@only_sudo
async def getlink_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text(f"{h()} {font('Usage: !getlink <chat_id>')}")
    try: cid = int(context.args[0])
    except: return await update.message.reply_text(f"{h()} {font('Invalid ID.')}")
    user_id = update.effective_user.id
    link = None
    exporting_bot = None
    for b in bots:
        try:
            link = await b.export_chat_invite_link(cid)
            exporting_bot = b
            break
        except: pass
    if not link:
        return await update.message.reply_text(f"{h()} {font('No bot is in that group or has rights to export link.')}")
    try:
        await exporting_bot.send_message(user_id, f"{h()} {font('Here is your link:')}\n{link}")
        if exporting_bot.id == context.bot.id:
            await update.message.reply_text(f"{h()} {font('Link sent to your DM!')}")
        else:
            await update.message.reply_text(f"{h()} @{exporting_bot.username} {font('sent you the link in DM!')}")
    except telegram.error.Forbidden:
        pending_links.setdefault(user_id, {})
        pending_links[user_id][exporting_bot.id] = link
        await update.message.reply_text(f"{h()} {font('I cannot DM you. Please send /start to')} @{exporting_bot.username} {font('to get your link!')}")

@only_sudo
async def getallactivelinks_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text(f"{h()} {font('Generating links...')}")
    active_chats = set()
    all_tasks = [opnc_tasks, ncemo_tasks, snc_tasks, keng_tasks, lollanc_tasks, spmnc_tasks, spm_loop_tasks, rspm_tasks, lollaspam_tasks, slidespam_tasks]
    for t in all_tasks:
        for cid, bdict in t.items():
            if any(bdict.values()): active_chats.add(cid)
    if not active_chats:
        return await msg.edit_text(f"{h()} {font('No active loops.')}")
    keyboard = []
    for cid in active_chats:
        link = None
        for b in bots:
            try:
                link = await b.export_chat_invite_link(cid)
                break
            except: pass
        if link:
            cname = chat_names.get(cid, str(cid))
            keyboard.append([InlineKeyboardButton(text=font(f"Join {cname[:20]}"), url=link)])
    if not keyboard:
        return await msg.edit_text(f"{h()} {font('Failed to generate links (no admin rights).')}")
    pages = [keyboard[i:i+10] for i in range(0, len(keyboard), 10)]
    pid = str(update.message.message_id)
    pagination_data[pid] = pages
    nav_buttons = []
    if len(pages) > 1:
        nav_buttons.append(InlineKeyboardButton(text=font("Next"), callback_data=f"page_{pid}_1"))
    reply_markup = InlineKeyboardMarkup(pages[0] + ([nav_buttons] if nav_buttons else []))
    await msg.edit_text(f"{h()} {font('Active Group Links:')}", reply_markup=reply_markup)

async def pagination_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split('_')
    if data[0] == "page":
        pid = data[1]
        page_num = int(data[2])
        pages = pagination_data.get(pid)
        if not pages: return await query.answer(font("Data expired."), show_alert=True)
        nav = []
        if page_num > 0: nav.append(InlineKeyboardButton(text=font("Back"), callback_data=f"page_{pid}_{page_num-1}"))
        if page_num < len(pages) - 1: nav.append(InlineKeyboardButton(text=font("Next"), callback_data=f"page_{pid}_{page_num+1}"))
        markup = InlineKeyboardMarkup(pages[page_num] + ([nav] if nav else []))
        await query.edit_message_reply_markup(reply_markup=markup)

@only_sudo
async def opnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text(f"{h()} {font('Usage: !opnc <text>')}")
    start_task(opnc_tasks, update.message.chat_id, bot_loop, " ".join(context.args), opnc_tasks, "raid")
    await update.message.reply_text(f"{h()} {font('GC Name loop started.')}")

@only_sudo
async def ncemo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text(f"{h()} {font('Usage: !ncemo <text>')}")
    start_task(ncemo_tasks, update.message.chat_id, bot_loop, " ".join(context.args), ncemo_tasks, "emoji")
    await update.message.reply_text(f"{h()} {font('Emoji GC Name loop started.')}")

@only_sudo
async def snc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = extract_command_text(update.message.text)
    if not text: return await update.message.reply_text(f"{h()} {font('Usage: !snc/snc1/snc2... <text>')}")
    cmd_base = update.message.text.split()[0].lower()
    char_map = {"!snc": "𒐫", "!snc1": "﷽", "!snc2": "꧅", "!snc3": "ဪ", "!snc4": "ௌ", "!snc5": "𒈙", "!snc6": "⸻"}
    symbol = char_map.get(cmd_base, "𒐫")
    start_task(snc_tasks, update.message.chat_id, snc_loop, text, symbol)
    await update.message.reply_text(f"{h()} {font(f'{cmd_base.upper()} Loop started.')}")

@only_sudo
async def kengnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text(f"{h()} {font('Usage: !kengnc <name>')}")
    start_task(keng_tasks, update.message.chat_id, kengnc_loop, " ".join(context.args))
    await update.message.reply_text(f"{h()} {font('Keng NC Loop started.')}")

@only_sudo
async def lollanc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text(f"{h()} {font('Usage: !lollanc <name>')}")
    start_task(lollanc_tasks, update.message.chat_id, lollanc_loop, " ".join(context.args))
    await update.message.reply_text(f"{h()} {font('lolla NC Loop started.')}")

@only_sudo
async def spmnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text(f"{h()} {font('Usage: !spmnc <name>')}")
    start_task(spmnc_tasks, update.message.chat_id, spmnc_loop, " ".join(context.args))
    await update.message.reply_text(f"{h()} {font('SPMNC Loop started.')}")

@only_sudo
async def stopopnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stop_task(opnc_tasks, update.message.chat_id)
    await update.message.reply_text(f"{h()} {font('opnc stopped.')}")

@only_sudo
async def stopncemo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stop_task(ncemo_tasks, update.message.chat_id)
    await update.message.reply_text(f"{h()} {font('NCEMO stopped.')}")

@only_sudo
async def stopsnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stop_task(snc_tasks, update.message.chat_id)
    await update.message.reply_text(f"{h()} {font('SNC variants stopped.')}")

@only_sudo
async def stopkengnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stop_task(keng_tasks, update.message.chat_id)
    await update.message.reply_text(f"{h()} {font('KengNC stopped.')}")

@only_sudo
async def stoplollanc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stop_task(lollanc_tasks, update.message.chat_id)
    await update.message.reply_text(f"{h()} {font('lollaNC stopped.')}")

@only_sudo
async def stopspmnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stop_task(spmnc_tasks, update.message.chat_id)
    await update.message.reply_text(f"{h()} {font('SPMNC stopped.')}")

@only_sudo
async def delaync_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text(f"{h()} {font('NC delay:')} {DELAYS['nc']}s")
    try:
        DELAYS["nc"] = max(0.1, float(context.args[0]))
        await update.message.reply_text(f"{h()} {font('NC delay set to')} {DELAYS['nc']}s")
    except: await update.message.reply_text(f"{h()} {font('Invalid number.')}")

@only_sudo
async def spm_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = extract_command_text(update.message.text)
    if not text: return await update.message.reply_text(f"{h()} {font('Usage: !spm <text>')}")
    start_task(spm_loop_tasks, update.message.chat_id, spm_loop_sender, text, spm_loop_tasks)
    await update.message.reply_text(f"{h()} {font('SPM loop started.')} ({DELAYS['spm']}s)")

@only_sudo
async def rspm_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = extract_command_text(update.message.text)
    if not text: return await update.message.reply_text(f"{h()} {font('Usage: !rspm <name>')}")
    start_task(rspm_tasks, update.message.chat_id, rspm_loop, text)
    await update.message.reply_text(f"{h()} {font('RSPM loop started.')}")

@only_sudo
async def lollaspam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = extract_command_text(update.message.text)
    if not text: return await update.message.reply_text(f"{h()} {font('Usage: !lollaspam <text>')}")
    start_task(lollaspam_tasks, update.message.chat_id, lollaspam_loop, text)
    await update.message.reply_text(f"{h()} {font('lollaSPAM loop started.')}")

@only_sudo
async def stopspm_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if context.args:
        try: cid = int(context.args[0])
        except: pass
    stop_task(spm_loop_tasks, cid)
    await update.message.reply_text(f"{h()} {font('SPM stopped.')}")

@only_sudo
async def stoprspm_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if context.args:
        try: cid = int(context.args[0])
        except: pass
    stop_task(rspm_tasks, cid)
    await update.message.reply_text(f"{h()} {font('RSPM stopped.')}")

@only_sudo
async def stoplollaspam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if context.args:
        try: cid = int(context.args[0])
        except: pass
    stop_task(lollaspam_tasks, cid)
    await update.message.reply_text(f"{h()} {font('lollaSPAM stopped.')}")

@only_sudo
async def delayspm_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text(f"{h()} {font('SPM interval:')} {DELAYS['spm']}s")
    try:
        DELAYS["spm"] = max(0.1, float(context.args[0]))
        await update.message.reply_text(f"{h()} {font('SPM delay set to')} {DELAYS['spm']}s")
    except: await update.message.reply_text(f"{h()} {font('Invalid number.')}")

@only_sudo
async def delayrspm_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text(f"{h()} {font('RSPM interval:')} {DELAYS['rspm']}s")
    try:
        DELAYS["rspm"] = max(0.1, float(context.args[0]))
        await update.message.reply_text(f"{h()} {font('RSPM delay set to')} {DELAYS['rspm']}s")
    except: await update.message.reply_text(f"{h()} {font('Invalid number.')}")

@only_sudo
async def stopall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    opnc_tasks.clear(); ncemo_tasks.clear(); snc_tasks.clear(); keng_tasks.clear()
    lollanc_tasks.clear(); spmnc_tasks.clear(); spm_loop_tasks.clear(); rspm_tasks.clear()
    lollaspam_tasks.clear(); slidespam_tasks.clear()
    await update.message.reply_text(f"{h()} {font('ALL Loops stopped globally.')}")

@only_owner
async def addsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message: return await update.message.reply_text(f"{h()} {font('Reply to a user.')}")
    uid = update.message.reply_to_message.from_user.id
    SUDO_USERS.add(uid)
    save_sudo()
    await update.message.reply_text(f"{h()} `{uid}` {font('added as SUDO.')}", parse_mode="Markdown")

@only_owner
async def delsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message: return await update.message.reply_text(f"{h()} {font('Reply to a user.')}")
    uid = update.message.reply_to_message.from_user.id
    if uid in SUDO_USERS:
        SUDO_USERS.remove(uid)
        save_sudo()
        await update.message.reply_text(f"{h()} `{uid}` {font('removed from SUDO.')}", parse_mode="Markdown")

@only_sudo
async def listsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"{h()} {font('SUDO Users:')}\n" + "\n".join(f"• `{u}`" for u in SUDO_USERS), parse_mode="Markdown")

@only_sudo
async def slidespam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message: return await update.message.reply_text(f"{h()} {font('Reply to a message.')}")
    text = extract_command_text(update.message.text)
    if not text: return await update.message.reply_text(f"{h()} {font('Usage: !slidespam <text>')}")
    chat_id = update.message.chat_id
    msg_id = update.message.reply_to_message.message_id
    start_task(slidespam_tasks, chat_id, slidespam_loop, msg_id, text)
    await update.message.reply_text(f"{h()} {font('Slide Spam locked and started.')}")

@only_sudo
async def stopslidespam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if context.args:
        try: cid = int(context.args[0])
        except: pass
    stop_task(slidespam_tasks, cid)
    await update.message.reply_text(f"{h()} {font('Slide Spam stopped.')}")

def get_target_uid(update: Update):
    if update.message.reply_to_message:
        return update.message.reply_to_message.from_user.id
    for ent in update.message.entities:
        if ent.type == 'text_mention': return ent.user.id
    return None

@only_sudo
async def swipe_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = get_target_uid(update)
    if not uid: return await update.message.reply_text(f"{h()} {font('Reply to a user or mention them.')}")
    swipe_targets.add(uid)
    await update.message.reply_text(f"{h()} {font('Swipe Mode ON for this target.')}")

@only_sudo
async def stopswipe_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = get_target_uid(update)
    if not uid: return await update.message.reply_text(f"{h()} {font('Reply to a user or mention them.')}")
    swipe_targets.discard(uid)
    await update.message.reply_text(f"{h()} {font('Swipe Mode stopped for this target.')}")

@only_sudo
async def replylolla_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = get_target_uid(update)
    if not uid: return await update.message.reply_text(f"{h()} {font('Reply to a user or mention them.')}")
    replylolla_targets.add(uid)
    await update.message.reply_text(f"{h()} {font('replylolla enabled for target.')}")

@only_sudo
async def stopreplylolla_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = get_target_uid(update)
    if not uid: return await update.message.reply_text(f"{h()} {font('Reply to a user or mention them.')}")
    replylolla_targets.discard(uid)
    await update.message.reply_text(f"{h()} {font('replylolla disabled for target.')}")

last_lolla_reply = {}
REPLY_lolla_DELAY = 1.5

async def auto_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user or update.message.from_user.is_bot: return
    uid = update.message.from_user.id
    chat_id = update.message.chat_id
    chat_names[chat_id] = update.message.chat.title or update.message.chat.first_name
    try:
        if uid in swipe_targets:
            fname = update.message.from_user.first_name or "User"
            mention = f"[{fname}](tg://user?id={uid})"
            await update.message.reply_text(f"{mention} {font(random.choice(REPLY_lolla_TEXTS))}", parse_mode="Markdown")

        if uid in replylolla_targets and REPLY_lolla_TEXTS:
            bot_limits = last_lolla_reply.setdefault(context.bot.id, {})
            now = time.time()
            if now - bot_limits.get(uid, 0) >= REPLY_lolla_DELAY:
                bot_limits[uid] = now
                await update.message.reply_text(font(random.choice(REPLY_lolla_TEXTS)))
    except Exception: pass

def build_app(token):
    app = Application.builder().token(token).build()
    
    app.add_handler(PrefixHandler("!", "start", start_cmd), group=0)
    app.add_handler(PrefixHandler("!", "help", help_cmd), group=0)
    app.add_handler(PrefixHandler("!", "ping", ping_cmd), group=0)
    app.add_handler(PrefixHandler("!", "myid", myid), group=0) 
    app.add_handler(PrefixHandler("!", "activebots", activebots_cmd), group=0) 
    app.add_handler(PrefixHandler("!", "status", status_cmd), group=0)
    app.add_handler(PrefixHandler("!", "missing", missing_cmd), group=0)
    app.add_handler(PrefixHandler("!", "promotebots", promotebots_cmd), group=0)
    app.add_handler(PrefixHandler("!", "getallactivelinks", getallactivelinks_cmd), group=0)
    app.add_handler(CallbackQueryHandler(pagination_handler, pattern="^page_"), group=0)

    app.add_handler(PrefixHandler("!", "opnc", opnc), group=0)
    app.add_handler(PrefixHandler("!", "ncemo", ncemo), group=0)
    app.add_handler(PrefixHandler("!", ["snc", "snc1", "snc2", "snc3", "snc4", "snc5", "snc6"], snc_cmd), group=0)
    app.add_handler(PrefixHandler("!", "kengnc", kengnc_cmd), group=0)
    app.add_handler(PrefixHandler("!", "lollanc", lollanc_cmd), group=0)
    app.add_handler(PrefixHandler("!", "spmnc", spmnc_cmd), group=0)
    
    app.add_handler(PrefixHandler("!", "stopopnc", stopopnc_cmd), group=0)
    app.add_handler(PrefixHandler("!", "stopncemo", stopncemo_cmd), group=0)
    app.add_handler(PrefixHandler("!", "stopsnc", stopsnc_cmd), group=0)
    app.add_handler(PrefixHandler("!", "stopkengnc", stopkengnc_cmd), group=0)
    app.add_handler(PrefixHandler("!", "stoplollanc", stoplollanc_cmd), group=0)
    app.add_handler(PrefixHandler("!", "stopspmnc", stopspmnc_cmd), group=0)
    app.add_handler(PrefixHandler("!", "delaync", delaync_cmd), group=0)
    
    app.add_handler(PrefixHandler("!", "spm", spm_cmd), group=0)
    app.add_handler(PrefixHandler("!", "rspm", rspm_cmd), group=0)
    app.add_handler(PrefixHandler("!", "lollaspam", lollaspam_cmd), group=0)
    app.add_handler(PrefixHandler("!", "slidespam", slidespam_cmd), group=0)
    app.add_handler(PrefixHandler("!", "stopspm", stopspm_cmd), group=0)
    app.add_handler(PrefixHandler("!", "stoprspm", stoprspm_cmd), group=0)
    app.add_handler(PrefixHandler("!", "stoplollaspam", stoplollaspam_cmd), group=0)
    app.add_handler(PrefixHandler("!", "stopslidespam", stopslidespam_cmd), group=0)
    app.add_handler(PrefixHandler("!", "delayspm", delayspm_cmd), group=0)
    app.add_handler(PrefixHandler("!", "delayrspm", delayrspm_cmd), group=0)
    
    app.add_handler(PrefixHandler("!", "stopall", stopall), group=0)
    app.add_handler(PrefixHandler("!", "addsudo", addsudo), group=0)
    app.add_handler(PrefixHandler("!", "delsudo", delsudo), group=0)
    app.add_handler(PrefixHandler("!", "listsudo", listsudo), group=0)
    app.add_handler(PrefixHandler("!", "swipe", swipe_cmd), group=0)
    app.add_handler(PrefixHandler("!", "stopswipe", stopswipe_cmd), group=0)
    app.add_handler(PrefixHandler("!", "replylolla", replylolla_cmd), group=0)
    app.add_handler(PrefixHandler("!", "stopreplylolla", stopreplylolla_cmd), group=0)
    app.add_handler(PrefixHandler("!", "getlink", getlink_cmd), group=0)

    app.add_handler(MessageHandler(filters.ALL, auto_replies), group=1)
    return app

async def run_all_bots():
    global apps, bots, bot_usernames
    for token in TOKENS:
        if token.strip():
            try:
                app = build_app(token)
                await app.initialize()
                await app.start()
                await app.updater.start_polling(drop_pending_updates=True)
                me = await app.bot.get_me()
                bot_usernames.append(me.username)
                apps.append(app)
                bots.append(app.bot)
                print(f"{C_GREEN}[SUCCESS] Bot running: @{me.username}{C_RESET}")
            except Exception as e:
                print(f"{C_RED}[ERROR] Failed to start bot: {e}{C_RESET}")

    if not apps:
        print(f"{C_RED}❌ No bots could be started. Exiting.{C_RESET}")
        return
    print(f"\n{C_GREEN}🚀 Lolla Keng Multi-Bot is running!{C_RESET}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_all_bots())
    except KeyboardInterrupt:
        print(f"\n{C_YELLOW}Shutting down...{C_RESET}")
    finally:
        loop.close()