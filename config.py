#!/usr/bin/env python


frontier = "BreadthFirstGatherer"
store = "StoreToFSFolder"
responseHandler = {'LinkExtractor':10, 'StorePage':20}
#responseHandler = {'StorePage': 10}
requestHandler = {'Dummy':10}
#requestHandler = {'CheckRobots': 10}
#initialList = ["http://de.wikipedia.org/wiki/Terry_Pratchett.html", "http://de.wikipedia.org/wiki/Vereinigte_Staaten", "http://de.wikipedia.org/wiki/Sherlock_Holmes", "http://de.wikipedia.org/wiki/Donald_Trump", "http://de.wikipedia.org/wiki/Python_(Programmiersprache)","http://de.wikipedia.org/wiki/Linux"]
initialList = ["http://de.wikipedia.org/wiki/Terry_Pratchett.html"]
#initialList = ["http://de.search.yahoo.com/search"]
#Add functionality in frontier context
allowDuplicates = False
