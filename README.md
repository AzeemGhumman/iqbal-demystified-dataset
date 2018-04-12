# Contents
The file **list-of-lists.yaml** contains the list of books

The folder **lists-yaml** contains the list of poems for each book

The folder **poems-yaml** contains the contents of the individual poems

# Development
The text files are only included to be backward compatible. We were using text files before but have switched over the yaml format. I would still like to support text files since for some contributors, it might be easier to edit simple text files instead of yaml files

To create a .yaml file from a .txt file, use the **poem-parser.py** python script
This script takes as argument an input folder path (containing .txt files) and an output folder path (for generated .yaml files)

`$> python poem-parser.py {folder-input} {folder-output}`
