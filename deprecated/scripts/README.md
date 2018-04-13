# YAML Structure


## Files Types
There are 3 types of YAML files
* [List Of Lists](#lists-of-lists)
* [List](#list)
* [Poem](#poem)



###  List Of Lists
This YAML file contains the lists of all the lists present in the database. There is an ID associated with each List. To get the contents of a specific lists, the user can query the server using the List ID
| Field Name | Type | Description
| ------ | ------ | ------ |
| lists | [ListOfListsObject](#listoflistsobject) |

##### Example
---
lists:
- id: List_001
  name:
  - lang: ur
    text: بانگ درا
  - lang: en
    text: Bang-e-Dara
- id: List_002
  name:
  - lang: ur
    text: بال جبریل
  - lang: en
    text: Bal-e-Jibreel
---

### List
This YAML file contains the contents of a list. A list is further divided into sections. Each section has one or more poems. Each poem has a Poem ID associated with it. To get the contents of aq specific poem, the user can query the server using the Poem ID
| Field Name | Type | Description
| ------ | ------ | ------ |
| name | List<[ListNameObject](#listnameobject)> |
| sections | List<[SectionObject](sectionobject)> |

##### Example
---
name:
- lang: ur
  text: بانگ درا
- lang: en
  text: Bang-e-Dara
sections:
- sectionName:
  - lang: ur
    text: حصہ اول ـــــــ 1905 تک
  - lang: en
    text: Before 1908
- poems:
  - id: '001_001'
    poemName:
    - lang: ur
      text: ہمالہ
    - lang: en
      text: THE HIMALAYAS
  - id: '001_002'
    poemName:
    - lang: ur
      text: گل رنگيں
    - lang: en
      text: THE COLORFUL ROSE
---

### Poem
This YAML file contains the contents of a poem. A poem is divided into shers. 
| Field Name | Type | Description
| ------ | ------ | ------ |
| id | string |
| audioUrl | string |
| heading | List<[HeadingObject](#headingobject)> |
| description | List<[DescriptionObject](#descriptionobject)> |
| sher | List<[SherObject](#sherobject)> |

##### Example
---
'id': '001_010'
'audioUrl': ''
'heading':
- 'lang': 'ur'
  'text': 'ہمدردي'
- 'lang': 'en'
  'text': 'SYMPATHY'
'description': []
'sher':
- 'id': '001_010_001'
  'meta': !!bool 'false'
  'sherContent':
  - 'lang': 'ur'
    'text': 'ٹہني پہ کسي شجر کي تنہا | بلبل تھا کوئي اداس بيٹھا'
  - 'lang': 'en'
    'text': 'Perched on the branch of a tree | Was a nightingale sad and lonely'
  - 'lang': 'ro'
    'text': 'Tehni Pe Kisi Shajar Ki Tanha | Bulbul Tha Koi Udas Baitha'
---

## Objects
### ListOfListsObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| id | string |
| name | List<[ListNameObject](#listnameobject)>

### ListNameObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| lang | string |
| text | string |

### SectionObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| sectionNames | List<[SectionNameObject](#sectionnameobject)> |

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
| sherContent | List<[SherContentObject](#shercontentobject)> |

### SherContentObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| lang | string |
| text | string |
| notes | List<[NotesObject](#notesobject)>

### NotesObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| phrase | string |
| meaning | string |
| occurrence | integer |

# Text Structure (Deprecated)

### Scripts
When I started collecting data, I used a custom format to store the contents in text file. After some time, I realized that an approach like this can work for simple projects, but if I want to move data around, I have to implement special parsers for every platform that needs to extract the contents of these files. We have ported all files to **YAML**. Almost every language has a YAML parser implemented which we can use to extract the contents. 

To port files from custom text format to YAML format, I wrote the following 2 scripts:

* convert-list-text-to-yaml.py
* convert-poem-text-to-yaml.py

Both scripts expect 2 arguments. 

First arg: Input folder
Second arg: Output folder

The script will fetch all text files in the input folder.
After that, it will parse the text contents, generate a YAML object and save that object in the output folder. As the script name suggesets, **convert-list-text-to-yaml.py** converts the lists to YAML and **convert-poem-text-to-yaml.py** converts the poems to YAML.
