#lolbuddy
a cli tool to update league of legends itemsets and ability order from champion.gg

#Installation:

open Terminal
* ```git clone https://github.com/CyrusRoshan/lolbuddy.git```

#Usage:

First get a champion.gg API key from TSM at <a href="http://api.champion.gg">api.champion.gg</a>, then:

* Use ```lolbuddy``` to start lolbuddy and automatically fetch and create the item sets, which will be named "Champion.gg". If it is the first run and no API key or league installation location have been entered, you will be prompted for the API key, and lolbuddy will check the default league location for your OS. If it is not found, you will be prompted for that as well.
* Use ```lolbuddy -a [api key] -l [league install location]``` to change these settings if they happen to change (or are improperly entered the first time) and update the item sets/ability order.
  * for example, on OS X this could be: ```lolbuddy -a APIKEYHERE123 -l "/Applications/League\ of\ Legends.app"```

---

#License:
##MIT

