import praw
import requests
import json

reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit("pythonforengineers")

keyphrase = '!worldfacts'

def do_something(comment):
        country = comment.body.replace(keyphrase, '')
        country = country.strip()
        response = requests.get('https://restcountries.eu/rest/v2/name/' + country)
        responseStr = ''
        if response.status_code == 404:
                responseStr += "I was unable to find a country matching your request. To use this bot, type !worldfacts [countryname]"
        else:
                text = response.text
                text = text[1:len(text) - 1]
                json_arr = json.loads(text)
                responseStr += 'Here are some facts about ' + country + '!\n\n\n'
                responseStr += 'Capital City: ' + json_arr['capital'] + '\n\n'
                responseStr += 'Population: ' + str(json_arr['population']) + '\n\n'
                currencies = ", ".join(str(currency['name']) for currency in json_arr['currencies'])
                responseStr += 'Currency: ' + currencies + "\n\n"
                languages = ", ".join(str(language['name']) for language in json_arr['languages'])
                responseStr += 'Languages: ' + languages + '\n\n'
                responseStr += '[National Flag](' + json_arr['flag'] + ')\n\n'
        comment.reply(responseStr)

for comment in subreddit.stream.comments():
        if comment.author.name != 'WorldFactsBot' and keyphrase in comment.body:
                do_something(comment)




