import io, os, re

def read_conllulex(f):
	with io.open(f, "r", encoding="utf8") as fr:
		conllulex = [x.split("\n") for x in fr.read().strip().split("\n\n")]
	return conllulex

def write_conllulex(conllulex, f):
	with io.open(f, "w", encoding="utf8") as f:
		f.write("\n\n".join(["\n".join(x) for x in conllulex])+"\n\n")

def read_txt(f):
	with io.open(f, "r", encoding="utf8") as fr:
		lines = fr.read().strip().split("\n")
	plain_list = []
	for line in lines:
		if line.startswith("# ::id lpp_1943."):
			plain_list.append({})
		elif line.startswith("# ::snt "):
			plain_list[-1]["en"] = line.replace("# ::snt ", "").strip()
		elif line.startswith("# ::zh "):
			plain_list[-1]["zh"] = line.replace("# ::zh ", "").strip()
	assert len(plain_list) == 1562
	return plain_list

def add_english_meta(plain_list, tmp_en_sent_id):
	added_meta = "\n# en_sent_id = lpp_en-%d" % (tmp_en_sent_id + 1) + \
	"\n# zh_amr_sent_id = test_amr.%d" % (tmp_en_sent_id + 1) + \
	"\n# en_text = %s" % plain_list[tmp_en_sent_id]["en"] + \
	"\n# zh_amr_text = %s" % plain_list[tmp_en_sent_id]["zh"]
	return added_meta

def retrieve_english_sentences(corrected_conllulex, plain_list):
	tmp_en_sent_id = 0
	for sent_conllulex_id, sent_conllulex in enumerate(corrected_conllulex):
		for line_id, line in enumerate(sent_conllulex):
			if line.startswith("# text = "):
				zh_str = line.replace("# text = ", "").strip()
				zh_str_nospace = get_nospace_str(zh_str)
				plain_zh_str_nospace = get_nospace_str(plain_list[tmp_en_sent_id]["zh"])
				if zh_str_nospace == plain_zh_str_nospace:
					corrected_conllulex[sent_conllulex_id][line_id] += add_english_meta(plain_list, tmp_en_sent_id)
					tmp_en_sent_id += 1
				elif plain_zh_str_nospace in zh_str_nospace:
					while plain_zh_str_nospace in zh_str_nospace:
						corrected_conllulex[sent_conllulex_id][line_id] += add_english_meta(plain_list, tmp_en_sent_id)
						tmp_en_sent_id += 1
						plain_zh_str_nospace = get_nospace_str(plain_list[tmp_en_sent_id]["zh"])
					
				elif zh_str_nospace in plain_zh_str_nospace:
					corrected_conllulex[sent_conllulex_id][line_id] += add_english_meta(plain_list, tmp_en_sent_id)
					if plain_zh_str_nospace.endswith(zh_str_nospace):
						tmp_en_sent_id += 1
				else:
					assert False
					
					
				
				
				
				
				# if zh_str_nospace in plain_zh_str_nospace:
				# 	corrected_conllulex[sent_conllulex_id][line_id] = add_english_meta_to_line(
				# 		corrected_conllulex[sent_conllulex_id][line_id], plain_list[tmp_en_sent_id])
				# else:
				# 	tmp_en_sent_id += 1
				# 	plain_zh_str_nospace = get_nospace_str(plain_list[tmp_en_sent_id]["zh"])
				# 	if zh_str_nospace in plain_zh_str_nospace:
				# 		corrected_conllulex[sent_conllulex_id][line_id] = \
				# 			"# en_sent_id = lpp_en-%d\n# zh_amr_sent_id = test_amr.%d\n# en_text = %s\n# zh_amr_text = %s\n" \
				# 			% (tmp_en_sent_id+1, tmp_en_sent_id+1, plain_list[tmp_en_sent_id]["en"], plain_list[tmp_en_sent_id]["zh"]) \
				# 			+ corrected_conllulex[sent_conllulex_id][line_id]
				# 	else:
				# 		assert False
	return corrected_conllulex

def get_nospace_str(s):
	return re.sub(r"\s+", "", s)

if __name__ == '__main__':
	CORRECTED_PATH = ".." + os.sep + "corrected.conllulex"
	PLAIN_PATH = ".." + os.sep + "plain.txt"
	NEW_PATH = ".." + os.sep + "more_meta.conllulex"
	
	# read data
	corrected_conllulex = read_conllulex(CORRECTED_PATH)
	plain_list = read_txt(PLAIN_PATH)
	
	# retrieve English sentence splits
	new_conllulex = retrieve_english_sentences(corrected_conllulex, plain_list)
	
	# write new conllulex file
	write_conllulex(new_conllulex, NEW_PATH)
	
	
	
	
