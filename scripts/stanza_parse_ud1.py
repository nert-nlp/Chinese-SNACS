import io, os, re
import stanza
from stanza.utils.conll import CoNLL
from utils import read_amr_plain, read_annotated_file, generate_construal, xpos2upos_dict

def parse_conllu(text, english_lines):
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
    chapter_initials = []
    text_fields = []
    for sid, sentence in enumerate(text):

        # if sid > 10:
        #     continue
        
        # Get Chapter initial sentences
        chapter_initials.append(True if re.match("^[IVX。 ]+$", sentence) else False)
        # Stanza parse UD
        doc = nlp(sentence) # Run the pipeline on input text
        dicts = doc.to_dict()
        conllu = CoNLL.convert_dict(dicts)
        text_fields.append("".join([x[1] for x in conllu[0]]))
        for tokid in range(len(conllu[0])):
            conllu[0][tokid][3] = xpos2upos_dict[conllu[0][tokid][3]] # change col3 to upos
            conllu[0][tokid][9] = "_"  # remove start_char and end_char
        conllu = "\n".join(['\t'.join(x) for x in conllu[0]])
        conllus.append(conllu)
        print('o Done parsing sentence %d/%d' % (sid, len(text)), end="\r")

    # assert sum(chapter_initials) == 27
    
    # Write conllu string
    chapter_no = 1
    conllu_string = ""
    for sent_id in range(len(conllus)):
        if chapter_initials[sent_id]:
            conllu_string += "# newdoc_id = lpp_1943_zh_ch-%.2d\n" % chapter_no
            chapter_no += 1
        conllu_string += "# sent_id = lpp_1943_zh-%d\n# text = %s\n# en_text = %s\n" % (
        sent_id + 1, text_fields[sent_id], english_lines[sent_id]) + conllus[sent_id] + "\n\n"

    return conllu_string


if __name__ == "__main__":
    AMR_PLAIN_PATH = ".." + os.sep + "amr_plain.txt"
    ANNOTATED_PATH = ".." + os.sep + "annotated.txt"
    OUT_PATH = ".." + os.sep + "snacs_stanza_new.conllu1"

    sents, index_lst = read_annotated_file(annotated_path=ANNOTATED_PATH)
    english_lines = read_amr_plain(AMR_PLAIN_PATH)
    conllu_string = parse_conllu(sents, english_lines)

    write_f = open(OUT_PATH, "w", encoding="utf8")
    write_f.write(conllu_string)
    write_f.close()
