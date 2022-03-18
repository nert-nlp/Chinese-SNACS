import io, re, os
from hanziconv import HanziConv

relmap = {
	"compound:dir": "compound:vv",
	"neg": "advmod",
	"obj:periph": "obj",
}

def read_conllu_file(conllufile):
	with io.open(conllufile, "r", encoding="utf8") as f:
		conllus = [x.split("\n") for x in f.read().strip().split("\n\n")]
	
	sentences = []
	conllus_simplified = []
	for conllu_id, conllu in enumerate(conllus):
		sentence = " ".join([x.split("\t")[1] for x in conllu if "\t" in x])
		sentences.append(HanziConv.toSimplified(sentence))
		conllu_tmp = ""
		for line in conllu:
			if "\t" not in line:
				continue
			fields = line.split("\t")
			fields[1] = HanziConv.toSimplified(fields[1])
			fields[4] = fields[3]
			fields[5] = "_"
			fields[7] = fields[7] if fields[7] not in relmap.keys() else relmap[fields[7]]
			fields[9] = "_"
			conllu_tmp += "\t".join(fields)+"\n"
		conllus_simplified.append(conllu_tmp)
	
	return sentences, conllus_simplified

def write_sentences(sentences, txtfile):
	with io.open(txtfile, "w", encoding="utf8") as f:
		f.write("\n".join(sentences)+"\n")

def write_conllus(conllus, conllufile):
	with io.open(conllufile, "w", encoding="utf8") as f:
		f.write("\n".join(conllus)+"\n")


if __name__ == '__main__':
	UD_HK_PATH = "../zh_hk-ud-test.conllu"
	UD_HK_SIMPLIFIED_PATH = "../zh_hk-ud-test-simplified.conllu"
	UD_HK_PLAIN_PATH = "../zh_hk-ud-test-plain.txt"
	
	sentences, conllus_simplified = read_conllu_file(UD_HK_PATH)
	write_conllus(conllus_simplified, UD_HK_SIMPLIFIED_PATH)
	write_sentences(sentences, UD_HK_PLAIN_PATH)
	
	
	
	