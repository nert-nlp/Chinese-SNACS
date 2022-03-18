import io, os, re
from utils import read_zh2en_alignment_file

def read_conllulex(filepath):
	conllulex_dict = {}
	with io.open(filepath, "r", encoding="utf8") as f:
		chunks = [x.split("\n") for x in f.read().strip().split("\n\n")]
	for chunk_id in range(len(chunks)):
		for line_id in range(len(chunks[chunk_id])):
			if chunks[chunk_id][line_id].startswith("# sent_id = lpp_1943."):
				sent_id = int(chunks[chunk_id][line_id].replace("# sent_id = lpp_1943.", ""))
				break
		sent_conllulex = [x.split("\t") for x in chunks[chunk_id] if "\t" in x]
		conllulex_dict[sent_id] = sent_conllulex
	return conllulex_dict

if __name__ == '__main__':
	eng_conlllulex_file_path = "../eng.conllulex"
	alignment_file_path = "../zh2en_adposition_alignments_final.txt"
	
	zh2en_alignments = read_zh2en_alignment_file(alignment_file_path)
	chunks = read_conllulex(eng_conlllulex_file_path)
	
	for align_id, alignment in enumerate(zh2en_alignments):
		if "," not in alignment[5] and alignment[4]!="None" and alignment[5]!="None":
			assert " " not in chunks[int(alignment[4])][int(alignment[5])-1][12]
			
	
	print("Done!")
		
		
	