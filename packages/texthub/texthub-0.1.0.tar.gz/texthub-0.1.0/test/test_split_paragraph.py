"""
    測試劃分段落的各種方法
"""
from texthub.Text import Content
import pickle

def test_split_paragraphs_anti_indent():
    # 計算結果
    with open("example/anti-indent-paragraph.txt", "r", encoding="utf-8") as f:
        text = f.read()
    C = Content(text, paragraph_split_method="anti-indent")
    paragraph_list = C.split_paragraphs()
    # 讀取預期結果
    with open("expect/anti-indent-paragraph.pkl", "rb") as f:
        expect = pickle.load(f)
    # 對比是否相同
    assert paragraph_list == expect, "expect: {}, result: {}".format(expect, paragraph_list)
    
    
def test_split_paragraphs_line():
    # 計算結果
    with open("example/line-paragraph.txt", "r", encoding="utf-8") as f:
        text = f.read()
    C = Content(text, paragraph_split_method="line")
    paragraph_list = C.split_paragraphs()
    # 讀取預期結果
    with open("expect/line-paragraph.pkl", "rb") as f:
        expect = pickle.load(f)
    # 對比是否相同
    assert paragraph_list == expect, "expect: {}, result: {}".format(expect, paragraph_list)
    
def test_split_paragraphs_indent():
    # 計算結果
    with open("example/indent-paragraph.txt", "r", encoding="utf-8") as f:
        text = f.read()
    C = Content(text, paragraph_split_method="indent")
    paragraph_list = C.split_paragraphs()
    # 讀取預期結果
    with open("expect/indent-paragraph.pkl", "rb") as f:
        expect = pickle.load(f)
    # 對比是否相同
    assert paragraph_list == expect, "expect: {}, result: {}".format(expect, paragraph_list)
    
def test_split_paragraphs_none():
    # 計算結果
    with open("example/none-paragraph.txt", "r", encoding="utf-8") as f:
        text = f.read()
    C = Content(text, paragraph_split_method="none")
    paragraph_list = C.split_paragraphs()
    # 讀取預期結果
    with open("expect/none-paragraph.pkl", "rb") as f:
        expect = pickle.load(f)
    # 對比是否相同
    assert paragraph_list == expect, "expect: {}, result: {}".format(expect, paragraph_list)