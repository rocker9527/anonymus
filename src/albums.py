# ForwardsCoverBot - don't let people on telegram forward with your name on the forward label
# Copyright (C) 2017-2019  Dario <dariomsn@hotmail.it> (github.com/91DarioDev)
#
# ForwardsCoverBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ForwardsCoverBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with ForwardsCoverBot.  If not, see <http://www.gnu.org/licenses/>

import storage

from telegram import InputMedia, InputMediaPhoto, InputMediaVideo
from telegram.ext import DispatcherHandlerStop, Updater
from telegram import ChatAction
from telegram import ParseMode
from string import Template

updater = Updater(storage.get_bot_token(), use_context=True)
bot = updater.bot

ALBUM_DICT = {}


def collect_album_items(update, context):
    """
    if the media_group_id not a key in the dictionary yet:
        - send sending action
        - create a key in the dict with media_group_id
        - add a list to the key and the first element is this update
        - schedule a job in 1 sec
    else:
        - add update to the list of that media_group_id
    """
    media_group_id = update.message.media_group_id
    if media_group_id not in ALBUM_DICT:
        bot.sendChatAction(
            chat_id=storage.get_target_chat(), 
            action=ChatAction.UPLOAD_PHOTO if update.message.photo else ChatAction.UPLOAD_VIDEO
        )
        ALBUM_DICT[media_group_id] = [update]
        # schedule the job
        context.job_queue.run_once(send_album, 10, context=[media_group_id])
    else:
        ALBUM_DICT[media_group_id].append(update)


def send_album(context):
    media_group_id = context.job.context[0]
    updates = ALBUM_DICT[media_group_id]

    # delete from ALBUM_DICT
    del ALBUM_DICT[media_group_id]

    # ordering album updates
    updates.sort(key=lambda x: x.message.message_id)

    media = []
    for update in updates:
        if update.message.photo:
            media.append(InputMediaPhoto(media=update.message.photo[-1].file_id, caption='',parse_mode=ParseMode.HTML))
        elif update.message.video:
            media.append(InputMediaVideo(media=update.message.video.file_id, caption='',parse_mode=ParseMode.HTML))
    
    try:
        bot.sendMediaGroup(chat_id=storage.get_target_chat(), media=media)
        bot.send_message(update.effective_chat.id, storage.get_string("MSG_SENT"), reply_to_message_id=update.message.message_id)
    except Exception as e:
            template = Template(storage.get_string("CANT_SEND"))
            bot.send_message(update.effective_chat.id, template.safe_substitute(message=e.message), reply_to_message_id=update.message.message_id)
    
