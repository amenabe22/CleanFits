from aiogram_forms import forms, fields
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

class UserForm(forms.Form):
    # LANGUAGE_CHOICES = ('English', 'Russian', 'Chinese')
    # LANGUAGE_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(*[
    #     KeyboardButton(label) for label in LANGUAGE_CHOICES
    # ])

    name = fields.StringField('Name')
    # language = fields.ChoicesField(
    #     'Language', LANGUAGE_CHOICES, reply_keyboard=LANGUAGE_KEYBOARD)
    email = fields.EmailField(
        'Email', validation_error_message='Wrong email format!')

class NewStoreForm(forms.Form):
    LOCATION_CHOICES = ('Yes', 'Not Yet', 'Soon')
    # LOCATION_KEYBOARD = InlineKeyboardMarkup().add(*[
    #     InlineKeyboardButton(label) for label in LOCATION_CHOICES
    # ])
    LOCATION_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(*[
        KeyboardButton(label) for label in LOCATION_CHOICES
    ])

    store_name = fields.StringField('Store Name')
    location = fields.ChoicesField(
        'Has Physical Location', LOCATION_CHOICES, reply_keyboard=LOCATION_KEYBOARD)

    # language = fields.ChoicesField(
    #     'Language', LANGUAGE_CHOICES, reply_keyboard=LANGUAGE_KEYBOARD)
    email = fields.EmailField(
        'Email', validation_error_message='Wrong email format!')
