# Chinese-SNACS

# Data are stored in the following files:
- raw.txt: plain text file with TOKEN:SCENE\~FUNCTION annotations
- out.conllulex: 20-column extend conllu file with auto-parsed dependencies and supersense annotations in the 14th, 15th columns
- corrected.conllulex: several POS tags in conllulex are human corrected to pass validation (see https://github.com/nert-nlp/conllulex)

# Training stanza UD1 parser based on CoreNLP-converted OntoNotes Chinese PTB trees





# Preprocessings


### Parse CTB using attach-juxtapose-parser
- See https://github.com/princeton-vl/attach-juxtapose-parser
- Follow their Github to setup conda environments
- cd attach-juxtapose-parser/
- conda activate ctbparser
- python parse.py language=chinese model_path=dumps/ctb_bert_graph.pth input=../Chinese-SNACS/snacs_plain.txt  output=../Chinese-SNACS/snacs_attach.ctb
- Takes \~10mins to parse


### Parse CTB to SD using Stanford CoreNLP Java package

- java -mx1024m -cp "\*:" edu.stanford.nlp.trees.international.pennchinese.ChineseGrammaticalStructure -basic -conllx -treeFile __parse_file__ 


### Convert Stanford Dependency to Universal Dependency v1

- python -m depedit -c stan2uni.ini IN_FILE.conll > OUT_FILE.conllu1

### Convert UD v1 to UD v2

- udapy -s ud.Convert1to2 < IN_FILE.conllu1 > OUT_FILE.conllu2


# SNACS validation



