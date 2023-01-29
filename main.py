# 5123712096:AAFoWsAeO_sJyrsl0upMa-LUCeHE-k8AWYE

# kmc bot
# 5255258937:AAHm1mOMKghVn8JA_55D7wbF0vrwGldtdCg
from datetime import datetime , timedelta , timezone
from pytz import timezone
from collections import OrderedDict
from pymongo import MongoClient
import telegram
from telegram.ext import *
import scratch as s
from telegram import KeyboardButton , ReplyKeyboardMarkup


bot = telegram.Bot(token="5255258937:AAHm1mOMKghVn8JA_55D7wbF0vrwGldtdCg")

# API_KEY = "5299420575:AAHDNH7-5Q6LhCqgQ_ZBwz8XSY2oFBz6dyM"


MONGODB_URL = "mongodb+srv://pugalkmc:pugalkmc@cluster0.vx30p.mongodb.net/botdbs?retryWrites=true&w=majority"

# MONGODB_URI = os.environ["mongodb+srv://pugalkmc:pugalkmc@cluster0.vx30p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"]

client = MongoClient(MONGODB_URL)
mydb = client.get_default_database()


def start(update , context):
    sender = update.message.reply_text
    chat_id = update.message.chat_id
    username = update.message.chat.username
    if str(username) == "None":
        sender("No username found for your account")
        sender("Please set username for your telegram\n1)Go telegram account settings\n2)Click username\n3)Set unique and simplified username")
    else:
        checking_exist = mydb["people"]
        update.message.reply_text("Please click this /help to continue chat")
        reply_keyboard = [['Question', 'Form Link', 'Active events'], ['Submit task']]
        update.message.reply_text("Use below buttons for quick access",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                               one_time_keyboard=True))

        for i in checking_exist.find({}):
            if username == i["username"]:
                break
        else:
            checking_exist.insert_one({"_id": chat_id, "username": username})
            bot.sendMessage(chat_id=1291659507, text="New user found @" + str(username))
            bot.sendMessage(chat_id=1292480260, text="New user found @" + str(username))


def help(update, context):
    sender = update.message.reply_text
    username = update.message.chat.username
    if str(username) == "None":
        sender("No username found for your account")
        sender("Please set username for your telegram\n1)Go telegram account settings\n2)Click username\n3)Set unique and simplified username")
    else:
        update.message.reply_text("""Available Commands :-
        /about_project_work - Full details about our work
        /tele_group - HOL Telegram group URL
        /daily_form_link - Daily Task form updated URL
        /active_events - Daily Task form updated URL""")


about_work = "none for now"


def About_Project(update, context):
    sender = update.message.reply_text
    username = update.message.chat.username
    if str(username) == "None":
        sender("No username found for your account")
        sender("Please set username for your telegram\n1)Go telegram account settings\n2)Click username\n3)Set unique and simplified username")
    else:
        update.message.reply_text(about_work)


def tele_group(update, context):
    sender = update.message.reply_text
    username = update.message.chat.username
    if str(username) == "None":
        sender("No username found for your account")
        sender("Please set username for your telegram\n1)Go telegram account settings\n2)Click username\n3)Set unique and simplified username")
    else:
        update.message.reply_text("Telegram group URL:\nhttps://t.me/dastofficialtg/")


def form(update, context):
    sender = update.message.reply_text
    username = update.message.chat.username
    if str(username) == "None":
        sender("No username found for your account")
        sender("Please set username for your telegram\n1)Go telegram account settings\n2)Click username\n3)Set unique and simplified username")
    else:
        getform_link = mydb["formlink"]
        get = getform_link.find_one({"_id": 0}, {"_id": 0, "link": 1})
        update.message.reply_text(get["link"])


def daily_work(update, context):
    sender = update.message.reply_text
    username = update.message.chat.username
    if str(username) == "None":
        sender("No username found for your account")
        sender("Please set username for your telegram\n1)Go telegram account settings\n2)Click username\n3)Set unique and simplified username")
    else:
        from database import event_logic
        event_logic(update)


def admin_commands():
    admin_cmd = """Available admin commands
    1) append <your text> --to add as question\n
    2) set_form <form link> --to set or update new form\n
    3) set_about <your text> --to add information about this project work\n
    4) set_new_event <your event message> --to set new events\n
    5) del_event <enter text> --delete already used event text to delete"""
    return admin_cmd


commands_list = ["hol_user_list", "hol_user_remove", "remove_admin", "add_admin", "multiple_add_question",
                 "commands_list", "del_event", "set_new_event", "set_new_form", "add_qn", "hol_user_add",
                 "request_question", "permission_list", "announcement_user", "give_all_questions","send_msg","trigger"]


def msg_handle(update, context):
    sender = update.message.reply_text
    username = update.message.chat.username
    chat_id = update.message.chat_id
    # first_name = update.message.chat.first_name
    # last_name = update.message.chat.last_name
    text = str(update.message.text)
    text_low = text.lower()
    taken = ""
    for i in commands_list:
        if i in text:
            taken = "yes"
            break
    if str(username) == "None":
        sender("No username found for your account")
        sender("Please set username for your telegram\n1)Go telegram account settings\n2)Click username\n3)Set unique and simplified username")

    elif "question" == text_low:
        from database import question_ask
        question_ask(update, username)
    elif "submit task" == text_low:
        from database import sumbit_request
        sumbit_request(update, bot, username, chat_id)
    elif "https://t.me/dastofficialtg/" in text:
        if text != "https://t.me/dastofficialtg/" or "https://t.me/dastofficialtg":
            from database import task_submit
            task_submit(update, bot, username, chat_id, text)
        else:
            sender("Wrong format")
    elif "form link" in text_low:
        form(update, context)
    elif "active events" in text_low:
        from database import event_logic
        event_logic(update)
    elif taken == "yes":
        admin_col = mydb["admins"]
        for i in admin_col.find({}):
            if username == i["username"]:
                from admin_fun import admin_mod
                admin_mod(update, text, bot, telegram)
                break
        else:
            sender("You don't have permission to access this")

    else:
        response = s.sample(text_low)
        sender(response)

def stats_month(update, context):
    chat_id = update.message.chat_id
    username = update.message.chat.username
    update.message.reply_text("Please wait some moment to get full analysis")
    update.message.reply_text("Daily Statistics")
    user_dict_temp = {}
    for i in range(1,31):
        if i < 10:
            st = "0"+str(i)
            stats = mydb["task_store" + st]
        else:
            stats = mydb["task_store"+str(i)]
        list_list = []
        for j in stats.find({}):
            keys = list(user_dict_temp.keys())
            if j["username"] not in keys:
                user_dict_temp[j["username"]] = len(j["link"])
            else:
                get = user_dict_temp[j["username"]]
                get += len(j["link"])
                user_dict_temp[j["username"]] = get
            number = []
            number.append(j["username"])
            number.append(len(j["link"]))
            list_list.append(number)

        if len(list_list) != 0:
            bot.sendMessage(chat_id = chat_id, text = "date - {0}:\n{1}".format(i , '\n'.join(str(x) for x in list_list)))
    update.message.reply_text("- - - - - - - - - - - - -")
    update.message.reply_text("Total Monthly Statistics:")
    dict1 = OrderedDict(sorted(user_dict_temp.items()))
    for i in list(dict1.keys()):
        bot.sendMessage(chat_id = chat_id , text = "{0} - {1}".format(i,user_dict_temp[i]))

def error(update, context):
    pass


def main():
    updater = Updater("5255258937:AAHm1mOMKghVn8JA_55D7wbF0vrwGldtdCg", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("tele_group", tele_group))
    dp.add_handler(CommandHandler("about_project_work", About_Project))
    dp.add_handler(CommandHandler("daily_form_link", form))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("active_events", daily_work))
    dp.add_handler(CommandHandler("stats_month",stats_month))
    dp.add_handler(MessageHandler(Filters.text, msg_handle))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

main()
