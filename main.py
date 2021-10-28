import idiomcorpus
import nltk
nltk.download('punkt')
from mtranslate import translate
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from nltk.tokenize import word_tokenize
import enchant
d = enchant.Dict("en_US")

def perform_operation():
    object=idiomcorpus.Idiomcorpus()
    object.idiom_init(result)

    try:
        object.check_idiom()
        object.idiom_convert()
        object.idiom_display()

    except:
         print(" ")



master=input("Enter Hinglish text:")
print("***********Actual I/P***************")
print(master)

token = word_tokenize(master)
print("\n**************In a word******************")
for i in token:
    print(i, ": ", d.check(i))

result = transliterate(master, sanscript.ITRANS, sanscript.DEVANAGARI)
print("\n*****************Final ans********************")
print(result)

a = perform_operation()
