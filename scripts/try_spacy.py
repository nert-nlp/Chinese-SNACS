import spacy
from spacy.tokens import Doc

nlp = spacy.load("zh_core_web_sm")

s = "这 本 书 中 写道 ： “ 这些 蟒蛇 把 它们 的 猎获物 不加 咀嚼 地 囫囵 吞下 。"
s = s.split(" ")

doc = Doc(nlp.vocab, words=s)
nlp.get_pipe("tok2vec")(doc)
nlp.get_pipe("tagger")(doc)
for token in doc:
    print(f"Token: {token.text:10} Tag: {token.tag_}")

# nlp.tokenizer = nlp.tokenizer.PretokenizedTokenizer
# # nlp.tokenizer = nlp.tokenizer.tokens_from_list
# # out = nlp.pipe([s])
#
# docs = [nlp.get_pipe("tok2vec")(spacy.tokens.doc.Doc(nlp.vocab, words=sequence)) for sequence in [s]]
# docs = [nlp.get_pipe("tagger")(spacy.tokens.doc.Doc(nlp.vocab, words=sequence)) for sequence in [s]]
# tags = [[t.tag_ for t in doc] for doc in docs]
#
#
# for doc in out:
# 	print([token.text for token in doc])

print()