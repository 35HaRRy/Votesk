
from TaskPacks import *

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

def matchTextToComponents(text, pairs):
    isMatched = False

    for synonym in synonyms:
        for key, values in synonym.iteritems():
            for value in values:
                text = text.replace(value, key)

    for pair in pairs:
        p = re.compile(pair["RegularExpression"])
        matches = p.match(text)

        if not matches == None:
            matches = matches.groups()

            assert len(matches) >= len(filter(lambda x: x["IsRequired"], pair["SentenceComponents"])), "Need all required components"

            for i in range(0, len(pair["SentenceComponents"]), 1):
                component = pair["SentenceComponents"][i]

                pair[component["Name"]] = ""
                if i < len(matches):
                    pair[component["Name"]] = matches[i]
                    isMatched = True
            break

    if isMatched == True:
        return pair
    else:
        return {}