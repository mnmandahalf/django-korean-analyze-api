from konlpy.tag import Mecab
from konlpy.utils import pprint
from analysisapp.tags import tag_dict
from hangul_romanize import Transliter
from hangul_romanize.rule import academic
import urllib.request

GAS_URL = "https://script.google.com/macros/s/AKfycbxcmYsrbp-k8_sCsw6wKh2fTWXUQczj7X0VtmejmlGDykZCjS1lo_xTpY-gw2o-3vU/exec"

def analyze(text):
    mecab = Mecab()
    poslist = mecab.pos(text)
    res = {
      "text": text,
      "translation": translate(text),
      "romanized": romanize(text),
      "tokens": make_tokens(list(map(new_pos, poslist)), translate_tokens(poslist)),
    }
    return res

def new_pos(pos):
    poslist = pos[1].split("+")
    new_tag_list =list(map(new_tag, poslist))
    return (pos[0], "+".join(new_tag_list))

def new_tag(pos):
    return tag_dict[pos]

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

def make_stem(token):
    if (token[1] in ["動詞", "形容詞"]):
        return token[0] + "다"

def make_tokens(token_list, trans_text):
    trans_lint = trans_text.replace(",", "、").split("、")
    new_list = []
    for token, trans in zip(token_list, trans_lint):
        new_list.append(
          {
            "token": token[0],
            "stem": make_stem(token),
            "romanized": romanize(token[0]),
            "translation": trans,
            "word_class": token[1]
          }
        )
    return new_list
