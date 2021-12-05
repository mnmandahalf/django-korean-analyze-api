from konlpy.tag import Mecab
from konlpy.tag import Okt
from konlpy.utils import pprint
from analysisapp.tags import tag_dict, trans_target
from hangul_romanize import Transliter
from hangul_romanize.rule import academic
import urllib.request
import itertools

GAS_URL = "https://script.google.com/macros/s/AKfycbxcmYsrbp-k8_sCsw6wKh2fTWXUQczj7X0VtmejmlGDykZCjS1lo_xTpY-gw2o-3vU/exec"

def analyze(raw_text):
    text = raw_text.replace(",", "")
    mecab_poslist = Mecab().pos(text)
    print(mecab_poslist)
    res = {
      "text": raw_text,
      "translation": translate(raw_text),
      "romanized": romanize(text),
      "tokens": make_tokens(list(map(new_pos, mecab_poslist)), mecab_poslist),
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

def translate_tokens(pos):
    substitute = substitute_trans(pos) 
    if(substitute):
        return substitute
    if(pos[1] in trans_target):
        stem = make_stem(pos)
        text = stem if stem else pos[0]
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

def make_stem(pos):
    if (pos and pos[1] in ["VV", "VA", "XSA"]):
        oktpos = Okt().pos(pos[0], norm=False, stem=True)
        return oktpos[0][0]

def make_tokens(token_list, mecab_poslist):
    new_list = []
    for token, pos in itertools.zip_longest(token_list, mecab_poslist):
        new_list.append(
          {
            "token": token[0],
            "stem": make_stem(pos),
            "romanized": romanize(token[0]),
            "translation": translate_tokens(pos),
            "word_class": token[1]
          }
        )
    return new_list

def make_syntaxes(text):
    tanslation = translate(text.replace(" ", ","))
    new_list = []
    for word, trans in itertools.zip_longest(text.split(" "), tanslation.replace(",", "、").split("、")):
        new_list.append(
            {
                "word": word,
                "translation": trans
            }
        )
    print(new_list)
    return text

def substitute_trans(pos):
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
    if pos[1] == "JKG":
        return "の"
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
