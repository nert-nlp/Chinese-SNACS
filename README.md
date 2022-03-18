# Chinese-SNACS

This corpus annotates adposition supersenses for the Mandarin Chinese translation of the Little Prince (小王子).
Adposition supersense annotations are based on English supersense guidelines (https://arxiv.org/abs/1704.02134) and source Chinese-English bitext is obtained from the AMR project (https://amr.isi.edu/download/amr-bank-struct-v1.6.txt).

## Data are stored in the following files:
- *snacs_annotated.txt*: plain text file with *TOKEN:SCENE\~FUNCTION* annotations
- *snacs_stanza.conllulex*: 20-column extended conllu file with stanza-parsed and udapy converted dependencies and supersense annotations in the 14th, 15th columns
- cf. conllulex validation (https://github.com/nert-nlp/conllulex)


## How to obtain the data:

### Step 1: stanza parse using customized models
> cd scripts

> python stanza_parse_ud1.py

- stanza-parsed UDv1 output file: *snacs_stanza.conllu1*
- contact sp1184@georgetown.edu for pretrained Chinese OntoNotes stanza models

### Step 2: use udapi to convert UD v1 to UD v2

(if udapi not installed) 
> pip install udapi

(back to Chinese_SNACS main directory) 
> cd ../

> udapy -s ud.Convert1to2 < snacs_stanza.conllu1 > snacs_stanza.conllu2

### Step 3: generate conllulex file by incorporating supersense annotations, adposition alignments and postag corrections (to pass validation)

> cd scripts/

> python ud2_to_conllulex.py



## Chinese to English adposition alignments
- For each adposition in Chinese, two annotators search across adpositions in the parallel English sentence and choose the aligned adposition if any. 
- Adposition alignment annotations appear in column 9, e.g. *AlignedTokId=6|AlignedAdposition=on*
- Multi-word adpositions do not occur in Chinese, but appear in English. For example, Chinese adpositions are aligned to English MWE such as because_of, as_if, out_of, etc; *AlignedTokId=2,3|AlignedAdposition=ahead_of*.
- Adposition alignments are not yet annotated for Chapters 1, 4 and 5.

## Chinese Lexical Categories (lexcat)


- ADJ: adjective, e.g. 新
- ADV: adverb, e.g. 也
- AUX: aspect marker, e.g. 着
- BA: ba-construction, e.g. 把
- CCONJ: coordinating conjunction, e.g. 和
- DE: de-construction, e.g. 的
- DET: determiner, e.g. 这
- INTJ: interjection, e.g. 哈哈
- LB: long bei construction, e.g. 被
- LC: localizer, e.g. 里
- N: noun, e.g. 中国
- NUM: number, e.g. 一百
- P: Prepositions (excluding 把 and 被), e.g. 在
- PART: particle, e.g. 吗
- PRON: pronoun, e.g. 我
- PUNCT: punctuation, e.g. 。
- SCONJ: subordinating conjunction, e.g. 虽然
- X: other part-of-speech, e.g. mathematical sign, foreign words

