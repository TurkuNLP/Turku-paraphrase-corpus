from datasets import load_dataset

d=load_dataset("turku_paraphrase_corpus.py",name="classification")
print(d)
for _ in range(10):
    for e in d["train"]:
        print(e)
    print("Pass 1")
    break
