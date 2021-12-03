# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Data Loader for Turku Paraphrase Corpus"""


import csv
import json
import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{kanerva-etal-2021-finnish,
  title = {Finnish Paraphrase Corpus},
  author = {Kanerva, Jenna and Ginter, Filip and Chang, Li-Hsin and Rastas, Iiro and Skantsi, Valtteri and Kilpeläinen, Jemina and Kupari, Hanna-Mari and Saarni, Jenna and Sevón, Maija and Tarkka, Otto},
  booktitle = {Proceedings of the 23rd Nordic Conference on Computational Linguistics (NoDaLiDa'21)},
  year = {2021},
  publisher = {Linköping University Electronic Press, Sweden},
  url = {https://aclanthology.org/2021.nodalida-main.29},
  pages = {288--298}
}
"""


# You can copy an official description
_DESCRIPTION = """\
Turku Paraphrase Corpus is a dataset of 104,645 manually annotated Finnish paraphrases. The vast majority of the data is classified as a paraphrase either in the given context, or universally.
"""

_HOMEPAGE = "https://turkunlp.org/paraphrase.html"

_LICENSE = "Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)"


# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
  
    'train': 'https://github.com/TurkuNLP/Turku-paraphrase-corpus/raw/ver-1.1.0/data-fi/train.json',
    'validation': 'https://github.com/TurkuNLP/Turku-paraphrase-corpus/raw/ver-1.1.0/data-fi/dev.json',
    'test': 'https://github.com/TurkuNLP/Turku-paraphrase-corpus/raw/ver-1.1.0/data-fi/test.json',
    'doctexts': 'https://github.com/TurkuNLP/Turku-paraphrase-corpus/raw/ver-1.1.0/data-fi/texts.json.gz'
}



class TurkuParaphraseCorpus(datasets.GeneratorBasedBuilder):
    """Turku Paraphrase Corpus is a dataset of 104,645 manually annotated Finnish paraphrases."""

    VERSION = datasets.Version("1.1.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="plain", version=VERSION, description="This loads the dataset in its plain format without any additional data transformations. In case of applying the dataset to a task (e.g. paraphrase classification or generation), some additional data transformations are suggested depending on the task (see 'classification', 'classification-context', 'plain-context'  and 'generation' for ready made transformations for paraphrase classification and paraphrase generation)."),
        datasets.BuilderConfig(name="plain-context", version=VERSION, description="This loads the dataset in its plain format without any additional data transformations. In case of applying the dataset to a task (e.g. paraphrase classification or generation), some additional data transformations are suggested depending on the task (see 'classification', 'classification-context', 'plain' and 'generation' for ready made transformations for paraphrase classification and paraphrase generation). Unlike 'plain', this dataset  includes the document contexts, which eats memory, but otherwise it is the same as 'plain'. This is useful for context-based modelling."),
        datasets.BuilderConfig(name="classification", version=VERSION, description="This loads the dataset in a format directly suitable for paraphrase classification. Each example is introduced twice with different order of the text passages, (text1, text2, label) and (text2, text1, label)"),
        datasets.BuilderConfig(name="classification-context", version=VERSION, description="This loads the dataset in a format directly suitable for paraphrase classification. Each example is introduced twice with different order of the text passages, (text1, text2, label) and (text2, text1, label). Unlike 'classification' this dataset includes the document contexts, which eats memory but otherwise it is the same as 'classification'. This is useful for context-based modelling."),
        datasets.BuilderConfig(name="generation", version=VERSION, description="This loads the dataset in a format suitable for paraphrase generation, where examples not considered suitable for generation models are discarded. Paraphrases without directionality are generated in both directions, while directional paraphrases (subsumption flag) are only generated from more detailed to more general one. Labels 2 (related but not a paraphrase), 3 (context dependent paraphrase), flag i (minor deviation), and flag s (style difference) are discarded."),
    ]

    #DEFAULT_CONFIG_NAME = "plain"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        # This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        if self.config.name == "generation":  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "gem_id": datasets.Value("string"),
                    "goeswith": datasets.Value("string"),
                    "fold": datasets.Value("int32"),
                    "input": datasets.Value("string"),
                    "output": datasets.Value("string"),
                    "label": datasets.Value("string"),
                    "binary_label": datasets.Value("string"),
                    "is_rewrite": datasets.Value("bool"),
                }
            )
        elif self.config.name in ("classification","plain"):
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "gem_id": datasets.Value("string"),
                    "goeswith": datasets.Value("string"),
                    "fold": datasets.Value("int32"),
                    "text1": datasets.Value("string"),
                    "text2": datasets.Value("string"),
                    "label": datasets.Value("string"),
                    "binary_label": datasets.Value("string"),
                    "is_rewrite": datasets.Value("bool"),
                }
            )
        elif self.config.name in ("classification-context","plain-context"):# same format for classification/original
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "gem_id": datasets.Value("string"),
                    "goeswith": datasets.Value("string"),
                    "fold": datasets.Value("int32"),
                    "text1": datasets.Value("string"),
                    "text2": datasets.Value("string"),
                    "label": datasets.Value("string"),
                    "binary_label": datasets.Value("string"),
                    "is_rewrite": datasets.Value("bool"),
                    "context1": {"doctext":datasets.Value("string"), "start":datasets.Value("int32"), "end":datasets.Value("int32")},
                    "context2": {"doctext":datasets.Value("string"), "start":datasets.Value("int32"), "end":datasets.Value("int32")}
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        
        my_urls = _URLs
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": data_dir["train"], "split": "train", "doctexts": data_dir["doctexts"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": data_dir["validation"], "split": "validation", "doctexts": data_dir["doctexts"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": data_dir["test"], "split": "test", "doctexts": data_dir["doctexts"]})
        ]

    def _generate_examples(self, filepath, split, doctexts=None):
        """ Yields examples as (key, example) tuples. """
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.

        if doctexts and self.config.name in ("classification-context","plain-context"): #we dont want to read this in for configs which do not need the contexts
            with open(doctexts, "rt", encoding="utf-8") as f:
                doctexts_dict=json.load(f)
        else:
            doctexts_dict={}
        
        with open(filepath, "rt", encoding="utf-8") as f:
            data = json.load(f)
            counter = 0
            for example in data:
                ctx=example.get("context") #this is either the context information (a dict), or an empty dict if absent
                if ctx is None:
                    ctx={}
                d1=ctx.get("doc1")
                d2=ctx.get("doc2")
                if self.config.name in ("classification-context","plain-context"): #these two configs take the context
                    example["context1"]={"doctext":doctexts_dict.get(d1,""),"start":ctx.get("beg1",0),"end":ctx.get("end1",0)}
                    example["context2"]={"doctext":doctexts_dict.get(d2,""),"start":ctx.get("beg2",0),"end":ctx.get("end2",0)}
                if self.config.name == "generation":
                    examples = self._prepare_for_generation(example)
                else:
                    examples = self._prepare_plain_and_classification(example)
                for e in examples:
                    e["gem_id"] = f"gem-turku_paraphrase_corpus-{split}-{counter}" # fill in gem_id
                    e["id"]=f"turku_paraphrase_corpus-{split}-{counter}" # fill in gem_id
                    yield counter, e
                    counter += 1
                    
                    
    #### HELPER FUNCTIONS ####
    
    def _skip_in_generation(self, label):
        """ define here which examples should be skipped when doing paraphrase generation """
        skip_labels = ["2", "3", "i", "s"]
        for l in skip_labels:
            if l in label:
                return True
        return False

    def _prepare_for_generation(self, orig_example):
        """ turn examples into generation format """
        processed = []
        d = {
        "gem_id": "placeholder", # fill in later
        "goeswith": orig_example["goeswith"] if orig_example["goeswith"]!=None else "not available",
        "fold": orig_example["fold"],
        "input": orig_example["txt1"],
        "output": orig_example["txt2"],
        "label": orig_example["label"],
        "binary_label": "positive" if orig_example["label"] != "2" else "negative",
        "is_rewrite": False}

        label = d["label"]
        if self._skip_in_generation(label) == False:
            if ">" in label:
                processed.append(d)
            elif "<" in label:
                processed.append(self._flip_example(d, "input", "output"))
            else:
                processed.append(d)
                processed.append(self._flip_example(d, "input", "output"))
       
        for rew in orig_example["rewrites"]:
            r = self._generate_rew(d, rew, "input", "output")
            processed.append(r)
            processed.append(self._flip_example(r, "input", "output"))
        return processed
            
    def _prepare_plain_and_classification(self, orig_example):
        """ turn examples into classification format """
        processed = []
        d = {
            "gem_id": "placeholder", # fill in later
            "goeswith": orig_example["goeswith"] if orig_example["goeswith"]!=None else "not available",
            "fold": orig_example["fold"],
            "text1": orig_example["txt1"],
            "text2": orig_example["txt2"],
            "label": orig_example["label"],
            "binary_label": "positive" if orig_example["label"] != "2" else "negative",
            "is_rewrite": False,
        }
        if "context1" in orig_example and "context2" in orig_example:
            d["context1"]=orig_example["context1"]
            d["context2"]=orig_example["context2"]

        processed.append(d)
        if self.config.name == "classification":
            processed.append(self._flip_example(d, "text1", "text2"))
        for rew in orig_example["rewrites"]:
            r = self._generate_rew(d, rew, "text1", "text2")
            processed.append(r)
            if self.config.name == "classification":
                processed.append(self._flip_example(d, "text1", "text2"))
        return processed
        
    def _generate_rew(self, orig, rew, field1, field2):
        """ turn rewrite into individual example """
        d = {
            "gem_id": "placeholder", # fill in later
            "goeswith": orig["goeswith"],
            "fold": orig["fold"],
            field1: rew[0],
            field2: rew[1],
            "label": "4",
            "binary_label": "positive",
            "is_rewrite": True,
        }
        if "context1" in orig and "context2" in orig:
            d["context1"]={"doctext":"","start":0,"end":0}
            d["context2"]={"doctext":"","start":0, "end":0}
        return d
            
    def _flip_example(self, example, field1, field2):
        """ flip the example (text1, text2, label) --> (text2, text1, label) """
        flipped = example.copy()
        if "<" in example["label"]: # label needs to be flipped
            flipped["label"] = example["label"].replace("<", ">")
        if ">" in example["label"]:
            flipped["label"] = example["label"].replace(">", "<")
        flipped[field1] = example[field2]
        flipped[field2] = example[field1]
        if "context1" in example and "context2" in example:
            flipped["context1"],flipped["context2"]=example["context2"],example["context1"]
        return flipped
        
