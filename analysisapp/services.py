from analysisapp.tags import tag_dict, trans_target, stem_target
from hangul_romanize import Transliter
from hangul_romanize.rule import academic
import urllib.request
import itertools
import mecab

GAS_URL = "https://script.google.com/macros/s/AKfycbxcmYsrbp-k8_sCsw6wKh2fTWXUQczj7X0VtmejmlGDykZCjS1lo_xTpY-gw2o-3vU/exec"

def analyze(raw_text):
    text = raw_text.replace(",", "")
    mecab_ = mecab.MeCab()
    mecab_poslist = mecab_.parse(text)
    res = {
      "text": raw_text,
      "translation": translate(raw_text),
      "romanized": romanize(text),
      "tokens": make_tokens(list(map(new_pos, mecab_poslist)), mecab_poslist),
    }
    return res

def new_pos(token):
    poslist = token[1].pos.split("+")
    new_tag_list = list(map(new_tag, poslist))
    return (token[0], "+".join(new_tag_list))

def new_tag(pos):
    return tag_dict[pos]

def token_list(pos):
    return pos[0]

def make_stem(token):
    expression = token[1].expression
    if expression:
        stem = expression.split("/")[0]
        return stem if token[1].pos.startswith("N") else stem + "다"

def make_suffix(token):
    expression = token[1].expression
    if expression:
        return expression.split("/")[2]

def translate_tokens(token):
    substitute = substitute_trans(token)
    if(substitute):
        return substitute
    if(token[1].pos in trans_target):
        return translate(token[0])
    for tgt in trans_target:
        if(tgt in token[1].pos):
            if token[1].pos.startswith("N"):
                return translate(make_stem(token))
            return translate(token[0])

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

def make_tokens(token_list, mecab_poslist):
    new_list = []
    for token, pos in itertools.zip_longest(token_list, mecab_poslist):
        new_list.append(
          {
            "token": token[0],
            "romanized": romanize(token[0]),
            "stem": make_stem(pos),
            "suffix": make_suffix(pos),
            "translation": translate_tokens(pos),
            "word_class": token[1]
          }
        )
    return new_list

def substitute_trans(token):
    char = token[0]
    pos = token[1].pos
    if pos[1] == "J":
      if char == "도":
          return "も"
      if char == "이":
          return "が"
    if pos == "JKS":
        return "が"
    if pos == "JKO":
        return "を、に"
    if pos == "JKG":
        return "の"
    if pos == "XSN":
        if char == "들":
            return "たち"
    if pos == "E":
        if char == "어서":
            return "〜てから"
        if char == "면":
            return "〜れば"
    if pos == "XSA+ETN":
        return "〜であること、〜さ"
    if pos == "XSA+ETM":
        return "〜な、〜である"
    if char == "못해":
        return "〜できない"
