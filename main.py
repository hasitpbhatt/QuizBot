import os
import discord
import asyncio
from keep_alive import keep_alive
import image_utils as iu
# install-pkg 
import pytesseract

client = discord.Client()


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
            if 'image' in y:
                print(y['image']['url'])
                im = iu.get_image_from_shoob(y['image']['url']).convert('L')
                im.save('a.png')
                filename = '{}.png'.format(message.channel.id)
                iu.process(im).save(filename)
                await message.channel.send(file=discord.File(filename))
                ch = message.channel
                await read_image_and_send(ch, filename)
                return

            elif 'got the card!' in y.get('description'):
                claim = True
                print(y['description'])

        if claim:
            await asyncio.sleep(120)
            await message.channel.send('Kalpana was killed')

    if not message.author.bot and message.content == 'read this' and len(message.attachments) > 0:
        print('reading')
        y = message.attachments[0]
        im = iu.get_image(y)
        filename = '{}_{}.png'.format(message.author.id, message.channel.id)
        im.save(filename)
        ch = message.channel
        await read_image_and_send(ch, filename)

async def read_image_and_send(channel, filename):
    txt = pytesseract.image_to_string(filename)
    print('got',txt)
    if txt and txt.strip() != '':
        print('txt',txt)
        await channel.send('-----\n' + txt + '\n-----\n')
    else:
        await channel.send('-----\n' + "Kuchh samajh nahi aaya" + '\n-----\n')

def run_server():
    os.environ['TESSDATA_PREFIX'] = "/home/runner/QuizBot/tessdata"
    keep_alive()
    client.run(os.environ['token'])

if __name__ == "__main__":
    run_server()
