import random

def sample(input_text):
   message = input_text.lower()
   if message in ("hi", "hello"):
       return "Hi,How can i help you\nUse /help to get commands to use"
   elif message in ("bye", "byee", "byeee"):
       return "bye , See you soon"
   elif message == ("how are you"):
       return "fine"
   elif message == "about":
       return "I'm Heros of the land task manager\nCreated by @PugalKMC"
   elif message in ("not received", "not receive"):
       return "ohhh"
   elif message in ("youtube", "youtube link", "channel link","youtube url"):
       return "YouTube link:\nhttps://youtube.com/channel/UCYc3hX7Q8ljFT5oRo6RqBPg"