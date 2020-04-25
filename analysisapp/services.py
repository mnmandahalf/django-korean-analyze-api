from konlpy.tag import Mecab
from konlpy.utils import pprint
from analysisapp.tags import tag_dict

def analyze(text):
    mecab = Mecab()
    poslist = mecab.pos(text)
    return map(new_pos, poslist)

def new_pos(pos):
    new_tag = tag_dict[pos[1]]
    return (pos[0], new_tag)