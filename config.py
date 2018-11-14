#!/usr/bin/env python


frontier = "BreadthFirstGatherer"
store = "StoreToFilesystem"
responseHandler = {'LinkExtractor':10, 'StorePage':20}
#responseHandler = {'StorePage': 10}
requestHandler = {'CheckFiles': 20, 'CheckRobots': 10}
#requestHandler = {'CheckRobots': 10}
initialList = ["https://de.wikipedia.org/wiki/Terry_Pratchett", "https://de.wikipedia.org/wiki/Vereinigte_Staaten", "https://de.wikipedia.org/wiki/Sherlock_Holmes", "https://de.wikipedia.org/wiki/Donald_Trump", "https://de.wikipedia.org/wiki/Python_(Programmiersprache)","https://de.wikipedia.org/wiki/Linux"]
#initialList = ["https://de.search.yahoo.com/search"]
#Add functionality in frontier context
allowDuplicates = False
