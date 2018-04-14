# YAML Structure


## Files Types
There are 3 types of YAML files
* [List Of Lists](#list-of-lists)
* [List](#list)
* [Poem](#poem)



###  List Of Lists
This YAML file contains the lists of all the lists present in the dataset. There is an ID associated with each List. To get the contents of a specific list, the user can query from the dataset using the List ID.

| Field Name | Type | Description
| ------ | ------ | ------ |
| lists | [ListOfListsObject](#listoflistsobject) | 
##### Example - a small section of list-of-lists.yaml file
```
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
```

### List
This YAML file contains the contents of a list. A list is further divided into sections. Each section has one or more poems. Each poem has a Poem ID associated with it. To get the contents of aq specific poem, the user can query from the dataset using the Poem ID.

| Field Name | Type | Description
| ------ | ------ | ------ |
| name | List<[ListNameObject](#listnameobject)> |
| sections | List<[SectionObject](sectionobject)> |

##### Example - a small section of lists/List_001.yaml
```
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
```

### Poem
This YAML file contains the contents of a poem. A poem is divided into shers.

| Field Name | Type | Description
| ------ | ------ | ------ |
| id | string | Poem ID
| audioUrl | string | Audio URL when the mp3 file is hosted. Currently, we support only one audio per poem 
| heading | List<[HeadingObject](#headingobject)> |
| description | List<[DescriptionObject](#descriptionobject)> |
| sher | List<[SherObject](#sherobject)> |

##### Example - a small section of poems/001/001_010.yaml
```
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
```

## Objects
### ListOfListsObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| name | List<[ListObject](#listobject)>

### ListObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| id | string | List ID
| name | List<[ListNameObject](#listnameobject)>

### ListNameObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| lang | string | Language (options: 'ur', 'en', 'ro')
| text | string | List Name in specified language

### SectionObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| sectionNames | List<[SectionNameObject](#sectionnameobject)> |

### SectionNameObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| lang | string | Language (options: 'ur', 'en', 'ro')
| text | string | List Section Name in specified language

### HeadingObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| lang | string | Language (options: 'ur', 'en', 'ro')
| text | string | Poem Heading in specified langauge

### DescriptionObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| lang | string | Language (options: 'ur', 'en', 'ro')
| text | string | Peom Description in specified language

### SherObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| id | string | Sher ID
| meta | boolean | This flags identifies text that is not part of a sher but is added by the author to provide context
| sherContent | List<[SherContentObject](#shercontentobject)> |

### SherContentObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| lang | string | Language (options: 'ur', 'en', 'ro')
| text | string | Sher Content in specified language
| notes | List<[NotesObject](#notesobject)>

### NotesObject
| Field Name | Type | Description
| ------ | ------ | ------ |
| phrase | string | The substring of text in SherContentObject to which this note is associated
| meaning | string | The content of the note
| occurrence | integer | In case the phrase occurs more than once, we can use this argument to specify which occurence the note applies to. Default: 1

# Text Files (Deprecated)

When I started collecting data, I used a custom format to store the contents in text file. After some time, I realized that an approach like this can work for simple projects, but if I want to move data around, I have to implement special parsers for every platform that needs to extract the contents of these files. We have ported all files to **YAML**. Almost every language has a YAML parser implemented which we can use to extract the contents.

### Scripts
To port files from custom text format to YAML format, I wrote the following 2 scripts:

* convert-list-text-to-yaml.py
* convert-poem-text-to-yaml.py

Both scripts expect 2 arguments.

First arg: Input folder
Second arg: Output folder

The script will fetch all text files in the input folder.
After that, it will parse the text contents, generate a YAML object and save that object in the output folder. As the script name suggests, **convert-list-text-to-yaml.py** converts the lists to YAML and **convert-poem-text-to-yaml.py** converts the poems to YAML.
