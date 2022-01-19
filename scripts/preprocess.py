import io, os
import stanza
from stanza.utils.conll import CoNLL
import re

def read_file(path):
    index_lsts = []
    sents = []
    with io.open(path, encoding="utf8") as f:
        for line in f.readlines():
            if line.startswith("X") or line.startswith("I") or line == "\n":
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
                sents.append(" ".join(toks))
                index_lsts.append(index_lst)
                # assert len(sents.split()) == len(index_lst)
    return sents, index_lsts


# This function fixes the
def generate_construal(ss):
    scene = "p." + ss.split("~")[0].lower()
    if "~" in ss:
        function = "p." + ss.split("~")[1].lower()
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
        for tok_id in range(len(toks)):
            assert "\t" in toks[tok_id]
            if supersenses[sent_id][tok_id] != 0:
                scene, function = generate_construal(supersenses[sent_id][tok_id])
            else:
                scene, function = ['_', '_']
            toks[tok_id] += '\t_' * 3 + '\t%s\t%s' % (scene, function) + '\t_' * 4
        conllulex += "# sent_id = lpp_zh-%d\n" % (sent_id+1) + "\n".join(toks) + "\n\n"
    return conllulex


if __name__ == "__main__":
    DATA_PATH = ".." + os.sep + "raw.txt"
    OUT_PATH = ".." + os.sep + "out.conllulex"

    sents, index_lst = read_file(DATA_PATH)
    conll_string = parse_conllu(sents)
    index_lst = index_lst[:len(conll_string)]
    conllulex_string = parse_conllulex(conll_string, index_lst)

    write_f = open(OUT_PATH, "w", encoding="utf8")
    write_f.write(conllulex_string)
    write_f.close()
