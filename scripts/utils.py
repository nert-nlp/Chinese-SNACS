import io, os, re

chinese_punctuations = ["。", "，", "？", "！", "”", "“", "：", "…"]

xpos2lexcat_dict = {
"AD":"ADV", # adverb	也
"AS": "AUX", # aspect marker	着
"BA": "BA", # 把 in ba-construction	把
"CC": "CCONJ", # coordinating conjunction	和
"CD": "NUM", #  cardinal number	一百
"CS": "SCONJ", # subordinating conjunction	虽然
"DEC": "DE", # 的 in a relative-clause	的
"DEG": "DE", # associative	的
"DER": "DE",	# in V-de const. and V-de-R	得
"DEV":	"DE", # 地 before VP	地
"DT": "DET", # determiner	这
"ETC": "N", # for words 等, 等等	等, 等等
"FW": "X", # foreign words	A
"IJ": "INTJ", # interjection	哈哈
"JJ": "ADJ", # other noun-modifer	新
"LB": "LB",	# 被 in long bei-const	被
"LC": "LC", # localizer	里
"M": "N", # measure word	个
"MSP": "PART", # other particle	所
"NN": "N", # common noun	工作
"NR": "N", # proper noun	中国
"NT": "N", # temporal noun	目前
"OD": "NUM", # ordinal number	第一
"ON": "N", #	onomatopoeia
"P": "P", # Prepositions (excluding 把 and 被)	在
"PN": "PRON", # pronoun	我
"PU": "PUNCT", # punctuation	标点
"SB": "V",	# 被 in short bei-const	被+V
"SP": "PART", # sentence-final particle	吗
"VA": "V", #	predicative adjective	好
"VC": "V", #		copula	是
"VE": "V", #		有 as the main verb	有
"VV": "V", #		other verbs	要
"X": "X", # numbers and units, mathematical sign	59mm
}


xpos2upos_dict = {
"AD":"ADV", # adverb	也
"AS": "AUX", # aspect marker	着
"BA": "ADP", # 把 in ba-construction	把
"CC": "CCONJ", # coordinating conjunction	和
"CD": "NUM", #  cardinal number	一百
"CS": "SCONJ", # subordinating conjunction	虽然
"DEC": "PART", # 的 in a relative-clause	的
"DEG": "PART", # associative	的
"DER": "PART",	# in V-de const. and V-de-R	得
"DEV":	"PART", # 地 before VP	地
"DT": "DET", # determiner	这
"ETC": "NOUN", # for words 等, 等等	等, 等等
"FW": "X", # foreign words	A
"IJ": "INTJ", # interjection	哈哈
"JJ": "ADJ", # other noun-modifer	新
"LB": "ADP",	# 被 in long bei-const	被
"LC": "ADP", # localizer	里
"M": "NOUN", # measure word	个
"MSP": "PART", # other particle	所
"NN": "NOUN", # common noun	工作
"NR": "PROPN", # proper noun	中国
"NT": "NOUN", # temporal noun	目前
"OD": "NUM", # ordinal number	第一
"ON": "NOUN", #	onomatopoeia
"P": "ADP", # Prepositions (excluding 把 and 被)	在
"PN": "PRON", # pronoun	我
"PU": "PUNCT", # punctuation	标点
"SB": "VERB",	# 被 in short bei-const	被+V
"SP": "PART", # sentence-final particle	吗
"VA": "VERB", #	predicative adjective	好
"VC": "VERB", #		copula	是
"VE": "VERB", #		有 as the main verb	有
"VV": "VERB", #		other verbs	要
"X": "X", # numbers and units, mathematical sign	59mm
}




def read_annotated_file(annotated_path):
    index_lsts = []
    sents = []
    with io.open(annotated_path, encoding="utf8") as f:
        for line in f.readlines():
            if line == "\n":
                continue
            else:
                toks = []
                index_lst = []
                line = re.split(r"\s+", line.strip())
                for tok in line:
                    if ":" in tok:
                        toks.append(tok.split(":")[0])
                        index_lst.append(tok.split(":")[1])
                    else:
                        toks.append(tok)
                        index_lst.append(0)
                assert len(toks) == len(index_lst)
                annotated_toks = " ".join(toks)
                
                sents.append(annotated_toks)
                index_lsts.append(index_lst)
                
                # assert len(sents.split()) == len(index_lst)
    return sents, index_lsts

def read_amr_plain(amr_plain_path):
    with io.open(amr_plain_path, "r", encoding="utf8") as f:
        lines = f.read().strip().split("\n")
    english_lines = [x.replace("# ::snt ", "") for x in lines if "# ::snt " in x]
    return english_lines

# This function fixes the
def generate_construal(ss):
    scene = "p." + ss.split("~")[0]
    if "~" in ss:
        function = "p." + ss.split("~")[1]
    else:
        function = scene
    return scene, function

def read_zh2en_alignment_file(alignment_file):
    with io.open(alignment_file, "r", encoding="utf8") as f:
        zh2en_alignments = [x.split("\t") for x in f.read().strip().split("\n") if "\t" in x]
    return zh2en_alignments

def read_meta_n_conllu_strings(conllu_path):
    meta_strings = []
    conllu_strings = []
    with io.open(conllu_path, "r", encoding="utf8") as f:
        chunks = f.read().strip().split("\n\n")
    
    for chunk in chunks:
        lines = chunk.strip().split("\n")
        meta_strings.append("\n".join([x for x in lines if "\t" not in x]))
        conllu_strings.append("\n".join([x for x in lines if "\t" in x]))
    
    return meta_strings, conllu_strings


