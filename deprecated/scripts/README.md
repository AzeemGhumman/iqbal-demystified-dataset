# Notes for Developers
# Scripts
When I started collecting data, I used a custom format to store the contents in text file. After some time, I realized that an approach like this can work for simple projects, but if I want to move data around, I have to implement special parsers for every platform that needs to extract the contents of these files. We have ported all files to **YAML**. Almost every language has a YAML parser implemented which we can use to extract the contents. 

[link](#listoflistsobject)

To port files from custom text format to YAML format, I wrote the following 2 scripts:
1 - convert-list-text-to-yaml.py
2 - convert-poem-text-to-yaml.py

Both scripts expect 2 arguments. 
First arg: Input folder
Second arg: Output folder

The script will fetch all text files in the input folder.
After that, it will parse the text contents, generate a YAML object and save that object in the output folder. As the script name suggesets, **convert-list-text-to-yaml** converts the lists to YAML and **convert-poem-text-to-yaml** converts the poems to YAML.

# YAML Structure
## Files Types
###  List-of-lists
| Field Name | Type | Description
| ------ | ------ | ------ |
| lists | ListOfListsObject |

### List
| Field Name | Type | Description
| ------ | ------ | ------ |
| name | List<ListNameObject> |
| sections | List<SectionObject> |

### Poem
| Field Name | Type | Description
| ------ | ------ | ------ |
| id | string |
| audioUrl | string |
| heading | List<HeadingObject> |
| description | List<DescriptionObject> |
| sher | List<SherObject> |

## Objects

### ListOfListsObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| id | string |
| name | List<ListNameObject>

### ListNameObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| lang | string |
| text | string |

### SectionObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| sectionNames | List<SectionNameObject> |

### SectionNameObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| lang | string |
| text | string |

### HeadingObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| lang | string |
| text | string |

### DescriptionObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| lang | string |
| text | string |

### SherObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| id | string |
| meta | boolean |
| sherContent | List<SherContentObject> |

### SherContentObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| lang | string |
| text | string |
| notes | List<NotesObject>

### NotesObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| phrase | string |
| meaning | string |
| occurrence | integer |

# Text Structure (Deprecated)


The text files are only included to be backward compatible. We were using text files before but have switched over the yaml format. I would still like to support text files since for some contributors, it might be easier to edit simple text files instead of yaml files

To create a .yaml file from a .txt file, use the **poem-parser.py** python script
This script takes as argument an input folder path (containing .txt files) and an output folder path (for generated .yaml files)

**poem .py**

`$> python poem-parser.py {folder-input} {folder-output}`
