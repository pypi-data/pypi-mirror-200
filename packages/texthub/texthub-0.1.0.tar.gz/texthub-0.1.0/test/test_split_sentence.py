from texthub.Text import Paragraph
import pandas as pd

# 讀取sentence_list
with open("example/sentence_list.txt", "r", encoding="utf-8") as f:
    sentence_list = []
    for line in f:
        sentence_list.append(line.strip())
df = pd.DataFrame(sentence_list, columns=["sentence"])


def test_symbol():
    Ps = df["sentence"].apply(
        lambda x: Paragraph(x, sentence_split_method="symbol")
    )
    df["symbol"] = Ps.apply(lambda x: x.split_sentences())
    df["symbol_len"] = df["symbol"].apply(lambda x: len(x))
    
    with open("expect/symbol_sentences.pkl", "rb") as f:
        expect_df = pd.read_pickle(f)
    
    pd.testing.assert_frame_equal(df[["sentence", "symbol", "symbol_len"]], expect_df)
    
def test_length():
    Ps = df["sentence"].apply(
        lambda x: Paragraph(x, sentence_split_method="length")
    )
    df["length"] = Ps.apply(lambda x: x.split_sentences())
    df["length_len"] = df["length"].apply(lambda x: len(x))
    
    with open("expect/length_sentences.pkl", "rb") as f:
        expect_df = pd.read_pickle(f)
    
    pd.testing.assert_frame_equal(df[["sentence", "length", "length_len"]], expect_df)
    
def test_length_symbol():
    Ps = df["sentence"].apply(
        lambda x: Paragraph(x, sentence_split_method="length+symbol")
    )
    df["length+symbol"] = Ps.apply(lambda x: x.split_sentences())
    df["length+symbol_len"] = df["length+symbol"].apply(lambda x: len(x))
    
    with open("expect/length+symbol_sentences.pkl", "rb") as f:
        expect_df = pd.read_pickle(f)
    
    pd.testing.assert_frame_equal(df[["sentence", "length+symbol", "length+symbol_len"]], expect_df)
    
def test_model():
    Ps = df["sentence"].apply(
        lambda x: Paragraph(x, sentence_split_method="model")
    )
    df["model"] = Ps.apply(lambda x: x.split_sentences())
    df["model_len"] = df["model"].apply(lambda x: len(x))
    
    with open("expect/model_sentences.pkl", "rb") as f:
        expect_df = pd.read_pickle(f)
    
    pd.testing.assert_frame_equal(df[["sentence", "model", "model_len"]], expect_df)