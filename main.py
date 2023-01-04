from telethon import events
from config import bot, bot_username, database_channel, links_database, owner_id
from telethon import Button
from mongo import ChannelsDB, UsersDB
import time

ChannelsDB = ChannelsDB()
UsersDB = UsersDB()


@bot.on(events.NewMessage(pattern="/broadcast", chats=owner_id))
async def _(event):
    msg = await event.get_reply_message()
    users = UsersDB.full()
    for i in users:
        try:
            await bot.send_message(i['_id'], msg)
            time.sleep(1)
        except Exception as e:
            print(e)

@bot.on(events.NewMessage(pattern="/start"))
async def _(event):
    try:
        UsersDB.add({"_id": event.chat_id})
    except Exception as e:
        print(e)

    if event.raw_text == "/start":
        await event.reply(
            "This bot is to get links of anime files.",
            buttons=[
                    Button.text("Anime Channels"),
                    Button.text('Ongoing Anime', resize=True, single_use=True)
                ]
            )

    else:
        if event.raw_text.split()[1].split('_')[0] == "single":
            try:
                _, channel_id, msg_id = event.raw_text.split()[1].split('_')
                file_msg = await bot.get_messages(int(channel_id), ids=int(msg_id)) 
                await bot.send_message(
                    event.chat_id,
                    file_msg
                    )

            except:
                await bot.send_message(event.chat_id, "No file with such id found")
        
        else:
            try:
                _, start_id, end_id = event.raw_text.split()[1].split('_')
                start_id, end_id = int(start_id), int(end_id)
                ids = []
                for i in range(start_id, end_id + 1):
                    ids.append(i)

                files_msg = await bot.get_messages(database_channel, ids=ids) 
                for i in files_msg:
                    await bot.send_message(event.chat_id, i)
                    time.sleep(1)
            except:
                await bot.send_message(event.chat_id, "No file with such id found")


@bot.on(events.NewMessage(func=lambda e: e.is_private))
async def _(event):
    if event.file:
        await event.reply(f"[{event.file.name}](t.me/{bot_username}?start=single_{event.chat_id}_{event.id})")

    elif event.raw_text == "Anime Channels":
        await event.reply("Main channel - @Od3ns_Community")

    elif event.raw_text == "Ongoing Anime":
        await event.reply("Ongoing Anime - @Od3ns_Ongoing_Anime")


@bot.on(events.NewMessage(chats=database_channel))
async def _(event):
    if event.file:
        await bot.send_message(links_database, f"Click on this link and press start to download:\n[{event.file.name}](t.me/{bot_username}?start=single_{event.chat_id}_{event.id})")


@bot.on(events.NewMessage(pattern="/addc", chats=owner_id))
async def _(event):
    data = event.raw_text.split(" ", 2)
    username = data[1]
    channel_name = data[2]
    if username.startswith("@"):
        ChannelsDB.add({"_id": username, "name":channel_name})
        await event.reply(f"Added channel to database:\nName: {channel_name}\nLink: {username}")
    else:
        await event.reply("Add channels in format like:\n`/addc <@username_of_channel> <search terms>")


@bot.on(events.NewMessage(pattern="/removec", chats=owner_id))
async def _(event):
    username = event.raw_text.split()[1]
    try:
        ChannelsDB.remove({"_id": username})
        await event.reply(f"Removed: {username}")
    except:
        await event.reply(f"{username} doesnt exist in database")


@bot.on(events.NewMessage(pattern="/search"))
async def _(event):
    search_term = event.raw_text.split(" ", 1)[1].strip().replace(" ", "").lower()
    data = ChannelsDB.full()
    names_list = []
    for i in data:
        if search_term in i["name"].strip().replace(" ", "").lower():
            names_list.append(i)
    if names_list:
        buttons1 = []
        for i in names_list:
            if len(i["name"]) > 55:
                buttons1.append([Button.inline(f'{i["name"][:22]}. . .{i["name"][-22:]}', data=i["_id"])])
            else:
                buttons1.append([Button.inline(i["name"], data=i["_id"])])

        await event.reply("Search results:", buttons=buttons1)
    else:
        await event.reply("No such anime found in our database")


@bot.on(events.CallbackQuery(pattern=b"@"))
async def _(event):
    data = event.data.decode('utf-8')
    await bot.send_message(event.chat_id, str(data))


@bot.on(events.NewMessage(pattern="/create_batch"))
async def _(event):
    data = event.raw_text.split(" ", 2)
    file_range = data[1].strip().replace("-", "_")
    button_text = data[2]
    msg = await event.get_reply_message()
    await bot.send_message(
        event.chat_id,
        msg,
        buttons=[Button.url(button_text, url=f"t.me/{bot_username}?start=batch_{file_range}")]
    )


@bot.on(events.NewMessage(pattern="/create_link"))
async def _(event):
    data = event.raw_text.split(" ", 1)
    file_range = data[1].strip().replace("-", "_")    
    await event.reply(f"t.me/{bot_username}?start=batch_{file_range}")


bot.start()

bot.run_until_disconnected()
