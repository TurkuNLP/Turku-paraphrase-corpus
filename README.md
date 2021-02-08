# Turku-paraphrase-corpus

** CONFIDENTIAL DATA UNDER REVIEW DO NOT REDISTRIBUTE **

# File format

> `txt1` and `txt2`

The paraphrase as extracted from the original document

> `rewrites`

a list of (rew1,rew2) pairs, the rewrite(s) produced for this paraphrase during the annotation

> `label`

Main label + additional flags

> `goeswith`

Identification of the document from which the paraphrase was extracted, all paraphrases from one document are in one fold

> `fold`

A number between 0 and 99, data split to 100 parts, respecting document boundaries

# Labels

These are discussed in detail in the paper [URL].

> `x, 1`

junk / uninteresting / unrelated

> `2`

related but not paraphrase

> `3`

paraphrase in the given document context, but not in general

> `4`

paraphrase regardless of context

# Flags

These flags are only given to the label 4 paraphrases and act as a qualifier to the paraphrase. Without the flag, these would drop to 3 or even 2.

> `i`

minor traceable difference (number, case, this vs that, etc.), treat as 2 for strict interpretation, treat as 4 for information retrieval etc

> `s`

style/strength difference

> `<`

txt1 is more general than txt2; txt2 is more specific than txt1

> `>`

txt2 is more general than txt1; txt1 is more specific than txt2

