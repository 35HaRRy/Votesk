
standartSentenceComponents = [{
    "Name": "Attendant",
    "IsRequired": True
},{
    "Name": "Verb",
    "IsRequired": True
},{
    "Name": "Objects",
    "IsRequired": False
}]

tasks = [{
    "Title": "Stop background listener",
    "IntentMethod": "workOnPi",
    "RegularExpression": "(pi)\s+(\w*)\s*([\w\d\s]*)",
    "SentenceComponents": standartSentenceComponents
}, {
    "Title": "Kodi dispatcher",
    "IntentMethod": "workOnKodi",
    "RegularExpression": "(kodi)\s+(\w*)\s*([\w\d\s]*)",
    "SentenceComponents": standartSentenceComponents
}]

attendants = ["kodi", "pi"]
verbs = ["play", "search", "next", "stop"]

synonyms = [{
    "kodi": ["cody"]
}]