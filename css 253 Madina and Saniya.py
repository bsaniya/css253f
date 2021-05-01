from bs4 import BeautifulSoup
from scraper_api import ScraperAPIClient
import unicodedata
import telebot
from telebot import types

#Credentials for the bot
TOKEN = '1748549673:AAE6knq5ZXGiYNNUuow3dNWvLzwLot1r-mY'
bot = telebot.TeleBot(TOKEN)

#Using ScraperAPIClient to mask IP address so the server won't block the parser
clientAPI = ScraperAPIClient('ff85490d3acca6769e6d7b196fe4644a')
top_ten = []


#function for analyze data

def main(region, rooms):
    urls = {
        'Москва' : 'https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ',
        'Санкт-Петербург' : 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ',
        'Новосибирск' : 'https://www.avito.ru/novosibirsk/kvartiry/prodam-ASgBAgICAUSSA8YQ',
        'Екатеринбург' : 'https://www.avito.ru/ekaterinburg/kvartiry/prodam-ASgBAgICAUSSA8YQ',
        'Нижний Новгород' : 'https://www.avito.ru/nizhniy_novgorod/kvartiry/prodam-ASgBAgICAUSSA8YQ',
        'Казань' : 'https://www.avito.ru/kazan/kvartiry/prodam-ASgBAgICAUSSA8YQ',
        'Самара' : 'https://www.avito.ru/samara/kvartiry/prodam-ASgBAgICAUSSA8YQ',
        'Челябинск' : 'https://www.avito.ru/chelyabinsk/kvartiry/prodam-ASgBAgICAUSSA8YQ',
        'Омск' : 'https://www.avito.ru/omsk/kvartiry/prodam-ASgBAgICAUSSA8YQ',
        'Ростов-на-Дону' : 'https://www.avito.ru/rostov-na-donu/kvartiry/prodam-ASgBAgICAUSSA8YQ',
        'Уфа' : 'https://www.avito.ru/ufa/kvartiry/prodam-ASgBAgICAUSSA8YQ',
        'Красноярск' : 'https://www.avito.ru/krasnoyarsk/kvartiry/prodam-ASgBAgICAUSSA8YQ',
        'Пермь' : 'https://www.avito.ru/perm/kvartiry/prodam-ASgBAgICAUSSA8YQ',
        'Волгоград' : 'https://www.avito.ru/volgograd/kvartiry/prodam-ASgBAgICAUSSA8YQ',
        'Воронеж' : 'https://www.avito.ru/voronezh/kvartiry/prodam-ASgBAgICAUSSA8YQ'
        }
    #current page
    page = 1
    #how many pages to parse
    pages_to_scrape = 2
    
    prices = 0
    apartment_count = 0
    price_of_apartment = ''
    
    if(region in urls):
        url = urls[region]
        current_url = url
        while True:
            r = clientAPI.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            parent_div = soup.find('div', class_='index-root-2c0gs')
            apartments = parent_div.find_all('div', class_='iva-item-root-G3n7v photo-slider-slider-3tEix iva-item-list-2_PpT iva-item-redesign-1OBTh items-item-1Hoqq items-listItem-11orH js-catalog-item-enum')
            print("URL: " + url)
            for apartment in apartments:
                try:    
                    all_data_div = apartment.find('div', class_='iva-item-body-NPl6W')
                    get_link = apartment.find('div', class_='iva-item-content-m2FiN')
                    apartment_price = all_data_div.find('div', class_='iva-item-priceStep-2qRpg').find('span', class_='price-text-1HrJ_ text-text-1PdBw text-size-s-1PUdo').contents[0]
                    description = all_data_div.find('div', class_='iva-item-titleStep-2bjuh').find('h3').contents[0] + ' | Price: ' + str(apartment_price) + ' RUB'
                    link = get_link.find('a', class_='iva-item-sliderLink-2hFV_').attrs['href']
                    try:
                        if(rooms == 1):
                            if(int(description[0]) == 1):
                                apartment_info = description + '\n Link: ' + 'https://www.avito.ru' + link
                                price_of_apartment = apartment_price
                                apartment_count += 1
                            else:
                                continue
                        elif(rooms == 2):
                            if(int(description[0]) == 2):
                                apartment_info = description + '\n Link: ' + 'https://www.avito.ru' + link
                                price_of_apartment = apartment_price
                                apartment_count += 1
                            else:
                                continue
                        elif(rooms == 3):
                            if(int(description[0]) == 3):
                                apartment_info = description + '\n Link: ' + 'https://www.avito.ru' + link
                                price_of_apartment = apartment_price
                                apartment_count += 1
                            else:
                                continue
                    except:
                        print('Not an apartment')  
                    prices += int(float(price_of_apartment.replace(' ','')))
                    if(unicodedata.normalize("NFKD", apartment_info) not in top_ten): #translate into readable format
                        top_ten.append(unicodedata.normalize("NFKD", apartment_info))
                except:
                    print('Some problem')
            print("Apartments num: " + str(apartment_count))
            page += 1
            if(page > pages_to_scrape):
                break
            url = current_url + '?p=' + str(page)

        avg_price = round(prices/apartment_count)

        result = ""
        #Assign collected data to the result variable
        for i in top_ten[-12:]:
            result += str(i) + "\n"

        result += "Average price: " + str(f"{avg_price:,}") + " RUB" + "\n" + 'Apartments analyzed: ' + str(apartment_count)

        return result

#Start of the Telegram bot

#States of the process
#We need state to keep track of the process. For example first comes CITY, then ROOMS. 
#The functions must be able to recognize their execution queue

bot.state = None 
CITY = 1
ROOMS = 3

#Initialize the data dictionary. I will use it assign inputs of the user
global data
data = {'city': "", 'rooms': ""}

#/start command listener
@bot.message_handler(commands=['start'])
def test(message):
    #List all the cities as a buttons
    keyboard = types.InlineKeyboardMarkup()
    a = types.InlineKeyboardButton(text = "Москва", callback_data='Москва')
    b = types.InlineKeyboardButton(text = "Санкт-Петербург", callback_data='Санкт-Петербург')
    c = types.InlineKeyboardButton(text = "Новосибирск", callback_data='Новосибирск')
    d = types.InlineKeyboardButton(text = "Екатеринбург", callback_data='Екатеринбург')
    e = types.InlineKeyboardButton(text = "Нижний Новгород", callback_data='Нижний Новгород')
    f = types.InlineKeyboardButton(text = "Казань", callback_data='Казань')
    g = types.InlineKeyboardButton(text = "Самара", callback_data='Самара')
    h = types.InlineKeyboardButton(text = "Челябинск", callback_data='Челябинск')
    i = types.InlineKeyboardButton(text = "Омск", callback_data='Омск')
    j = types.InlineKeyboardButton(text = "Ростов-на-Дону", callback_data='Ростов-на-Дону')
    k = types.InlineKeyboardButton(text = "Уфа", callback_data='Уфа')
    l = types.InlineKeyboardButton(text = "Красноярск", callback_data='Красноярск')
    m = types.InlineKeyboardButton(text = "Пермь", callback_data='Пермь')
    n = types.InlineKeyboardButton(text = "Волгоград", callback_data='Волгоград')
    o = types.InlineKeyboardButton(text = "Воронеж", callback_data='Воронеж')
    keyboard.add(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o)
    #Send message when /start command is typed
    bot.send_message(message.chat.id, "Hey there! Need info about apartments? Go ahead and choose the city", reply_markup=keyboard)

    #Change the state to CITY
    bot.state = CITY

#if /cancel command is given. the bot will stop the current action
@bot.message_handler(commands=['cancel'])
def test(message):
    bot.send_message(message.chat.id, 'Type /start to get info about apartments')
    bot.state = None

#Comes after the test function. Assigns city name to data dictionary.
@bot.callback_query_handler(func=lambda msg:bot.state==CITY)
def get_title(call):

    data['city'] = call.data

    #ask user about rooms 
    bot.send_message(call.message.chat.id, f"City: {call.data}\nHow many ROOMS?(1-3) \nNote: wait for a minute after you pass room number")
    #Change the state to ROOMS
    bot.state = ROOMS
#The final function. Get the user input about rooms, and pass it to the main() function to parse the data. 

@bot.message_handler(func=lambda msg:bot.state==ROOMS)
def get_title(message):
    data['rooms'] = int(message.text)
    res = main(data['city'], data['rooms'])
    bot.send_message(message.chat.id, res)
    bot.state = None
    print(data)
    print(res)

#start the bot
bot.polling()
