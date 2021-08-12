# Turku-paraphrase-corpus

*The team*

Jenna Kanerva, Filip Ginter, Li-Hsin Chang, Iiro Rastas, Valtteri Skantsi, Jemina Kilpeläinen, Hanna-Mari Kupari, Aurora Piirto, Jenna Saarni, Maija Sevón, and Otto Tarkka

*Reference*

Jenna Kanerva, Filip Ginter, Li-Hsin Chang, Iiro Rastas, Valtteri Skantsi, Jemina Kilpeläinen, Hanna-Mari Kupari, Jenna Saarni, Maija Sevón, and Otto Tarkka. 2021. Finnish Paraphrase Corpus. Proceedings of NoDaLiDa'21. (to appear)

# File format

Each of the corpus data files is a `JSON` -formatted file, containing a list of data items. Additionally, to avoid repetition and excessive data file sizes, the texts of the documents are published in a single `JSON` -formatted file and referred to from the paraphrase data files. Each data item is a dictionary with the following keys:

`txt1` and `txt2`: the paraphrase as extracted from text
`rewrites`: a list of (rew1,rew2) pairs, the rewrite(s) produced for this paraphrase during the annotation, if any
`label`: main label + additional flags
`fold`: 0-99, data split into 100 parts respecting document boundaries, you can use this e.g. to implement crossvalidation safely
`goeswith`: identification of the document from which the paraphrase was extracted, all paraphrases from one document are in one fold, this can be `null` in case the source of the paraphrase is not from document-structured data
`context`: if available, it is a dictionary specifying the context of the paraphrases, i.e. their location in the original document. If not available, this is `null`. The keys are as follows:
  `beg1,end1`: the beginning and end character offsets of the first paraphrase text in its source document (Python notation, i.e. `end` is the first character index after the final character of the span)
  `doc1`: the key to the file `texts.json` where the actual text is stored
  `beg2,end2,doc2`: same as above, for the second paraphrase text

# Labels

These labels and their meaning are discussed in detail in the [accompanying paper](https://aclanthology.org/2021.nodalida-main.29/). To summarize:

`2`: related but not paraphrase
`3`: paraphrase in the given document contexts, but not in general
`4`: paraphrase in all reasonably possible contexts

# Flags

The following flags are applied as needed to label 4 paraphrases

`i`: minor traceable difference (number, case, 'this' vs 'that', etc.), treat as label 2 for strict interpretation, treat as label 4 for information retrieval and other similar tasks where minor differences do not matter
`s`: style difference (for example equivalent meaning, but one of the statements substantially more colloquial than the other)
`<`: txt1 is more general than txt2; txt2 is more specific than txt1; treat as label 3 for strict interpretation
`>`: txt2 is more general than txt1; txt1 is more specific than txt2; treat as label 3 for strict interpretation


