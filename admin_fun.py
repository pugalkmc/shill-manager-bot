import pymongo

from datetime import datetime
import random

commands_list = ["hol_user_list", "hol_user_remove", "remove_admin", "add_admin", "multiple_add_question",
                 "commands_list", "del_event", "set_new_event", "set_new_form", "add_qn", "hol_user_add",
                 "request_question", "permission_list", "announcement_user", "give_all_questions", "send_msg","trigger"]

MONGODB_URL = "mongodb+srv://pugalkmc:pugalkmc@cluster0.vx30p.mongodb.net/botdbs?retryWrites=true&w=majority"

# MONGODB_URI = os.environ["mongodb+srv://pugalkmc:pugalkmc@cluster0.vx30p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"]

client = pymongo.MongoClient(MONGODB_URL)
mydb = client.get_default_database()


def admin_mod(update, text, bot, telegram):
    username = update.message.chat.username
    chat_id = update.message.chat_id
    sender = update.message.reply_text

    if "del_event " in text:
        daily_work_event_del = text.replace("del_event ", '')
        del_event = mydb["events"]
        for i in del_event.find({}):
            if daily_work_event_del == i["event_text"]:
                del_event.delete_one({"_id": i["_id"]})
                sender("SUCCESSFULLY DELETED THE GIVEN EVENT\n\n{0}".format(i["event_text"]))
                from database import event_logic
                event_logic(update)
                break
        else:
            sender("No event founded , please give correctly")

    elif "set_new_event " in text:
        daily_work_event_text = text.replace("set_new_event ", '')
        events = mydb["events"]
        total_key = []
        get_all = events.find({})
        for i in get_all:
            get_keys = i["_id"]
            total_key.append(get_keys)
        for i in range(1, 10):
            if i not in total_key:
                from datetime import datetime
                now = datetime.now()
                events.insert_one({"_id": i, "time": now, "event_text": daily_work_event_text})
                update.message.reply_text("added at index " + str(i))
                sender("New work set done")
                break
        else:
            update.message.reply_text("Out of range 10")


    elif "set_new_form " in text:
        updated_form = text.replace("set_new_form ", 'Daily task form link:\n')
        myform_get = mydb["formlink"]
        try:
            myform_get.delete_one({"_id": 0})
            sender("Deleted form")
            myform_get.insert_one({"_id": 0, "link": updated_form})
            sender("New form set done")
        except:
            sender("Error found on set new form link")

    elif "add_qn " in text:
        text_qn = text.replace("add_qn ", '')
        from database import dict_add
        dict_add(update, text_qn)
    elif "hol_user_remove " in text:
        hol_remove = text.replace("hol_user_remove ", "")
        hol_remove = hol_remove.replace("@", '')
        qn_userremove_col = mydb["qn_permission"]
        counter = qn_userremove_col.find({})
        if "PugalKMC" == hol_remove  and username != "PugalKMC":
            sender("Can't do this operation on owner")
        else:
            for i in counter:
                if hol_remove == i["username"]:
                    qn_userremove_col.delete_one({"username": hol_remove})
                    sender("Permission removed for user @{0}".format(hol_remove))
                    break
            else:
                sender("No user found named as {0}".format(hol_remove))
    elif "hol_user_add " in text:
        text_user = text.replace("hol_user_add ", '')
        qn_useradd_col = mydb["qn_permission"]
        check = qn_useradd_col.find({})
        if "@" in text_user:
            text_user = text_user.replace("@", '')
        for i in check:
            if text_user == i["username"]:
                sender("User already exist")
                break
        else:
            qn_useradd_col.insert_one({"username": text_re})
            sender("Qn permission given to user @{0}".format(text_re))
    elif "hol_user_list" in text:
        qn_useradd_col = mydb["qn_permission"]
        qn_per = []
        for i in qn_useradd_col.find({}):
            qn_per.append(i["username"])
        sender("Current question permission given for:\n{0}".format(', '.join(str("@" + x) for x in qn_per)))
    elif "request_question " in text:
        qn_reason = mydb["qn_reason"]
        text = text.replace("request_question ", "")
        if "true" in text:
            qn_reason.delete_one({"_id": 0})
            qn_reason.insert_one({"_id": 0, "request": "true", "reason": "None"})
            sender("Question request permission granted")
        elif "false" in text:
            text = text.replace("false", '')
            qn_reason.delete_one({"_id": 0})
            if len(text) >= 2:
                qn_reason.insert_one({"_id": 0, "request": "false", "reason": text})
            else:
                qn_reason.insert_one({"_id": 0, "request": "false", "reason": "None"})
            sender("Question request permission denied to users")
        else:
            sender("Command error found:\nUse admin_command to get full details about admin commands")
    elif "commands_list" in text:
        sender("Command list:\n{0}".format(', '.join(str(x) for x in commands_list)))
    elif "give_all_questions" in text:
        questions = mydb["questions"]
        list_questions = []
        getter = questions.find({})
        for i in getter:
            list_questions.append(i["question"])
        sender("total active questions:\n{0}".format('\n{}\n'.join(str(x) for x in list_questions)))

    elif "multiple_add_question " in text:
        text_mul = text.replace("multiple_add_question ", "")
        if "{}" in text_mul:
            text_list = text_mul.split("{}")
            from database import dict_add_multiple
            dict_add_multiple(update, text_list)
        else:
            sender("Not a correct format to add")
    elif "remove_admin " in text:
        admin_col = mydb["admins"]
        text_username = text.replace("remove_admin ", '')
        text_username = text_username.replace("@", '')
        if "PugalKMC" == text_username:
            sender("Can't remove bot owner")
        else:
            for i in admin_col.find({}):
                if i["username"] == text_username:
                    admin_col.delete_one({"_id": i["_id"]})
                    sender("Admin removed @" + text_username)
                    break
            else:
                sender("Admin username not found @{0}".format(text_username))
        admin_display(sender, admin_col)

    elif "add_admin " in text:
        admin_col = mydb["admins"]
        text_username = text.replace("add_admin ", '')
        for i in admin_col.find({}):
            if i["username"] == text_username:
                sender("@{0} already on admin post".format(i["username"]))
                break
        else:
            admin_col.insert_one({"username": text_username})
            sender("New admin @{0} successfully added ".format(text_username))
        admin_display(sender, admin_col)


    elif "announcement_user " in text:
        text_an = text.replace("announcement_user ", "")
        users = mydb["people"]
        users_list = users.find({})
        for i in users_list:
            bot.sendMessage(chat_id=i["_id"], text="<b>New Announcement❇</b>:\n\n" + text_an,
                            parse_mode=telegram.ParseMode.HTML)

        else:
            sender("Announcement successfully done")
    elif "send_msg" in text:
        if "send_msg_user" == text:
            users = mydb["people"]
            users_list = users.find({})
            for i in users_list:
                list_get = []
                id = i["_id"]
                user = i["username"]
                list_get.append(id)
                list_get.append(user)
                bot.sendMessage(chat_id=chat_id, text=list_get)
        if "send_msg " in text:
            text_an = text.replace("send_msg_user ", "")
            text_id = text_an.split("{}")
            bot.sendMessage(chat_id=text_id[0], text="<b>Message from admin❇</b>:\n\n" + text_id[1],
                            parse_mode=telegram.ParseMode.HTML)
            sender("Message sended successfully🥳")
    elif "trigger" == text:
        from database import trigger
        trigger(update, bot)
    else:
        sender("Error found on your admin command {0} \nTry Again".format(text))


def admin_display(sender, admin_col):
    admin_list = []
    for i in admin_col.find({}):
        admin_list.append(i["username"])
    sender("Current Admin list:\n{0}".format(', '.join(str("@" + x) for x in admin_list)))
