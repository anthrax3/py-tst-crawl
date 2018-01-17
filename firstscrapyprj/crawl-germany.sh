#!/bin/bash
# crawl-germany search_word city_Germany

if [ "$1" != "" ] 
then
	weblink="https://www.dastelefonbuch.de/Suche/"$1
	if [ "$2" != "" ]
	then
		weblink="https://www.dastelefonbuch.de/Suche/"$1"/"$2
	fi
	echo $weblink
	scrapy crawl -a url=$weblink germanyp_css
	
else
	echo "Script parameters is empty: first parameter - search word; second parameter - city"
	
fi	

# scrapy crawl -a url=www.dastelefonbuch.de/Suche/Auto/Stuttgart germanyp_css