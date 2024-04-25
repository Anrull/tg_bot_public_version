# kb = [
#         [types.KeyboardButton(text="11B")],
#         [types.KeyboardButton(text="11A")],
#         [types.KeyboardButton(text="10B")],
#         [types.KeyboardButton(text="10A")],
#         [types.KeyboardButton(text="9B")],
#         [types.KeyboardButton(text="9A")],
#         [types.KeyboardButton(text="8B")],
#         [types.KeyboardButton(text="8A")],
#         [types.KeyboardButton(text="7C")],
#         [types.KeyboardButton(text="7B")],
#         [types.KeyboardButton(text="7A")],
#         [types.KeyboardButton(text="6B")],
#         [types.KeyboardButton(text="6A")]
#     ]

# builder = InlineKeyboardBuilder()
    
# for i in config.list_classes:
#     builder.button(text=f"{i}", callback_data=f"{i}")

# keyboard = types.ReplyKeyboardMarkup(
#     keyboard=kb,
#     resize_keyboard=True,
#     input_field_placeholder="choice",
# )

# builder.adjust(4, 4)

# await message.reply(text=config.hello_message, reply_markup=builder.as_markup())