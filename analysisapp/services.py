from konlpy.tag import Mecab
from konlpy.utils import pprint
from analysisapp.tags import tag_dict
from hangul_romanize import Transliter
from hangul_romanize.rule import academic
import urllib.request

GAS_URL = "https://script.google.com/macros/s/AKfycbyZOEOeTmftFoh4vO1hmLO7JNkiWOKOMarrACMS4YLz8Dnk2o0/exec"

def analyze(text):
    mecab = Mecab()
    poslist = mecab.pos(text)
    res = {
      "text": text,
      "translation": translate(text),
      "tokens_translation": translate_tokens(poslist),
      "romanized": romanize(text),
      "tokens": list(map(new_pos, poslist)),
    }
    return res

def new_pos(pos):
    new_tag = tag_dict[pos[1]]
    return (pos[0], new_tag)

def token_list(pos):
    return pos[0]

def translate_tokens(poslist):
  tokens = list(map(token_list, poslist))
  text = ",".join(tokens)
  return translate(text)

def translate(text):
    params = {
      "text": text,
      "source": "ko",
      "target": "ja"
    }
    req = urllib.request.Request('{}?{}'.format(GAS_URL, urllib.parse.urlencode(params)))
    res = urllib.request.urlopen(req).read()
    return res.decode("UTF-8")

def romanize(text):
    transliter = Transliter(academic)
    return transliter.translit(text)