# Chinese-SNACS

# Data are stored in the following files:
- raw.txt: plain text file with TOKEN:SCENE\~FUNCTION annotations
- out.conllulex: 20-column extend conllu file with auto-parsed dependencies and supersense annotations in the 14th, 15th columns
- corrected.conllulex: several POS tags in conllulex are human corrected to pass validation (see https://github.com/nert-nlp/conllulex)

# Training stanza UD1 parser based on CoreNLP-converted OntoNotes Chinese PTB trees

java -mx1024m -cp "*:" edu.stanford.nlp.trees.international.pennchinese.ChineseGrammaticalStructure -treeFile __parse_file__ -basic -conllx
