# mmap_ninja_dataframe

Here, you can find a full list of the things you can do with `mmap-ninja-dataframe`.
A single sample is represented as a `dict`.
The two main abstractions are `DataFrameMmap` and `SparseDataFrameMmap`.
Use `DataFrameMmap` when you have the same keys present in every sample. 
If you have optional keys, which are available only in some samples, use `SparseDataFrameMmap`.

## Contents

Utils API:

1. [Generate batches from a function applied on data](#generate-batches-from-a-function-applied-on-data)

DataFrameMmap API:

1. [Create a DataFrameMmap from a list of dictionaries](#create-a-dataframemmap-from-a-list-of-dictionaries)
2. [Create a DataFrameMmap from a dictionary of lists](#create-a-dataframemmap-from-a-dictionary-of-lists)
3. [Create a DataFrameMmap from a generator](#create-a-dataframemmap-from-a-generator)
4. [Open an existing DataFrameMmap](#open-an-existing-dataframemmap)
5. [Append new samples to a DataFrameMmap](#append-new-samples-to-a-numpy-memmap)

SparseDataFrameMmap API:

1. [Create a SparseDataFrameMmap from list of dictionaries](#create-a-sparsedataframemmap-from-list-of-dictionaries)
2. [Create a SparseDataFrameMmap from a generator](#create-a-sparsedataframemmap-from-a-generator)
3. [Open an existing SparseDataFrameMmap](#open-an-existing-sparsedataframemmap)
4. [Append new samples to a SparseDataFrameMmap](#append-new-samples-to-a-raggedmmap)


### Generate batches from a function applied on data

When you have a sequence and you want to apply a function to batches of that sequence, use the `generate_batches` function.
For example, to tokenize a list of texts in a batched fashion using Hugginface tokenizers, use:

```python
from mmap_ninja_dataframe.base import generate_batches
from transformers import BertTokenizerFast

tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
texts = [
    'This is the first text',
    'Foo bar to yo asdasdasdasd asdasda',
    "We went to the dentist",
    "Spiderman is a superhero.",
    "Ilya e pich.",
    "Prodavam zelki",
]
for tokenized_batch in generate_batches(tokenizer, texts, 4):
    print(tokenized_batch)
```

### Create a DataFrameMmap from a list of dictionaries

To create a `DataFrameMmap` from a `list` of `dict`s, just use the `DataFrameMmap.from_list_of_dicts` method:

```python
import numpy as np
from mmap_ninja_dataframe.dense import DataFrameMmap

dicts = [
    {'input': np.array([1., 3., 7.1]), 'target': 0},
    {'input': np.array([0.1, 23.]), 'target': 1}
]
DataFrameMmap.from_list_of_dicts(
    out_dir='dataframe',
    dicts=dicts,
    mode='sample',
    verbose=True
)
```

### Create a DataFrameMmap from a dictionary of lists

To create a `DataFrameMmap` from a `dict` of `lists`s, just use the `DataFrameMmap.from_dict_of_lists` method:

```python
import numpy as np
from mmap_ninja_dataframe.dense import DataFrameMmap

dict_of_lists = {
    'input': [
        np.array([1., 3., 7.1]),
        np.array([0.1, 23.]),
    ],
    'target': [
        0,
        1
    ]
}
DataFrameMmap.from_dict_of_lists(
    out_dir='dataframe',
    dict_of_lists=dict_of_lists,
    verbose=True
)
```

### Create a DataFrameMmap from a generator

Very often, you cannot load the whole dataset into memory. In these cases, you can use the `DataFrameMmap.from_generator`
method. For example:

```python
import numpy as np
from mmap_ninja_dataframe.dense import DataFrameMmap

def generator_of_samples():
    for i in range(1, 100):
        yield {'description': f'descr{i}', 'tokens': np.zeros(i), 'index': i}


DataFrameMmap.from_generator(
    out_dir='alternative',
    sample_generator=generator_of_samples(),
    batch_size=32,
    mode='sample',
    verbose=True
)
```

Note that if you want to yield batches from the generator (as opposed to samples as in the previous example), you
have to pass `mode="batch"`. For example, you can use `DataFrameMmap.from_generator` and `generate_batches` to create
a `DataFrameMmap` which stores the results of tokenization with Huggingface:

```python
from mmap_ninja_dataframe.base import generate_batches
from mmap_ninja_dataframe.dense import DataFrameMmap
from transformers import BertTokenizerFast

tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
texts = [
    'This is the first text',
    'Foo bar to yo asdasdasdasd asdasda',
    "We went to the dentist",
    "Spiderman is a superhero.",
    "Ilya e pich.",
    "Prodavam zelki",
]

df_mmap = DataFrameMmap.from_generator(
    out_dir='df_mmap',
    sample_generator=generate_batches(tokenizer, texts, 4),
    batch_size=2,
    mode='batch',
    verbose=True
)
```

### Open an existing DataFrameMmap

Once you have created a `DataFrameMmap`, you can open it using its constructor.

```python
from mmap_ninja_dataframe.dense import DataFrameMmap

df_mmap = DataFrameMmap('df_mmap')
# len(df_mmap) now returns the number of samples in the dataframe
# df_mmap[5] is now a dictionary representing the 5-th sample
# df_mma['col'] is now a mmap representing the 
```

If you want to open a column with a specific wrapper function (see `mmap_ninja`'s `wrapper_fn` parameter), you can
pass a value to the `wrapper_fn_dict` parameter. 

If only a few columns need to be read from the parent directory, pass them to the `subset` argument. 

If `target_keys` is passed, then each sample will contain additional two keys: `idx` and `tasks`.
They can be used when using the `DataFrameMmap` as a dataset for training.

### Append new samples to a DataFrameMmap

You can add new samples to a `DataFrameMmap` easily.

To add a single sample, use the `.append` method.

To add multiple samples, use the `.extend` method.

To add multiple samples, represented by a dictionary of lists, use the `.extend_with_list_of_dicts`.

```python
import numpy as np
from mmap_ninja_dataframe.dense import DataFrameMmap

dataframe_mmap = DataFrameMmap('df_mmap')
dataframe_mmap.append({'description': 'He talked for so long.', 'tokens': np.array([1, 2, 3])})
```

### Create a SparseDataFrameMmap from list of dictionaries

To create a `SparseDataFrameMmap` from a `list` of `dict`s, just use the `SparseDataFrameMmap.from_list_of_dicts` method:

```python
import numpy as np
from mmap_ninja_dataframe.sparse import SparseDataFrameMmap

dicts = [
    {'input': np.array([1., 3., 7.1]), 'target': 0},
    {'input': np.array([0.1, 23.])}
]
SparseDataFrameMmap.from_list_of_dicts(
    out_dir='dataframe',
    dicts=dicts,
    verbose=True
)
```


### Create a SparseDataFrameMmap from a generator

Very often, you cannot load the whole dataset into memory. In these cases, you can use the `SparseDataFrameMmap.from_generator`
method. For example:


```python
from dnn_cool_synthetic_dataset.base import create_dataset

from mmap_ninja_dataframe.sparse import SparseDataFrameMmap

dicts = create_dataset(10_000)
sparse_mmap: SparseDataFrameMmap = SparseDataFrameMmap.from_generator(
    out_dir='sparse',
    sample_generator=dicts,
    batch_size=64,
    verbose=True
)
```

### Open an existing SparseDataFrameMmap

Once you have created a `SparseDataFrameMmap`, you can open it using its constructor.

```python
from mmap_ninja_dataframe.sparse import SparseDataFrameMmap

df_mmap = SparseDataFrameMmap('df_mmap')
# len(df_mmap) now returns the number of samples in the dataframe
# df_mmap[5] is now a dictionary representing the 5-th sample
```

If you want to open a column with a specific wrapper function (see `mmap_ninja`'s `wrapper_fn` parameter), you can
pass a value to the `wrapper_fn_dict` parameter. 

If only a few columns need to be read from the parent directory, pass them to the `subset` argument. 

If `target_keys` is passed, then each sample will contain additional two keys: `idx` and `tasks`.
They can be used when using the `DataFrameMmap` as a dataset for training.

### Append new samples to a SparseDataFrameMmap

You can add new samples to a `SparseDataFrameMmap` easily.

To add a single sample, use the `.append` method.

To add multiple samples, use the `.extend` method.

```python
import numpy as np
from mmap_ninja_dataframe.dense import DataFrameMmap

dataframe_mmap = DataFrameMmap('df_mmap')
dataframe_mmap.append({'description': 'He talked for so long.', 'tokens': np.array([1, 2, 3])})
```
