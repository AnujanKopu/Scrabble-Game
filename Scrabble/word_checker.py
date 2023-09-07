import enchant 
import PyDictionary 
from PyDictionary import PyDictionary


class WordChecker():

    def __init__(self):
        self.enchant_dict = enchant.Dict("en_US")
        self.py_dictionary=PyDictionary()
        with open('./Scrabble/twl_words.txt','r') as twl_words:
            self.twl_dict:set = set([line.replace('\n','') for line in twl_words.readlines()])

    def check(self,word:str) -> tuple[bool,str]:
        word = word.lower()
        if "_" in word: 
            if word.count("_") == 1:
                for i in range(97,122):
                    if self._word_check(word.replace('_',chr(i))):  
                        word = word.replace('_',chr(i))
                        break
                else: return (False,word)

                return (True,word,self.py_dictionary.meaning(word,disable_errors=True))
            else:
                for i in range(97,122):
                    for j in range(97,122):
                        if self._word_check(word.replace('_',chr(i),1).replace('_',chr(j))):  
                            word = word.replace('_',chr(i),1).replace('_',chr(j))
                            break
                    if self._word_check(word):
                        break
                else: return (False,word)
                return (True,word,self.py_dictionary.meaning(word,disable_errors=True))
        else:   
            if self._word_check(word) is False: return (False,word)
            else: return (True,word,self.py_dictionary.meaning(word,disable_errors=True))

    
    def _word_check(self,word):
        return self.enchant_dict.check(word) or word in self.twl_dict #self.enchant_dict.check(word.capitalize()) or word in self.twl_dict
