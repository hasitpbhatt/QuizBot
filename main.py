import os
import discord
import asyncio
from keep_alive import keep_alive
import image_utils as iu
import pytesseract
import time

client = discord.Client()

mp = dict()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.bot and message.author.name == 'Shoob':
        claim = False
        for x in message.embeds:
            y = x.to_dict()
            if 'image' in y and message.channel.id == 836759068755361832:
                print(y['image']['url'])
                im = iu.get_image_from_shoob(y['image']['url']).convert('1').convert('L')
                filename = '{}.png'.format(message.channel.id)
                kk = iu.process(im)
                zz = iu.process2(kk)
                zz.save(filename)
                await message.channel.send(file=discord.File(filename))
                s = time.time()
                txt = pytesseract.image_to_string(zz)
                txt = txt.replace(' ','').replace('\n','').replace('\t','')
                print('txt',txt)
                await message.channel.send(
                '#### ' + txt + ' ####')
                print('took', time.time()-s)
                return

            elif 'got the card!' in y.get('description'):
                claim = True
                print(y['description'])

        if claim:
            mp[message.channel.id] = time.time()
            await asyncio.sleep(120)
            y = time.time()
            if y-mp[message.channel.id] >= 120:
              out_channel = message.channel
              # try:
              #   for ch in message.guild.channels:
              #       if 'shoob-reminder' in ch.name:
              #           print("found",ch)
              #           out_channel = client.get_channel(ch.id)
              # except:
              #   print("error occurred")
              # await out_channel.send('@{} feels lonely!!! <#{}>'.format(message.author.id,message.channel.id))
              role = discord.utils.find(
        lambda r: r.name == 'T1' or r.name == 'Ghajini', message.guild.roles)
              if role:
                await out_channel.send('<@&{}> Shoob remembers you!!!'.format(role.id))

def run_server():
    iu.init_tesseract()
    keep_alive()
    client.run(os.environ['token'])

if __name__ == "__main__":
    run_server()
