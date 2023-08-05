"""
    測試各種外部模組是否能正常執行
"""

def test_import():
    import importlib
    # 開啟module_list.txt檔案，讀取模組名稱
    with open("module_list.txt", "r", encoding="utf-8") as f:
        module_list = f.read().splitlines()
    
    for module_name in module_list:
        try:
            importlib.import_module(module_name)
        except ImportError:
            raise ImportError(f"{module_name} 模組無法匯入")
    
    

def test_punctuators():
    """
        測試 punctuators 模組是否能正常運作
    """
    from punctuators.models import PunctCapSegModelONNX
    m = PunctCapSegModelONNX.from_pretrained("pcs_47lang")
    input_texts = [
    "hola mundo cómo estás estamos bajo el sol y hace mucho calor santa coloma abre los huertos urbanos a las escuelas de la ciudad",
    "hello friend how's it going it's snowing outside right now in connecticut a large storm is moving in",
    "未來疫苗將有望覆蓋3歲以上全年齡段美國與北約軍隊已全部撤離還有鐵路公路在內的各項基建的來源都將枯竭",
    "በባለፈው ሳምንት ኢትዮጵያ ከሶማሊያ 3 ሺህ ወታደሮቿንም እንዳስወጣች የሶማሊያው ዳልሳን ሬድዮ ዘግቦ ነበር ጸጥታ ሃይሉና ህዝቡ ተቀናጅቶ በመስራቱ በመዲናዋ ላይ የታቀደው የጥፋት ሴራ ከሽፏል",
    "all human beings are born free and equal in dignity and rights they are endowed with reason and conscience and should act towards one another in a spirit of brotherhood",
    "सभी मनुष्य जन्म से मर्यादा और अधिकारों में स्वतंत्र और समान होते हैं वे तर्क और विवेक से संपन्न हैं तथा उन्हें भ्रातृत्व की भावना से परस्पर के प्रति कार्य करना चाहिए",
    "wszyscy ludzie rodzą się wolni i równi pod względem swej godności i swych praw są oni obdarzeni rozumem i sumieniem i powinni postępować wobec innych w duchu braterstwa",
    "tous les êtres humains naissent libres et égaux en dignité et en droits ils sont doués de raison et de conscience et doivent agir les uns envers les autres dans un esprit de fraternité",
    ]
    results= m.infer(input_texts)
    for input_text, output_texts in zip(input_texts, results):
        print(f"Input: {input_text}")
        print("Outputs:")
        for text in output_texts:
            print(f"\t{text}")
        print()
        
def test_transformers():
    from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

    tokenizer = AutoTokenizer.from_pretrained("IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment")
    model = AutoModelForSequenceClassification.from_pretrained("IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment")
    classifier = TextClassificationPipeline(model=model, tokenizer=tokenizer)
    result = classifier("今天天氣真好")
    print(result)