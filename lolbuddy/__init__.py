#!/usr/bin/env python3
import json
from requests_futures.sessions import FuturesSession
import sys
import os
import pickle
from copy import deepcopy
import shutil
# import pprint # pprint used for debug, doesn't need to be used for production
# pp = pprint.PrettyPrinter(indent=4)

def main():

    if ('--reset' in sys.argv or '-r' in sys.argv):
        try:
            os.remove('.lolbuddy')
        except:
            print('\nThere was no existing config file, could not delete nonexistent file. Exiting...\n')
        sys.exit("Exiting after an attempted reset")

    if ('--delete' in sys.argv or '-d' in sys.argv):
        try:
            data = pickle.load(open('.lolbuddy', 'rb'))
            shutil.rmtree(data['location'] + '/Champions')
        except:
            print('\nLeague install location data wasn\'t stored, could not delete item sets. Exiting...\n')
        sys.exit("Exiting after an attempted data deletion")

    # don't want to write to file if we don't need to
    writeToFile = False

    try:
        data = pickle.load(open('.lolbuddy', 'rb'))
        location = data['location']
        apiKey = data['apiKey']
    except:
        writeToFile = True
        data = {'location': '', 'apiKey': ''}
        location = ''
        apiKey = ''

    # Check if the .lolbuddy file either doesn't have the location saved or doesn't have the correct location saved
    if (location == '' or not os.path.exists(location)):
        # otherwise, check if the location is one of the defaults for the OS
        writeLocation = True
        if os.name == 'posix': # OS X
            location = '/Applications/League of Legends.app/Contents/LoL/Config'
        elif os.name == 'nt': # Windows
            location = 'C:/Riot Games/League of Legends/Config'
        else: # Linux
            print('\nSorry, linux is not supported...\n')
            quit()
        # If the location path STILL isn't correct, prompt the user for the correct path
        while not os.path.exists(location):
            writeLocation = True
            location = input('Could not find location of league config folder, please enter it here. It should look something like this "C:/Riot Games/League of Legends/Config" or "/Applications/League of Legends.app/Contents/LoL/Config":\n')

    # if the API key isn't saved or clearly too short to be a champion.gg API key
    if len(apiKey) < 20: # assuming consistency, champion.gg's is 32 chars
        writeToFile = True
        # keep prompting user until they get it right
        while len(apiKey) < 20:
            apiKey = input('Please enter a valid API key from api.champion.gg: ')

    if writeToFile:
        data = {'location': location, 'apiKey': apiKey}
        pickle.dump(data, open('.lolbuddy', 'wb'))

    session = FuturesSession()

    print('\nGetting champion info...')

    apiKeyValidated = False
    while not apiKeyValidated:
        url = 'http://api.champion.gg/champion?api_key=' + apiKey
        infoRequest = session.get(url) # start request
        requestData = infoRequest.result().content.decode('utf-8') # finish request
        try:
            champions = json.loads(requestData)
            apiKeyValidated = True
        except:
            apiKey = input('Seems like the API key didn\'t work, please enter a valid API key: ')
            data['apiKey'] = apiKey
            pickle.dump(data, open('.lolbuddy', 'wb'))
    totalChampions = len(champions)
    championsComplete = 0
    championInfo = []

    print('\nThere are currently {0} champions. Getting individual champion data...'.format(totalChampions))

    def incrementChamps(sess, resp):
        nonlocal championsComplete, championInfo
        championsComplete += 1
        champion = resp.content.decode('utf-8')
        try:
            championJson = json.loads(champion)
            championInfo.append(championJson)
        except:
            print('Error while attempting to fetch champion {0}'.format(championsComplete))

    for champion in champions:
        url = 'http://api.champion.gg/champion/' + champion['key'] + '?&api_key=' + apiKey
        championData = session.get(url, background_callback=incrementChamps)

    while championsComplete < totalChampions:
        print('({0}/{1}) champions complete...'.format(championsComplete, totalChampions), end='\r')
        sys.stdout.flush()

    print('\nAll champion data fetched, removing previous item sets...')

    championsComplete = 0
    shutil.rmtree(location + '/Champions')

    print('Previous item sets deleted, creating new item sets...\n')

    for champion in championInfo:
        champFolder = os.path.join(location, 'Champions', champion[0]['key'], 'Recommended')
        if not os.path.exists(champFolder):
            os.makedirs(champFolder)

        for roleNum, role in enumerate(champion):
            try:
                jsonFile = {
                    'title': role['role'],
                    'type': 'custom',
                    'map': 'SR',
                    'mode': 'CLASSIC',
                    'priority': True,
                    'sortrank': 0,
                    'blocks': []
                }

                itemList = lambda listName: deepcopy({
                    'type': listName,
                    'recMath': False,
                    'minSummonerLevel': -1,
                    'maxSummonerLevel': -1,
                    'showIfSummonerSpell': '',
                    'hideIfSummonerSpell': '',
                    'items': []
                })

                highestWin = itemList('Highest Win %: ')
                highestPlay = itemList('Most Popular: ')


                # for skill order (goes in title)
                for skill in role['skills']['highestWinPercent']['order']:
                    highestWin['type'] += skill + '>'
                highestWin['type'] = highestWin['type'][:-1]

                for skill in role['skills']['mostGames']['order']:
                    highestPlay['type'] += skill + '>'
                highestPlay['type'] = highestPlay['type'][:-1]

                def insertItems(oldArray, newArray):
                    for item in oldArray:
                        # item id 2010 is for total biscuits, which cannot be bought in the shop and do not
                        # show up if put in itemsets, so we switch to pots instead
                        if (item['id'] == '2003'):
                            newArray.append({'id': '2010', 'count': 1})
                        else:
                            newArray.append({'id': '{0}'.format(item['id']), 'count': 1})

                # for first items
                insertItems(role['firstItems']['highestWinPercent']['items'], highestWin['items'])
                insertItems(role['firstItems']['mostGames']['items'], highestPlay['items'])

                # for full build
                insertItems(role['items']['highestWinPercent']['items'], highestWin['items'])
                insertItems(role['items']['mostGames']['items'], highestPlay['items'])

                # for trinkets
                highestWinTrinket = {'games': 0, 'winPercent': 0}
                highestPlayTrinket = {'games': 0, 'winPercent': 0}

                for trinket in role['trinkets']:
                    if trinket['games'] > highestPlayTrinket['games']:
                        highestPlayTrinket = trinket
                    if trinket['winPercent'] > highestWinTrinket['winPercent']:
                        highestWinTrinket = trinket

                highestWin['items'].append({'id': '{0}'.format(highestWinTrinket['item']['id']), 'count': 1})
                highestPlay['items'].append({'id': '{0}'.format(highestPlayTrinket['item']['id']), 'count': 1})

                # add item sublists to json object with item list info
                jsonFile['blocks'].extend([highestWin, highestPlay])

                # save the json file to the champion's folder
                itemSetFile = open('{0}/championgg{1}.json'.format(champFolder, roleNum + 1), 'w+')
                itemSetFile.write(json.dumps(jsonFile))

            except:
                # e.g. for when champion.gg's API would serve empty item sets for some champion roles (e.g. Morde mid, Galio supp)
                print('\nSomething went wrong when saving item lists for {0} {1}...'.format(champion[0]['key'], role['role']))

        championsComplete += 1

    print('\nAll Done! Your item sets are ready!\n\n')


if __name__ == '__main__':
    main()
