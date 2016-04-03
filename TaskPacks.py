
from Tools import *

taskPacks = [{
    "Title": "Repeat task pack",
    "ExtractMethod": "repeatTask",
    "RegularExpression": "(\w*)\s+times",
    "SentenceComponents": [{
        "Name": "Counter",
        "IsRequired": True
    }]
}, {
    "Title": "Finder",
    "ExtractMethod": "findTask",
    "RegularExpression": "find\s+(last|new|final)*([\w\d\s]*)",
    "SentenceComponents": [{
        "Name": "Order",
        "IsRequired": False
    }, {
        "Name": "ItemName",
        "IsRequired": True
    }]
}]

standartSentenceComponents = [{
    "Name": "Attendant",
    "IsRequired": True
}, {
    "Name": "Verb",
    "IsRequired": True
}, {
    "Name": "Objects",
    "IsRequired": False
}]

synonyms = [{
    "kodi": ["cody"]
}]

attendants = ["kodi", "pi"]
verbs = ["play", "search", "next", "stop"]