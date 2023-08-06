# Description

Searches files line by line for given words

# Installation

`pip install lineident`

# Usage

**From command line:**

`--path PATH --words WORDS [--method {or,and}] [--format {std,wln}]`

| Option | Short | Type | Default | Description |
|---|---|---|---|---|
|--path | -p | String | - | Path to file which shall be searched |
|--words | -w | String | - | CSV input e.g.: dog,cat,hello |
|--method | -m | String | or | or = Checks if one of the words is in the line <br> and = Checks if all words are in the line |
|--format | -f | String | std | std = Standard output <br> wln = Without Line Number |


# Example

`python -m lineident -p path/to/example_list.txt -w cat,dog,people -m or`

```
################################################################################

lineident by 5f0
Searches files line by line for given words

Current working directory: path/to/lineident

-->    Path: path/to/example_list.txt
-->     MD5: 175e1b9d0e5d980323dcd01e1d4b21e9
-->  SHA256: 3563b6334e666d43365882ba5a218592a9036f2eeb2dbc6ed38a66ff1175b2ac

Datetime: 01/01/1970 11:12:13

################################################################################

Search Options:
---

Method: or
 Words: ["cat", "dog", "people"]


Result:
---
Hits: 2
---

Line Nr: 44 --> cat
Line Nr: 51 --> dog
Line Nr: 53 --> people

################################################################################

Execution Time: 0.0 sec

```


# License

MIT