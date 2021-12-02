from datasets import load_dataset

d=load_dataset("turku_paraphrase_corpus.py",name="classification-nocontext")
print(d)
for e in d["train"]:
    print(e)
