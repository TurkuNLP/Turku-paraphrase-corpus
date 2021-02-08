# Turku-paraphrase-corpus

** CONFIDENTIAL DATA UNDER REVIEW DO NOT REDISTRIBUTE **

# File format

`txt1` and `txt2`: the paraphrase as extracted from text
`rewrites`: a list of (rew1,rew2) pairs, the rewrite(s) produced for this paraphrase during the annotation
`label`: main label + additional flags
`goeswith`: identification of the document from which the paraphrase was extracted, all paraphrases from one document are in one fold
`fold`: 0-99, data split to 100 parts, respecting document boundaries

# Labels

These are discussed in detail in the paper [URL].

x, 1: junk / uninteresting / unrelated
2: related but not paraphrase
3: paraphrase in the given document context, but not in general
4: paraphrase regardless of context

# Flags

i: minor traceable difference (number, case, this vs that, etc.), treat as 2 for strict interpretation, treat as 4 for information retrieval etc
s: style/strength difference
<: txt1 is more general than txt2; txt2 is more specific than txt1
>: txt2 is more general than txt1; txt1 is more specific than txt2

