import pyConTextNLP.pyConTextGraph as pyConText
import pyConTextNLP.itemData as itemData
import networkx as nx
import pyConTextNLP.helpers as helpers
from os import path
import re

reports = [
    """IMPRESSION: Evaluation limited by lack of IV contrast; however, no evidence of
      bowel obstruction or mass identified within the abdomen or pelvis. Non-specific interstitial opacities and bronchiectasis seen at the right
     base, suggestive of post-inflammatory changes.""",
    """IMPRESSION: Evidence of early pulmonary vascular congestion and interstitial edema. Probable scarring at the medial aspect of the right lung base, with no
     definite consolidation."""
    ,
    """IMPRESSION:

     1.  2.0 cm cyst of the right renal lower pole.  Otherwise, normal appearance
     of the right kidney with patent vasculature and no sonographic evidence of
     renal artery stenosis.
     2.  Surgically absent left kidney.""",
    """IMPRESSION:  No pneumothorax.""",
    """IMPRESSION: No definite pneumothorax""",
    """IMPRESSION:  New opacity at the left lower lobe consistent with pneumonia."""
]
# относительный адрес!
script_dir = path.dirname(__file__)
print(script_dir)

modifiers = itemData.instantiateFromCSVtoitemData(
    "file:///"+script_dir+"/lexical_rus.tsv")

targets = itemData.instantiateFromCSVtoitemData(
    "file:///"+script_dir+"/utah_rus.tsv")

# Example function to analyze each sentence
def markup_sentence(s, modifiers, targets, prune_inactive=True):
    """
    """
    markup = pyConText.ConTextMarkup()
    markup.setRawText(s)
    markup.cleanText()
    markup.markItems(modifiers, mode="modifier")
    markup.markItems(targets, mode="target")
    markup.pruneMarks()
    markup.dropMarks('Exclusion')
    # apply modifiers to any targets within the modifiers scope
    markup.applyModifiers()
    markup.pruneSelfModifyingRelationships()
    if prune_inactive:
        markup.dropInactiveModifiers()
    return markup

#for x in reports:
#    print(x)
#    print(markup_sentence(x,modifiers, targets, prune_inactive=True))
#    print("End --- \n")

# print(markup_sentence("Пациент не был болен тромбозом", modifiers, targets, prune_inactive=True))

filename = script_dir+"/definite_existence/1.txt"
with open(filename, encoding="utf8") as f:
    text = f.read()

sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)

for i in range(len(sentences)):
    print(markup_sentence(sentences[i], modifiers, targets, prune_inactive=True))