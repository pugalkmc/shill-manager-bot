
import pymongo

import datetime
import random

MONGODB_URL = "mongodb+srv://pugalkmc:pugalkmc@cluster0.vx30p.mongodb.net/botdbs?retryWrites=true&w=majority"

# MONGODB_URI = os.environ["mongodb+srv://pugalkmc:pugalkmc@cluster0.vx30p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"]

client = pymongo.MongoClient(MONGODB_URL)
mydb = client.get_default_database()


def question_ask(update, username):
    sender = update.message.reply_text
    fix = check_per(username)
    qn_request = mydb["qn_reason"]
    question = mydb["questions"]
    check = qn_request.find_one({"_id": 0})
    if check["request"] == "true":
        if fix == "allow":
            try:
                list_ids = []
                now = datetime.datetime.now() - datetime.timedelta(days=1)
                for i in question.find({}):
                    if i["time"] < now:
                        list_ids.append(i["_id"])
                rand = random.choice(list_ids)
                qn_get_unformat = question.find_one({"_id": rand})
                qn_format = qn_get_unformat["question"]
                qn_repeat = qn_get_unformat["repeat"]
                qn_time = datetime.datetime.now()
                qn_repeat -= 1
                question.update_one({"_id": rand}, {"$set": {"repeat": qn_repeat, "time": qn_time}})
                if qn_repeat == 0:
                    question.delete_one({"_id": rand})
                sender(qn_format)
            except:
                sender("No questions available at the moment")
        else:
            sender("You don't have permission to get questions")
    else:
        sender("Question provider currently off\nReason:\n{0}".format(check["reason"]))


def event_logic(update):
    events = mydb["events"]
    sender = update.message.reply_text
    length = 0
    for i in events.find({}):
        length += 1
    if length == 0:
        sender("No active events founded")
    else:
        sender("Current active events:")
        for i in events.find({}):
            update.message.reply_text(i["event_text"])


def dict_add(update, text):
    mydb = client["botdbs"]
    total_key = []
    myquestion = mydb["questions"]
    get_all = myquestion.find({})
    dup = "no"
    for i in get_all:
        if i["question"] == text:
            update.message.reply_text("Duplicate question found:\n" + str(text))
            dup = "yes"
            break
    if dup == "no":
        get_all = myquestion.find({})
        for j in get_all:
            print(j)
            total_key.append(j["_id"])
        for k in range(1, 500):
            if k not in total_key:
                from datetime import datetime, timedelta
                now = datetime.now() - timedelta(days=1)
                myquestion.insert_one({"_id": k, "time": now, "question": text, "repeat": 7})
                update.message.reply_text("added at index " + str(k))
                break
        else:
            update.message.reply_text("Out of range 500")


def dict_add_multiple(update, text_list):
    mydb = client["botdbs"]
    myquestion = mydb["questions"]
    now = datetime.datetime.now()
    indexing = []
    dup_list = 0
    find_dup = myquestion.find({})
    #
    for i in find_dup:
        get = i["question"]
        if get in text_list:
            text_list.remove(get)
            dup_list += 1
    update.message.reply_text("Total duplicates found:" + str(dup_list))
    #
    for i in text_list:
        total_key = []
        get_all = myquestion.find({})
        for j in get_all:
            get_keys = j["_id"]
            total_key.append(get_keys)
        for k in range(1, 400):
            if k not in total_key:
                myquestion.insert_one({"_id": k,"time":now, "question": i, "repeat": 7})
                indexing.append(k)
                break
        else:
            update.message.reply_text("Out of range 400")
    if len(indexing) == 0:
        update.message.reply_text("list of index used 'None'")
    else:
        update.message.reply_text("list of index used" + str(indexing))
        update.message.reply_text("New multiple questions added")

def sumbit_request(update , bot , username , chat_id):
    if check_per(username) == "allow":
        update.message.reply_text("🔽Now send your message link🔽")
    else:
        update.message.reply_text("You don't have permission to do task")

def check_per(username):
    fix = "none"
    question_per = mydb["qn_permission"]
    for i in question_per.find({}):
        if i["username"] == username:
            fix = "allow"
    return fix


from pytz import timezone

def task_submit(update , bot , username , chat_id ,text):
    ind_time_date = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%d')
    store = mydb["task_store"+ind_time_date]
    fix = check_per(username)
    ind_time = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M')
    if "allow" == fix:
        for i in store.find({}):
            if i["_id"] == chat_id:
                store.delete_one({"_id": chat_id})
                list_ = []
                for i in i['link']:
                    list_.append(i)
                else:
                    list_.append(text)
                store.insert_one({"_id": chat_id, "username": username, "link": list_ , "time":ind_time})
                update.message.reply_text("Got your response successfully")
        else:
            store.insert_one({"_id": chat_id, "username": username, "link":[text], "time":ind_time})
            update.message.reply_text("Got your response successfully")

def trigger(update,bot):
    ind_time = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%d')
    check_active = mydb["task_store"+ind_time]
    for i in check_active.find({}):
        if len(i["link"]) == 1:
            bot.sendMessage(chat_id=i["_id"], text="Task Remainder⏰:\nYou completed only 1 task\nDo remaining 4 task for today")
        elif len(i["link"]) == 2:
            bot.sendMessage(chat_id=i["_id"], text="Task Remainder⏰:\nYou completed only 2 task\nDo remaining 3 task for today")
        elif len(i["link"]) == 3:
            bot.sendMessage(chat_id=i["_id"], text="Task Remainder⏰:\nYou completed only 3 task\nDo remaining 2 more task for today")
        elif len(i["link"]) == 4:
            bot.sendMessage(chat_id=i["_id"], text="Task Remainder⏰:\nYou completed only 4 task\nDo one more task for today")
        else:
            bot.sendMessage(chat_id=i["_id"], text = "Task Remainder⏰:\nYou are looks inactive today\nDo total of 5 task for today")
    else:
        update.message.reply_text("Triggered all task worker...Done")
