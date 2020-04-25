from konlpy.tag import Mecab
from konlpy.utils import pprint
from analysisapp.tags import tag_dict
from hangul_romanize import Transliter
from hangul_romanize.rule import academic

def analyze(text):
    mecab = Mecab()
    poslist = mecab.pos(text)
    res = {
      "text": text,
      "translation": translate(text),
      "romanized": romanize(text),
      "tokens": list(map(new_pos, poslist)),
    }
    return res

def new_pos(pos):
    new_tag = tag_dict[pos[1]]
    return (pos[0], new_tag)

def translate(text):
    return "日本語訳"

def romanize(text):
    transliter = Transliter(academic)
    return transliter.translit(text)