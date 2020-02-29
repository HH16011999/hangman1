import telebot
import config
import random
import time

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

words = ['cow', 'horse', 'parrot', 'wolf', 'fox', 'dog', 'cat']

playing = False
inputLetter = ''
listWord = []
rWord = ''
word = []
rWordLen = 0
h_id = 0
complite = 0
letters = []

def add_h_id():
	global h_id
	h_id += 1

def add_complite():
	global complite
	complite += 1

@bot.message_handler(commands=['start'])
def welcome(message):
	sti = open('static/welcome.webp', 'rb')
	bot.send_sticker(message.chat.id, sti)

	#keyboard
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Random number")
	item2 = types.KeyboardButton("Hangman")

	markup.add(item1, item2)
	bot_chat_id = message.chat.id
	bot.send_message(message.chat.id, "Welcome, {0.first_name}!\nI am - <b>{1.first_name}</b>".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
	nMessage = message
	if message.chat.type == 'private':
		if message.text == 'Random number':
			bot.send_message(message.chat.id, str(random.randint(0,100)))
		elif message.text == 'Hangman':
			global playing
			global inputLetter
			global word
			global rWordLen
			global rWord
			global listWord
			global h_id
			global complite
			global letters
			playing = True

			rWord = ''
			listWord = []
			tWord = ''
			
			letters = []
			
			mSender(message, '\nLets play game Hangman. I make up animal name and you try to guess it.\n')
			
			rWord = words[random.randint(0, len(words)-1)]
			rWordLen = len(rWord)
			
			tWord = ''
			ttWord = ''
			
			for number in range(rWordLen):
				tWord += '_'
				ttWord += '_ '
			
			word = list(tWord)
			mSender(message, ttWord)
		
			#bot.send_photo(message.chat.id, open('static/0.png', 'rb'))
		
			mSender(message, 'Enter your letter')
			h_id = 0
			complite = 0
			listWord = list(rWord)
			

		elif playing & len(message.text) == 1:
			if checkLetters(message.text):
				mSender(message, 'You already inputed this letter, try another.')
				return
			if listWord.count(message.text)<=1:
				letters.append(message.text)
			tempWord = ''
			inputLetter = message.text
			
			letterId = check(inputLetter)
			if letterId<0:
				mSender(message, 'Wrong letter. Try again.')
				add_h_id()
				bot.send_photo(message.chat.id, open('static/'+ str(h_id) + '.png', 'rb'))
				if h_id >= 6:
					mSender(message, 'Game over')
					playing = False
					return
			else:
				mSender(message, 'YEAH!!! Its true letter!')
				for y in range(rWordLen):
					if y == letterId:
						word[letterId] = listWord[letterId]
						listWord[letterId] = '-'
				for y in word:
					tempWord += y + ' '
				mSender(message, tempWord)
				add_complite()

				#bot.send_photo(message.chat.id, open('static/'+ str(h_id) + '.png', 'rb'))
				if complite >= rWordLen:
					mSender(message, 'You win!!!')
					playing = False
					return
				else:
					mSender(message, 'Enter your letter')

		else:
			bot.send_message(message.chat.id, "I don't know what to answer")

def check(letter):
	global listWord
	n = 0
	for x in listWord:
		if x == letter:
			return n
		else:
			n+=1
	return -1

def checkLetters(letter):
	return False if letters.count(letter) == 0 else True

@bot.message_handler(content_types=['text'])
def mSender(message, str):
	bot.send_message(message.chat.id, str)

#RUN
bot.polling(none_stop=True)


