import discord
from discord.ext import commands
import asyncio
from crawler import min_price_crawler
import threading
from concurrent.futures import ThreadPoolExecutor

bot = commands.Bot(command_prefix= ">")

with open("items.txt", "a+"):
    pass

def double_search(list_1, list_2, value_1, value_2):
    if len(list_1) == len(list_2):
        for i in range(len(list_1)):
            if list_1[i] == value_1 and list_2[i] == value_2:
                return i
    return -1

def unique_ids(id_list):
    unique_ids = []
    for id in id_list:
        if id not in unique_ids:
            unique_ids.append(id)
    return unique_ids


async def market_analyzer():
    await bot.wait_until_ready()

    while not bot.is_closed():
        data = {
            "channels": [],
            "items": [],
            "prices": []
        }

        new_prices = []

        unique_items = []

        lines = []

        threads = []

        index_updates = []

        results = []

        with open("items.txt", "r") as file:

            for line in file.readlines():

                lines.append(line)

                content = line.split(",")

                data["channels"].append(content[0])
                data["items"].append(content[1])
                data["prices"].append(content[2])

            unique_items = unique_ids(data["items"])

        with ThreadPoolExecutor() as executor:
            for item in unique_items:
                try:
                    thread = executor.submit(min_price_crawler, item)
                    threads.append(thread)
                    
                except:
                    print("Deu merda")
    
        results = [thread.result() for thread in threads]

        print(results)

        for i in range(len(results)):
            for j in range(len(data["items"])):
                if results[i][0] == data["items"][j]:
                    if data["prices"][j] == "Item not announced yet" or results[i][1] == "Item not announced yet":
                        continue
                    if int(results[i][1]) != int(data["prices"][j]):
                        index_updates.append(j)
                    
        index_updates.sort(reverse=True)

        for i in index_updates:
            del lines[i]
            lines.append(f"{}")

        with open("items.txt", "w+") as f:
            for i in lines:
                f.write()

        print()

        await asyncio.sleep(60)

@bot.event
async def on_ready():

    bot.loop.create_task(market_analyzer())
    print(f"Connected as {bot.user}")

@bot.command()
async def warn(ctx, channel_name, item_id):
    user = ctx.message.author

    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    channel_id = channel.id

    data = {
        "channels": [],
        "items": [],
        "prices": []
    }

    with open("items.txt", "r") as file:
        for line in file.readlines():
            content = line.split(",")
            
            data["channels"].append(content[0])
            data["items"].append(content[1])
            data["prices"].append(content[2])
            
    with open("items.txt", "a") as file:
 
        i = double_search(data["channels"], data["items"], str(channel_id), str(item_id))

        print(i)
       
        if i != -1:
            await ctx.send("Item already on warn")
        else:
            id, price = min_price_crawler(item_id)
            file.write(f"{channel_id},{item_id},{price}\n")
            await ctx.send(f"{user} put a warn in Item: {item_id}")

        

@bot.command()
async def set_channel(ctx, name):

    channel = discord.utils.get(ctx.guild.channels, name=name)
    channel_id = channel.id 

    channels = [] 

    with open("channels.txt", "r") as file:
        for line in file.readlines():
            channels.append(int(line))

    with open("channels.txt", "a") as file:
        if channel_id not in channels:
            file.write(str(channel_id)+"\n")
            await ctx.send(f"Channel: id: {channel_id}, name: {name} has been set to warn")
        else:
            await ctx.send(f"Channel: id: {channel_id}, name: {name} has been set to warn")
        

    

bot.run("ODMzMDcyNjc2NzE2ODA2MTg0.YHtBYw.n8HzMn_TgGp5VciGRl2abcDY3dU")