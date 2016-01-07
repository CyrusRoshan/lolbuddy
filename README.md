#lolbuddy
a cli tool to update league of legends itemsets and ability order from champion.gg

lolbuddy automagically creates ingame item sets from the first items, final builds, and skill orders with the most games and highest win rates from champion.gg

#Installation:

As simple as ```pip3 install lolbuddy```

#Usage:

First get a champion.gg API key from TSM at <a href="http://api.champion.gg">api.champion.gg</a>, then:

Use ```lolbuddy``` to start lolbuddy and automatically fetch and create the item sets, which will be named by the role the item set is for.

If no API key or league installation location have been entered, or they are invalid, you will be prompted for the API key, and lolbuddy will check the default league location for your OS. If it is not found, you will be prompted for that as well.

Use ```lolbuddy -r``` or ```lolbuddy --reset``` to reset lolbuddy (delete info on league location and API key)

Use ```lolbuddy -d``` or ```lolbuddy --delete``` to delete all item sets

---

#License:
##MIT

