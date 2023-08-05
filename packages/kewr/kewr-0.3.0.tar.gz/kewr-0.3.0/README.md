# KEWR

A simple python script runner.

Many processes we use python for consist of a set of scripts, with particular inputs and outputs. tskr can be used to track all the scripts in a workflow and run them independently. 

For example, our project might include scripts to preprocess some data, do some analysis, then produce some plots. Each of these scripts might take arguments or options. We might complete the sequence like this 

```
python ./preprocess_script.py /path/to/data
python ./analysis_script.py argument_1 --optional-flag  
python ./plotting_script.py /path/to/plot/dir
```

tskr aims to keep our scripts organized along with their arguments.

## Installation

```
pip install kewr
```

## Usage

First create a new config file

```
python -m kewr create #creates a new tskr config file in the directory
```

In this file we define the stages of our script sequence. The config is a .toml file with sections for each stage.

```
[stage1]
help = "description of what the stage does"
cmd = "python example_script.py --option"
deps = ["/path/to/input/file"]
outs = ["/path/to/output/file"]
```

List the available stages with 

```
python -m kewr list
```

Run each stage with 

```
python -m kewr run stage1
```

You can also run multiple stages at once with 

```
python -m kewr run stage1 stage2 stage3
```

Or run all stages at once

```
python -m kewr run all
```