import discord
from discord.ext import commands
import asyncio
from crawler import min_price_crawler
import threading
from concurrent.futures import ThreadPoolExecutor
import pymongo
from dotenv import load_dotenv
import os


load_dotenv()

TOKEN = os.getenv('TOKEN')
MONGO = os.getenv('MONGO')

bot = commands.Bot(command_prefix= ">")

client = pymongo.MongoClient(MONGO)
db = client["Items"]
collection = db["Items"]

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
        
        update_ids = []
        threads = []
        query = collection.find({})
        items = [i for i in query]

        with ThreadPoolExecutor() as executor:

            for item in items:
                try:
                    thread = executor.submit(min_price_crawler, item["item_id"])
                    threads.append(thread)
                except Exception as e:
                    print(e)
    
        results = [thread.result() for thread in threads]

        for result in results:
            for item in items:

                if result[0] == item["item_id"]:
                    if item["price"] == "Item not announced yet" or result[1] == "Item not announced yet":
                        continue
                    if int(result[1]) != int(item["price"]):
                        update_ids.append((item["_id"], item["channel_id"], item["item_id"], result[1]))

        for id in update_ids:
            channel = bot.get_channel(id=int(id[1]))
            collection.replace_one({"_id": id[0]}, {"channel_id":id[1], "item_id":id[2], "price": id[3]})

            await channel.send(f"Item: {id[2]} now is {id[3]} zenys")

        await asyncio.sleep(30)

@bot.event
async def on_ready():

    bot.loop.create_task(market_analyzer())
    print(f"Connected as {bot.user}")

@bot.command()
async def warn(ctx, channel_name, item_id):
    user = ctx.message.author

    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    channel_id = channel.id

    try:
        item = collection.find_one({"channel_id": str(channel_id), "item_id": item_id})
    except Exception as e:
        print(e)
        item = None
    
    if item != None:
        await ctx.send("Item already on warn")
    else:
        id, price = min_price_crawler(item_id)
        collection.insert_one({"channel_id": str(channel_id), "item_id": item_id, "price": price})
        await ctx.send(f"{user} put a warn in Item: {item_id}")

@bot.command()
async def unwarn(ctx, channel_name, item_id):

    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    channel_id = channel.id

    try:
        collection.delete_one({"channel_id": str(channel_id), "item_id": item_id})
        await ctx.send(f"Item: {item_id} has been removed from channel: {channel_name}")
        
    except Exception as e:
        print(e)
        await ctx.send("Item couldn't be removed")


bot.run(TOKEN)