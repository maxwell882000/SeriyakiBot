import os

import telebot
from application import telegram_bot
from application.admin import bp
from application.core.models import User
from config import Config
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from werkzeug.utils import secure_filename

from .forms import MailForm


@bp.route('/mailing', methods=['GET', 'POST'])
@login_required
def mailing():
    mail_form = MailForm()
    if mail_form.validate_on_submit():
        file = request.files['image']
        file_name = file.filename
        if file:
            filename = secure_filename(file_name)
            file.save(os.path.join(Config.MAILING_DIRECTORY, filename))
        text = mail_form.mail.data
        file_id = None
        filepath = (Config.MAILING_DIRECTORY + file_name)
        if mail_form.image.data:
            if mail_form.preview.data == False:
                users = User.query.all()
                for user in users:
                    user_id = user.id
                    if file_id:
                        try:
                            file = open(filepath, 'rb')
                            telegram_bot.send_photo(chat_id=user_id,
                                                    photo=file_id,
                                                    caption=text)
                            file.close()
                        except telebot.apihelper.ApiException:
                            continue
                    else:
                        user_id = user.id
                        try:
                            file = open(filepath, 'rb')
                            file_id = telegram_bot.send_photo(chat_id=user_id,
                                                              photo=file,
                                                              caption=text).photo[-1].file_id
                            file.close()
                        except telebot.apihelper.ApiException:
                            continue
            elif mail_form.preview.data == True:
                users = [583411442, 1294618325, 64925540]
                for user in users:
                    user_id = user
                    if file_id:
                        try:
                            file = open(filepath, 'rb')
                            telegram_bot.send_photo(chat_id=user_id,
                                                    photo=file_id,
                                                    caption=text)
                            file.close()
                        except telebot.apihelper.ApiException:
                            continue
                    else:
                        user_id = user
                        try:
                            file = open(filepath, 'rb')
                            file_id = telegram_bot.send_photo(chat_id=user_id,
                                                              photo=file,
                                                              caption=text).photo[-1].file_id
                            file.close()
                        except telebot.apihelper.ApiException:
                            continue
            os.remove((Config.MAILING_DIRECTORY + "/" + file_name))
        else:
            if mail_form.preview.data == False:
                users = User.query.all()
                for user in users:
                    user_id = user.id
                    try:
                        telegram_bot.send_message(chat_id=user_id,
                                                  text=text)
                    except telebot.apihelper.ApiException:
                        continue

            elif mail_form.preview.data == True:
                users = [583411442, 1294618325, 64925540]
                for user in users:
                    try:
                        telegram_bot.send_message(chat_id=user,
                                                  text=text)
                    except telebot.apihelper.ApiException:
                        continue

        flash('Рассылка запущена!', category='success')
        return redirect(url_for('admin.mailing'))

    return render_template('admin/mailing.html',
                           title='Рассылка',
                           area='mailing',
                           mail_form=mail_form)
