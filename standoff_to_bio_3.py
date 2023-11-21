# Convert tags to int and create dataset for Huggingface

import os

# Dictionary of labels to ids
label2id = {
    "O": 0,
    "B-Claim": 1,
    "I-Claim": 2,
    "B-Majorclaim": 3,
    "I-Majorclaim": 4,
    "B-Premise": 5,
    "I-Premise": 6
}

# Function to convert tags to their corresponding ids
def tags_to_ids(tags, label_to_id):
    return [label2id.get(tag, 0) for tag in tags]


id_list = []  # a list of ints
tokens_list = []  # a list of tuple of strings
ner_tags_list = []  # a list of tuple of ints

id = 0
for file in os.listdir('output_with_bio'):
    if file.endswith(".tsv"):
        with open(os.path.join('output_with_bio', file), 'r') as f:
            sample_text = f.read()
            # Your code here

        # Splitting the text into lines, and then into tokens and tags
        lines = sample_text.strip().split("\n")
        tokens, tags = zip(*[line.split("\t") for line in lines])

        # Converting tags to their corresponding ids
        tag_ids = tags_to_ids(tags, label_to_id)
        assert len(tokens) == len(tag_ids)
        id_list.append(id)
        tokens_list.append(tuple(tokens))
        ner_tags_list.append(tuple(tag_ids))

        id += 1

# Minimum working example
from datasets import Dataset, Features, Value, ClassLabel, Sequence
data = {
    "id":id_list,
    "ner_tags": ner_tags_list,
    "tokens": tokens_list
}


features = Features({
    "id": Value("int32"),
    "tokens": Sequence(Value("string")),
    "ner_tags": Sequence(ClassLabel(names=["O","B-Claim","I-Claim", "B-Majorclaim", "I-Majorclaim", "B-Premise", "I-Premise"]))
})

ds = Dataset.from_dict(data, features)

ds_split= ds.train_test_split(test_size=0.1, shuffle=True)

# save ds_split to pickle
import pickle
with open('ds_split.pickle', 'wb') as f:
    pickle.dump(ds_split, f)