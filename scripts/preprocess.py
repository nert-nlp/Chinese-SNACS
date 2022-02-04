import io, os
import stanza
from stanza.utils.conll import CoNLL
import re

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
"LB": "P",	# 被 in long bei-const	被
"LC": "P", # localizer	里
"M": "NOUN", # measure word	个
"MSP": "PART", # other particle	所
"NN": "NOUN", # common noun	工作
"NR": "PROPN", # proper noun	中国
"NT": "NOUN", # temporal noun	目前
"OD": "NUM", # ordinal number	第一
"ON": "NOUN", #	onomatopoeia
"P": "P", # Prepositions (excluding 把 and 被)	在
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

def read_file(annotated_path, plain_path):
    index_lsts = []
    sents = []
    with io.open(plain_path, encoding="utf8") as f:
        plains = f.read().strip().split("\n")
    with io.open(annotated_path, encoding="utf8") as f:
        # plain_sent_id = 0
        
        for line in f.readlines():
            if line == "\n":
                continue
            ## remove chapter lines
            # elif line.startswith("X") or line.startswith("I"):
            #     continue
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
                
                # if re.sub(r'\s+', '', annotated_toks) != re.sub(r'\s+', '', plains[plain_sent_id]):
                #     print(plain_sent_id, "annotated: ", annotated_toks, "plain: ", plains[plain_sent_id], sep="\n")
                # assert re.sub(r'\s+', '', annotated_toks) == re.sub(r'\s+', '', plains[plain_sent_id])
                # plain_sent_id += 1
                
                sents.append(annotated_toks)
                index_lsts.append(index_lst)
                
                # assert len(sents.split()) == len(index_lst)
    return sents, index_lsts


# This function fixes the
def generate_construal(ss):
    scene = "p." + ss.split("~")[0]
    if "~" in ss:
        function = "p." + ss.split("~")[1]
    else:
        function = scene
    return scene, function


def parse_conllu(text):
    # stanfordnlp.download('zh') # Download the English models
    nlp = stanza.Pipeline("zh", processors='tokenize,pos,lemma,depparse', tokenize_pretokenized=True, tokenize_no_ssplit=True,
                          # tokenize_model_path="/Users/loganpeng/Dropbox/Dissertation/code/stanza-train/stanza/saved_models/tokenize/zh_ontonotes_tokenizer.pt",
                          pos_pretrain_path="/Users/loganpeng/Dropbox/Dissertation/code/stanza-train/stanza/saved_models/pos/zh_ontonotes.pretrain.pt",
                          pos_model_path="/Users/loganpeng/Dropbox/Dissertation/code/stanza-train/stanza/saved_models/pos/zh_ontonotes_tagger.pt",
                          depparse_pretrain_path="/Users/loganpeng/Dropbox/Dissertation/code/stanza-train/stanza/saved_models/depparse/zh_ontonotes.pretrain.pt",
                          depparse_model_path="/Users/loganpeng/Dropbox/Dissertation/code/stanza-train/stanza/saved_models/depparse/zh_ontonotes_parser.pt")
    # nlp = stanza.Pipeline("zh", processors='tokenize,pos,lemma,depparse', tokenize_pretokenized=True, tokenize_no_ssplit=True)
    ### nlp = stanza.Pipeline(processors='tokenize,pos,lemma,depparse', lang='zh', tokenize_pretokenized=True, use_gpu=True, pos_batch_size=3000)
    conllus = []
    for sid, sentence in enumerate(text):
        # if sid > 10:
        #     continue
        doc = nlp(sentence) # Run the pipeline on input text
        dicts = doc.to_dict()
        conllu = CoNLL.convert_dict(dicts)
        for tokid in range(len(conllu[0])):
            conllu[0][tokid][3] = xpos2upos_dict[conllu[0][tokid][3]] # change col3 to upos
            conllu[0][tokid][9] = "_"  # remove start_char and end_char
        conllu = "\n".join(['\t'.join(x) for x in conllu[0]])
        conllus.append(conllu)
        print('o Done parsing sentence %d/%d' % (sid, len(text)), end="\r")
    return conllus


def parse_conllulex(conllus, supersenses):
    """
    conllu: text file in conllu form
    supersense: A list of supersense annotations for each token, 0
    """
    assert len(supersenses) == len(conllus)
    conllulex = "# newdoc_id = lpp_zh\n"
    
    for sent_id in range(len(conllus)):
        toks = conllus[sent_id].split("\n")
        assert len(toks) == len(supersenses[sent_id])
        text_field = ""
        for tok_id in range(len(toks)):
            assert "\t" in toks[tok_id]
            text_field += toks[tok_id].split('\t')[1]
            if supersenses[sent_id][tok_id] != 0:
                scene, function = generate_construal(supersenses[sent_id][tok_id])
            else:
                scene, function = ['_', '_']
            toks[tok_id] += '\t_' * 3 + '\t%s\t%s' % (scene, function) + '\t_' * 4
        conllulex += "# sent_id = lpp_zh-%d\n# text = %s\n" % (sent_id+1, text_field) + "\n".join(toks) + "\n\n"
    return conllulex


if __name__ == "__main__":
    PLAIN_PATH = ".." + os.sep + "plain.txt"
    ANNOTATED_PATH = ".." + os.sep + "annotated.txt"
    OUT_PATH = ".." + os.sep + "out.conllulex"

    sents, index_lst = read_file(annotated_path=ANNOTATED_PATH, plain_path=PLAIN_PATH)
    conll_string = parse_conllu(sents)
    index_lst = index_lst[:len(conll_string)]
    conllulex_string = parse_conllulex(conll_string, index_lst)

    write_f = open(OUT_PATH, "w", encoding="utf8")
    write_f.write(conllulex_string)
    write_f.close()
