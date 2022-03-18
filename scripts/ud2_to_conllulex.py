import io, os
import stanza
from stanza.utils.conll import CoNLL
import re
import copy
from utils import read_annotated_file, read_zh2en_alignment_file, generate_construal, xpos2lexcat_dict

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

    

def parse_conllulex(conllus, supersenses, metas, zh2en_alignments):
    """
    conllu: text file in conllu form
    supersense: A list of supersense annotations for each token, 0
    """
    assert len(supersenses) == len(conllus) == len(metas)
    conllulex = ""
    doc_id = None
    updated_alignments = copy.copy(zh2en_alignments)
    
    for sent_id in range(len(conllus)):
        if "# newdoc_id = lpp_1943_zh_ch-" in metas[sent_id]:
            doc_id = int(re.match(r"# newdoc_id = lpp_1943_zh_ch-(\d+)", metas[sent_id]).group(1))
        conllulex += metas[sent_id] + "\n"
        toks = conllus[sent_id].split("\n")
        assert len(toks) == len(supersenses[sent_id])
        
        for tok_id in range(len(toks)):
            assert "\t" in toks[tok_id]
            fields = toks[tok_id].split("\t")
            if fields[7] == "etc":
                fields[7] = "dep"
            
            if supersenses[sent_id][tok_id] != 0:
                scene, function = generate_construal(supersenses[sent_id][tok_id])
                
                # Include zh2en adposition alignments
                if doc_id not in [1, 4, 5]:
                    assert fields[1] == updated_alignments[0][1]
                    fields[9] = "AlignedTokId=%s|AlignedAdposition=%s" % \
                                        (updated_alignments[0][5], updated_alignments[0][2])
                    updated_alignments.pop(0)

            else:
                scene, function = ['_', '_']
            toks[tok_id] = "\t".join(fields) + \
                           '\t_\t%s\t%s' % (xpos2lexcat_dict[fields[4]], fields[2]) +  \
                           '\t%s\t%s' % (scene, function) + '\t_' * 4
        conllulex += "\n".join(toks) + "\n\n"
        
    assert len(updated_alignments) == 0
    
    return conllulex


if __name__ == "__main__":
    CONLLU2_PATH = ".." + os.sep + "snacs_stanza.conllu2"  # for conllu info
    CONLLU1_PATH = ".." + os.sep + "snacs_stanza.conllu1"  # for sentence and newdoc meta information
    ANNOTATED_PATH = ".." + os.sep + "annotated.txt"
    ALIGNMENT_PATH = os.path.join("..", "..", "Adposition_Alignment", "zh2en_adposition_alignments_after_adjudication.txt")
    OUT_PATH = ".." + os.sep + "snacs_stanza.conllulex"
    

    sents, index_lst = read_annotated_file(annotated_path=ANNOTATED_PATH)
    meta_strings, _ = read_meta_n_conllu_strings(CONLLU1_PATH)
    _, conllu_strings = read_meta_n_conllu_strings(CONLLU2_PATH)
    zh2en_alignments = read_zh2en_alignment_file(ALIGNMENT_PATH)
    
    conllulex_string = parse_conllulex(conllu_strings, index_lst, meta_strings, zh2en_alignments)

    write_f = open(OUT_PATH, "w", encoding="utf8")
    write_f.write(conllulex_string)
    write_f.close()
