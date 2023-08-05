"""


"""
import pandas as pd

RE_TABLE = {
    ".": "<re_dot>",
    "^": "<re_head>",
    "$": "<re_dollor>",
    "*": "<re_star>",
    "+": "<re_plus>",
    "?": "<re_question>",
    "{": "<re_bracket_L3>",
    "}": "<re_bracket_R3>",
    "[": "<re_bracket_L2>",
    "]": "<re_bracket_R2>",
    "(": "<re_bracket_L1>",
    ")": "<re_bracket_R1>",
    "|": "<re_or>",
    "&": "<re_and>",
    ":": "<re_colon>",
    "=": "<re_equal>",
    "-": "<re_minus>",
}

def re_replace(text,inverse=False):
    from bidict import bidict
    # 選擇取代表
    if inverse == False:
        re_table = RE_TABLE
    else:
        re_table = dict(bidict(RE_TABLE).inverse)

    # 取代所有元素
    for key in re_table.keys():
        text = text.replace(key, re_table[key])
    return text
#%%
from punctuators.models import PunctCapSegModelONNX

segmenter = PunctCapSegModelONNX.from_pretrained("pcs_47lang")


#%%
class Content:
    """
        Content為整篇文章的内容，一個Content會具有以下屬性：
            - content: 文章的內容
            - paragraph_split_method: 段落分割方法
            - title: 文章的標題
            - text_ID: 文章的ID
            - df_sentence: 文章的句子列表
                - paragraph_index: 段落編號
                - sentence_index: 句子編號
                - sentence: 句子內容
                - label1: 句子的第一個標籤
                - label2: 句子的第二個標籤
                - ...
        可以拆分成多個Paragraph
        支持不同的段落分割方式
            - 換行即為段落
            - 縮排為一個新的段落
            - 縮排為前一個段落的一部分
            - 使用openai的API來分割段落
        支持段落regex過濾
    """
    def __init__(self, content, 
                 paragraph_split_method="line", 
                 title="Content", text_ID=None,
                 paragraph_filter_regex=None,
                 **kwargs): # 支援往下傳遞的參數
        #* 檢查參數
        if not content:
            raise ValueError("The 'content' parameter cannot be empty.")
        if not isinstance(content, str):
            raise TypeError("The 'content' parameter must be a string.")
        
        #* 參數設定 
        self.paragraph_split_method = paragraph_split_method # 段落分割方法
        self.title = title # 文章的標題
        self.paragraph_filter_regex = paragraph_filter_regex
        # 如果沒有指定ID，則使用文章的內容的MD5值作為ID
        if text_ID is None:
            import hashlib
            self.text_ID = hashlib.md5(content.encode("utf-8")).hexdigest()
        else:
            self.text_ID = text_ID
        
        #* 初始化
        #! self.content = re_replace(content) # 前處理去除特殊符號
        self.content = content
        paragraph_list = self.split_paragraphs() # 段落列表
        
        # 過濾段落
        if self.paragraph_filter_regex is not None and self.paragraph_filter_regex != "":
            paragraph_list = self.paragraph_filter(paragraph_list)
            
        # 將每個段落轉換成Paragraph類型的物件，加上段落編號為ID
        self.Paragraph_list = [Paragraph(paragraph, paragraph_index=i+1, **kwargs) for i, paragraph in enumerate(paragraph_list)]
        #// self.Paragraph_list = [Paragraph(paragraph, **kwargs) for paragraph in paragraph_list]
        
        #* 初始化df_sentence
        # 將每個段落的df_sentence合併成一個大的df_sentence, 並加上段落ID
        df_sentence_list = [P.df_sentence.assign(paragraph_index=P.paragraph_index) for P in self.Paragraph_list]
        self.df_sentence = pd.concat(df_sentence_list, ignore_index=True)
        # 合併段落編號和句子編號，形成index
        self.df_sentence["index"] = self.df_sentence.apply(lambda row: str(row["paragraph_index"]) + "-" + str(row["sentence_index"]), axis=1)
        # 移除paragraph_index和sentence_index
        self.df_sentence = self.df_sentence.drop(["paragraph_index", "sentence_index"], axis=1)
        # 重設column順序：index、paragraph_abstract、sentence、label1、label2、...
        self.df_sentence = self.df_sentence[["index", "paragraph_abstract", "sentence"] + [col for col in self.df_sentence.columns if col not in ["index", "paragraph_abstract", "sentence"]]]
        
    def split_paragraphs(self):
        """
            拆分段落
        """
        if self.paragraph_split_method == "openai":
            return self.split_paragraphs_openai()
        elif self.paragraph_split_method == "line":
            return self.split_paragraphs_line()
        elif self.paragraph_split_method == "indent":
            return self.split_paragraphs_indent()
        elif self.paragraph_split_method == "anti-indent":
            return self.split_paragraphs_anti_indent()
        elif self.paragraph_split_method == "none":
            return self.split_paragraphs_none()
        else:
            raise ValueError("paragraph_split_method must be one of ['openai','line','indent','anti-indent']")
        
    def split_paragraphs_openai(self):
        """
            使用openai的API來分割段落
        """
        # 開發中，暫時不支持
        raise NotImplementedError("split_paragraphs_openai is not implemented yet")
    
    def split_paragraphs_line(self):
        """
            換行即為段落
        """
        # 拆分段落
        line_list = self.content.split("\n")
        # 去除每一行裡面的空白
        line_list = [line.strip() for line in line_list]
        # 去除空白行
        paragraph_list = [line for line in line_list if line != ""]
        return paragraph_list
        
        
    def split_paragraphs_indent(self):
        """
            縮排為一個新的段落
        """
        import re
        # 拆分段落
        line_list = self.content.split("\n")
        paragraph_list = []
        # 用一個迴圈來處理每行
        # 若該行為縮排，作為一個新的段落
        # 若該行不為縮排，則加入前一個段落
        paragraph_one = ""
        for line in line_list:
            # 若為縮排，則作為一個新的段落    
            if re.match(r"^\s+", line):
                paragraph_list.append(paragraph_one)
                paragraph_one = line.strip()
            else: # 若不為縮排，則加入前一個段落
                paragraph_one += line.strip()
        paragraph_list.append(paragraph_one)
        # 去除空白段落
        paragraph_list = [paragraph for paragraph in paragraph_list if paragraph != ""]
        return paragraph_list
                
            
    def split_paragraphs_anti_indent(self):
        """
            縮排為前一個段落的一部分
        """
        import re
        # 拆分段落
        line_list = self.content.split("\n")
        paragraph_list = []
        # 用一個迴圈來處理每行
        # 若該行為縮排，則加入前一個段落
        # 若該行不為縮排，作為一個新的段落
        paragraph_buffer = ""
        for line in line_list:
            
            # 若為縮排，則加入前一個段落
            if re.match(r"^\s+", line):
                paragraph_buffer += line.strip()
            else: # 若不為縮排，則作為一個新的段落
                paragraph_list.append(paragraph_buffer)
                paragraph_buffer = line.strip()
        paragraph_list.append(paragraph_buffer) # 最後一個段落
        # 去除空白段落
        paragraph_list = [paragraph for paragraph in paragraph_list if paragraph != ""]
        return paragraph_list
    
    def split_paragraphs_none(self):
        """
            不拆分段落
        """
        # 清理所有的換行和空白
        paragraph_list = [self.content.replace("\n", " ").replace(" ", "").strip()]
        return paragraph_list
    
    
    def paragraph_filter(self, paragraph_list):
        import re
        new_paragraph_list = []
        for paragraph in paragraph_list:
            matches = re.finditer(self.paragraph_filter_regex, paragraph, re.MULTILINE)
            for match in matches:
                if match.group() != "":
                    new_paragraph_list.append(match.group())
        return new_paragraph_list
        
    
    def predict(self):
        _ = [P.predict() for P in self.Paragraph_list]
        df_sentence_list = [P.df_sentence.assign(paragraph_index=P.paragraph_index) for P in self.Paragraph_list]
        self.df_sentence = pd.concat(df_sentence_list, ignore_index=True)
        # 合併段落編號和句子編號，形成index
        self.df_sentence["index"] = self.df_sentence.apply(lambda row: str(row["paragraph_index"]) + "-" + str(row["sentence_index"]), axis=1)
        # 移除paragraph_index和sentence_index
        self.df_sentence = self.df_sentence.drop(["paragraph_index", "sentence_index"], axis=1)
        # 重設column順序：index、paragraph_abstract、sentence、label1、label2、...
        self.df_sentence = self.df_sentence[["index", "paragraph_abstract", "sentence"] + [col for col in self.df_sentence.columns if col not in ["index", "paragraph_abstract", "sentence"]]]
        return self.df_sentence
class Paragraph:
    """
        Paragraph為文章的一個段落，一個Paragraph會包含以下資訊
            - paragraph: 段落的內容
            - sentence_split_method: 句子分割方法
            - paragraph_index: 段落的ID
            - df_sentence: 句子的DataFrame，包含以下欄位
                - sentence_index: 句子的ID
                - sentence: 句子的內容
                - label1: 句子的第一個標籤
                - label2: 句子的第二個標籤
                - ...
        可以拆分成多個Sentence
        支持不同句子分割方式
            - 使用符號分割，如句號、問號、感嘆號
            - 使用長度分割，如每個句子長度不超過20個字
            - 使用openai的API來分割段落
    """
    def __init__(self, paragraph, sentence_split_method="length", paragraph_index=0, **kwargs):
        #* 檢查參數
        if not isinstance(paragraph, str):
            raise TypeError("paragraph must be a string")
        if not isinstance(paragraph_index, int):
            raise TypeError("paragraph_index must be an integer")
        
        #* 初始化
        self.paragraph = paragraph
        self.paragraph_abstract = paragraph[:15] # 取前15個字當作摘要
        self.sentence_split_method = sentence_split_method
        self.paragraph_index = paragraph_index
        sentence_list = self.split_sentences()
        
        #* 初始化Sentence
        # 將每個句子轉換成Sentence類型的物件，加上句子編號為ID
        self.Sentence_list = [Sentence(sentence, sentence_index=i+1, **kwargs) for i, sentence in enumerate(sentence_list)]
        
        #* 初始化df_sentence
        model_list = kwargs.get("model_list", [])
        self.model_name_list = [model.model_name for model in model_list]
        self.df_sentence = pd.DataFrame(
            columns = ["sentence_index", "sentence"] + self.model_name_list
        )
        self.df_sentence["sentence_index"] = [S.sentence_index for S in self.Sentence_list]
        self.df_sentence["sentence"] = [S.sentence for S in self.Sentence_list]
        self.df_sentence["paragraph_abstract"] = self.paragraph_abstract
        for model_name in self.model_name_list:
            self.df_sentence[model_name] = [S.tags[model_name] for S in self.Sentence_list]
        
    def split_sentences(self):
        """
            拆分句子
        """
        if self.sentence_split_method == "model":
            return self.split_sentences_model()
        elif self.sentence_split_method == "symbol":
            return self.split_sentences_symbol()
        elif self.sentence_split_method == "length":
            return self.split_sentences_length()
        elif self.sentence_split_method == "length+symbol":
            return self.split_sentences_length_symbol()
        else:
            raise ValueError("sentence_split_method must be one of ['model','symbol','length', 'length+symbol']")
        
    def split_sentences_model(self):
        """
            使用model來分割句子:
        """
        return segmenter.infer([self.paragraph])[0]
    
    def split_sentences_symbol(self):
        """
            只使用符號分割句子
        """
        import re
        # 拆分句子
        sentence_list = re.split(r"([。？！])", self.paragraph) # 用符號分割句子
        sentence_list = ["".join(sentence_list[i:i+2]) for i in range(0, len(sentence_list), 2)] # 每2個元素為一個句子，保留符號
        # 去除每一句裡面的空白
        sentence_list = [sentence.strip() for sentence in sentence_list]
        # 去除空白句子
        sentence_list = [sentence for sentence in sentence_list if sentence != ""]
        return sentence_list
    
    def split_sentences_length(self, max_length=50):
        """
            使用長度分割句子
        """
        # 將句子分割成每個句子長度不超過max_length
        sentence_list = []
        sentence_buffer = ""
        for word in self.paragraph:
            # 若句子長度不超過max_length，則加入前一個句子
            if len(sentence_buffer) + len(word) <= max_length:
                sentence_buffer += word
            # 若句子長度超過max_length，則加入sentence_list
            else:
                sentence_list.append(sentence_buffer)
                sentence_buffer = word
        # 將最後一個句子加入sentence_list
        sentence_list.append(sentence_buffer)
        return sentence_list
        
    
    def split_sentences_length_symbol(self, max_length=50):
        """
            使用長度優先+符號輔助分割句子
        """
        import re
        # 用任何符號分割句子
        sub_sentence_list = re.split(r"([。？！、；,」\.])", self.paragraph)
        # 將不超過max_length的句子合併
        sentence_list = []
        sub_sentence_buffer = "" 
        for sub_sentence in sub_sentence_list:
            # 若句子只有1個字，加入前一個句子
            if len(sub_sentence) <= 1:
                sub_sentence_buffer += sub_sentence
            # 若句子長度不超過max_length，則加入前一個句子
            elif len(sub_sentence_buffer) + len(sub_sentence) <= max_length:
                sub_sentence_buffer += sub_sentence
            else: # 若句子長度超過max_length，則作為一個新的句子
                sentence_list.append(sub_sentence_buffer)
                sub_sentence_buffer = sub_sentence
        sentence_list.append(sub_sentence_buffer) # 最後一個句子
        sentence_list = [s for s in sentence_list if s != ""] # 去除空白句子
        return sentence_list
    
    def predict(self):
        _ = [S.predict() for S in self.Sentence_list]
        for model_name in self.model_name_list:
            self.df_sentence[model_name] = [S.tags[model_name] for S in self.Sentence_list]
        return self.df_sentence
    

class Sentence:
    """
        Sentence為段落的一個句子，在目前系統中為最小單位
        每個句子會針對不同的判斷模型，有不同的tag
    """
    def __init__(self, sentence, sentence_index=0, model_list=[]):
        #* 檢查參數
        if not isinstance(sentence, str):
            raise TypeError("sentence must be a string")
        if not isinstance(sentence_index, int):
            raise TypeError("sentence_index must be an integer")
        
        #* 初始化
        self.sentence = sentence
        self.sentence_index = sentence_index
        self.model_list = model_list
        self.tags = {}
        for model in model_list:
            self.tags[model.model_name] = None
        
    
    def predict(self):
        """
            使用不同的模型來預測句子的tag
        """
        for model in self.model_list:
            result = model.predict(self.sentence)[0]
            self.tags[model.model_name] = result.get("label")
            self.tags[model.model_name + "_score"] = result.get("score")
        return self.tags
    