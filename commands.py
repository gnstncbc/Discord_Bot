# commands.py

import responses

async def handle_message(message, client):
    user_message = str(message.content)
    channel = str(message.channel)

    if user_message[0] == '?':
        user_message = user_message[1:]  # Remove the '?' prefix for private messages
        await send_private_message(message, user_message)
    else:
        await send_public_message(message, user_message)

    if user_message == 'eyv':
        raise SystemExit

async def send_private_message(message, user_message):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response)
    except Exception as e:
        print(e)

async def send_public_message(message, user_message):
    try:
        response = responses.handle_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)
