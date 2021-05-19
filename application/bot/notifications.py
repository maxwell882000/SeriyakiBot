from application import telegram_bot
from application.core import notifyservice, orderservice, userservice
from application.core.models import Order, Comment
from application.resources import strings
from telebot.types import Message
from telebot.apihelper import ApiException
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def check_group(m: Message):
    return m.chat.type == 'group' or m.chat.type == 'supergroup'


@telegram_bot.message_handler(commands=['notify'], func=check_group)
def notifications_handler(message: Message):
    chat_id = message.chat.id
    chat_title = message.chat.title

    result = notifyservice.add_notification_chat(chat_id, chat_title)
    if result:
        success_message = strings.get_string('notifications.success')
        telegram_bot.send_message(chat_id, success_message)
    else:
        exist_message = strings.get_string('notifications.exist')
        telegram_bot.send_message(chat_id, exist_message)

@telegram_bot.callback_query_handler(func=lambda call: str(call.data).startswith('order:'))
def notification_callback_query(call):
    order = orderservice.get_order_by_id(int(call.data[6:]))
    user_id = order.user_id 
    user = userservice.get_user_by_id(call.from_user.id)
    for chat in notifyservice.get_all_notification_chats():
        try:
            telegram_bot.send_message(chat.chat_id, 'Заказ #{}, принял {}'.format(order.id, call.from_user.first_name))
        except ApiException:
            pass
    telegram_bot.send_message(user_id, strings.get_string('notify.accepted'))
    telegram_bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    telegram_bot.answer_callback_query(call.id)

def notify_new_order(order: Order, total_sum: float):
    notification_chats = notifyservice.get_all_notification_chats()
    notification_message = strings.from_order_notification(order, total_sum)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(strings.get_string('notify.accept'), callback_data='order:' + str(order.id)))
    for chat in notification_chats:
        try:
            telegram_bot.send_message(chat.chat_id, notification_message, reply_markup=markup, parse_mode='HTML')
            if order.location:
                telegram_bot.send_location(chat.chat_id, order.location.latitude, order.location.longitude)
        except ApiException:
            pass


def notify_new_comment(comment: Comment):
    notification_chats = notifyservice.get_all_notification_chats()
    notification_message = strings.from_comment_notification(comment)
    for chat in notification_chats:
        try:
            telegram_bot.send_message(chat.chat_id, notification_message, parse_mode='HTML')
        except ApiException:
            pass
