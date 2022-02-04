import io, os, re

def read_conllulex(f):
	with io.open(f, "r", encoding="utf8") as fr:
		conllulex = [x.split("\n") for x in fr.read().strip().split("\n\n")]
	return conllulex

def write_conllulex(conllulex, f):
	with io.open(f, "w", encoding="utf8") as f:
		f.write("\n\n".join(["\n".join(x) for x in conllulex])+"\n\n")

def get_toks_for_one_sent(sent):
	toks = [x.split("\t")[1] for x in sent if "\t" in x]
	return toks

if __name__ == '__main__':
	OUT_PATH = ".." + os.sep + "out.conllulex"
	CORRECTED_PATH = ".." + os.sep + "corrected.conllulex"
	
	out_conllulex = read_conllulex(OUT_PATH)
	corrected_conllulex = read_conllulex(CORRECTED_PATH)
	
	corrected_sent_id = 0
	for out_sent_id in range(len(out_conllulex)):
		out_toks = get_toks_for_one_sent(out_conllulex[out_sent_id])
		corrected_toks = get_toks_for_one_sent(corrected_conllulex[corrected_sent_id])
		if len(out_toks) <= 2 and out_toks != corrected_toks:
			continue
		assert out_toks == corrected_toks
		out_conllulex[out_sent_id] = [x for x in out_conllulex[out_sent_id] if x.startswith("#")] + \
		                             [x for x in corrected_conllulex[corrected_sent_id] if not x.startswith('#')]
		corrected_sent_id += 1
	
	NEW_PATH = ".." + os.sep + "out_corrected.conllulex"
	write_conllulex(out_conllulex, NEW_PATH)
	
	