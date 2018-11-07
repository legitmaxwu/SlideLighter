
import operator
import six
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../My First Project-0251e42aed7f.json"



def GenerateMap(dict):
    conceptString = ""
    for concept in dict:
        for _ in range(dict[concept]):
            conceptString += concept + " "

    return entities_text(conceptString.lower())

def entities_text(text):
    from google.cloud import language
    from google.cloud.language import enums
    from google.cloud.language import types
    outDict = {}
    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities


    for entity in entities:
        outDict[entity.name] = outDict.get(entity.name,0) + 1

    lst = []

    for a in outDict:
        lst.append((a,outDict[a]))
    lst.sort(key = lambda x: -x[1])  
    return lst
    
