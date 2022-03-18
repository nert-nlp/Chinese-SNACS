import io, os, re


def get_deprel_list(filepath):
	with io.open(filepath, "r", encoding="utf8") as f:
		lines = f.read().strip().split("\n")
	deprel_list = sorted(list(set([x.split("\t")[7] for x in lines if "\t" in x])))
	return deprel_list

def simplify_relations(rel_list):
	return sorted(list(set([x.split(":")[0] for x in rel_list])))

if __name__ == '__main__':
	UD2_EWT_TRAIN_PATH = "/Users/loganpeng/Dropbox/Corpora/UD_English-EWT/en_ewt-ud-train.conllu"
	UD2_GUM_TRAIN_PATH = "/Users/loganpeng/Dropbox/Corpora/UD_English-GUM/en_gum-ud-train.conllu"
	HK2_TEST_PATH = "/Users/loganpeng/Dropbox/Spring_2022/RA_Nathan/Chinese-SNACS/zh_hk-ud-test.conllu"
	CONVERTED_HK2_TEST_PATH = "/Users/loganpeng/Dropbox/Spring_2022/RA_Nathan/Chinese-SNACS/zh_hk-ud-test-attach.ctb.conllu2hk"
	CONVERTED_SNACS_PATH = "/Users/loganpeng/Dropbox/Spring_2022/RA_Nathan/Chinese-SNACS/snacs_attach.ctb.conllu2hk"
	STANZA_SNACS_PATH = "/Users/loganpeng/Dropbox/Spring_2022/RA_Nathan/Chinese-SNACS/snacs_stanza.conllu2"
	
	
	
	print("UD2_EWT_TRAIN_PATH: ",  " ".join(simplify_relations(get_deprel_list(UD2_EWT_TRAIN_PATH))))
	# print("UD2_GUM_TRAIN_PATH: ", " ".join(get_deprel_list(UD2_GUM_TRAIN_PATH)))
	# print("HK2_TEST_PATH: ",  " ".join(simplify_relations(get_deprel_list(HK2_TEST_PATH))))
	# print("CONVERTED_HK2_TEST_PATH: ",  " ".join(get_deprel_list(CONVERTED_HK2_TEST_PATH)))
	# print("CONVERTED_SNACS_PATH: ", " ".join(simplify_relations(get_deprel_list(CONVERTED_SNACS_PATH))))
	print("STANZA_SNACS_PATH: ", " ".join(simplify_relations(get_deprel_list(STANZA_SNACS_PATH))))