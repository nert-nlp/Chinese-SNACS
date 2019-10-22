import io, os
import stanfordnlp
import re

def read_file(path):
    index_lst = []
    sents = ""
    with io.open(path, encoding="utf8") as f:
        for line in f.readlines():
            if line.startswith("X") or line.startswith("I") or line == "\n":
                continue
            else:
                toks = []
                line = re.split(r"\s+", line.strip())
                for tok in line:
                    if ":" in tok:
                        toks.append(tok.split(":")[0])
                        index_lst.append(tok.split(":")[1])
                    else:
                        toks.append(tok)
                        index_lst.append(0)
                sents += " ".join(toks)
                sents += " \n"
                index_lst.append(0)
                # assert len(sents.split()) == len(index_lst)
    return sents, index_lst[:-1]


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
    nlp = stanfordnlp.Pipeline(processors='tokenize,mwt,pos,lemma,depparse', lang='zh', tokenize_pretokenized=True, use_gpu=True, pos_batch_size=3000)
    doc = nlp(text) # Run the pipeline on input text
    return doc.conll_file.conll_as_string()


def parse_conllulex(conllu, supersenses):
    """
    conllu: text file in conllu form
    supersense: A list of supersense annotations for each token, 0
    """
    lines = conllu.strip().replace('\r', '').split('\n')
    assert len(supersenses) == len(lines)
    for l_id in range(len(lines)):
        if '\t' in lines[l_id]:
            if supersenses[l_id] != 0:
                scene, function = generate_construal(supersenses[l_id])
            else:
                scene, function = ['_', '_']
            lines[l_id] = lines[l_id] + '\t_' * 3 + '\t%s\t%s' % (scene, function) + '\t_' * 4

    return '\n'.join(lines)


if __name__ == "__main__":
    DATA_PATH = ".." + os.sep + "raw.txt"
    OUT_PATH = ".." + os.sep + "out.conllulex"

    sents, index_lst = read_file(DATA_PATH)
    conll_string = parse_conllu(sents)
    conllulex_string = parse_conllulex(conll_string, index_lst)

    write_f = open(OUT_PATH, "w", encoding="utf8")
    write_f.write(conllulex_string)
    write_f.close()
