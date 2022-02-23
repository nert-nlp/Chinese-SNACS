import io, os, re
from supar import Parser
# parser = Parser.load("crf-con-electra-zh")
parser = Parser.load("biaffine-dep-electra-zh")

plain_file_path = "../snacs_plain.txt"
supar_ctb_path = "../snacs_supar.ctb"

with io.open(plain_file_path, "r", encoding="utf8") as f:
	lines = [re.split(r" +", x.strip()) for x in f.read().strip().split("\n")]

# lines = lines[:10]

## Method 1: as a whole
# parsed = parser.predict(lines, lang=None, verbose=False)
# parsed = [str(x) for x in parsed]

## Method 2: sentence by sentence
parsed = []
for line_id, line in enumerate(lines):
	if line_id <= 610:
		continue
	tmp = str(parser.predict([line], lang=None, verbose=False)[0])
	parsed.append(tmp)
	print(tmp)
	print("o Done with line: %d" % line_id)

with io.open(supar_ctb_path, "w", encoding="utf8") as f:
	f.write("\n\n".join(parsed)+"\n\n")