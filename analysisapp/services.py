from konlpy.tag import Mecab
from konlpy.utils import pprint
from analysisapp.tags import tag_dict
from hangul_romanize import Transliter
from hangul_romanize.rule import academic
import urllib.request
import itertools

GAS_URL = "https://script.google.com/macros/s/AKfycbxcmYsrbp-k8_sCsw6wKh2fTWXUQczj7X0VtmejmlGDykZCjS1lo_xTpY-gw2o-3vU/exec"

def analyze(text):
    mecab = Mecab()
    poslist = mecab.pos(text)
    res = {
      "text": text,
      "translation": translate(text),
      "romanized": romanize(text),
      "tokens": make_tokens(list(map(new_pos, poslist)), translate_tokens(poslist), poslist),
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
  print(text)
  return translate(text)

def translate(text):
    params = {
      "text": text,
      "source": "ko",
      "target": "ja"
    }
    req = urllib.request.Request('{}?{}'.format(GAS_URL, urllib.parse.urlencode(params)))
    res = urllib.request.urlopen(req).read()
    print(res.decode("UTF-8"))
    return res.decode("UTF-8")

def romanize(text):
    transliter = Transliter(academic)
    return transliter.translit(text)

def make_stem(token):
    if (token[1] in ["動詞", "形容詞"]):
        return token[0] + "다"

def make_tokens(token_list, trans_text, poslist):
    trans_list = trans_text.replace(",", "、").split("、")
    # print(trans_text)
    # print(trans_list)
    new_list = []
    for token, trans, pos in itertools.zip_longest(token_list, trans_list, poslist):
        new_list.append(
          {
            "token": token[0],
            "stem": make_stem(token),
            "romanized": romanize(token[0]),
            "translation": substitute_trans(trans, pos),
            "word_class": token[1]
          }
        )
    return new_list

def substitute_trans(trans, pos):
    # print(pos)
    if pos[1] == "J":
      if pos[0] == "도":
          return "も"
      if pos[0] == "이":
          return "が"
    if pos[1] == "JKS":
        return "が"
    if pos[1] == "JKO":
        return "を、に"
    if pos[1] == "XSN":
        if pos[0] == "들":
            return "たち"
    if pos[1] == "E":
        if pos[0] == "어서":
            return "〜てから"
        if pos[0] == "면":
            return "〜れば"
    if pos[1] == "XSA+ETN":
        return "〜であること、〜さ"
    if pos[1] == "XSA+ETM":
        return "〜な、〜である"
    if pos[0] == "못해":
        return "〜できない"
    return trans
