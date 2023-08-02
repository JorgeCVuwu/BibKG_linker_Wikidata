# BibKG_Wikidata Linker

BibKG_Wikidata Linker is an initiative developed by Jorge Cerda, and guided by Professor Aidan Hogan. 
The project comprises a collection of methods created to establish a connection between [BibKG](https://bibkg.imfd.cl/), a knowledge graph centered around academic publications in the domain of computer science, and Wikidata, linking equivalent entities between both data sources.

The main objective of this project is to establish direct links between entities in BibKG and Wikidata, providing researchers with a reliable connection to a broader knowledge ecosystem. This integration unlocks a wealth of possibilities for analysis, cross-referencing, and gaining enriched insights, enabling researchers to explore academic publications in the field of computer science with a more comprehensive understanding.

Additionally, this project aims to expand the range of information accessible within BibKG, presenting an array of potential enhancements for the future. For example, with the data from Wikidata entities BibKG could incorporate external IDs from diverse data sources previously unavailable. 

The continuous growth and enrichment of BibKG will significantly augment the amount of information accessible to researchers, providing them with robust and extensive resources for their scholarly endeavors.

# Getting started

This project uses three main methods that allow obtaining links between BibKG and Wikidata:

## BibKG Parser

BiG Parser is a data parser that allows you to create a new BibKG file in JSON format, from the dump that has the MillenniumDB format. The resulting JSON file makes it easier to work with BibKG data when you want to work with a large amount of data.

To use this parser, you must follow the following steps:

1. Download BibKG dump [here](https://henryrosales.com/media/datasets/dblp_arnetminer_aligment.milldb.zip).
2. In 'BibKG_parser/bibkg_parser.py' file, change BibKG dump file path based on downloaded file location. It is highly recommended to have at least 8 GB of RAM available when performing the process. If you have 16 GB of RAM or more, it is recommended to modify the list of file parts in the 'BibKG_parser/bibkg_parser.py' file, in such a way that the process can be carried out faster in a single part (creating only one filename in the list). Also, note that the resulting JSON file will be created in the 'db/JSON/bibkg.py' path. If the previous folders do not exist, create those folders (or change the path to any desired position).
3. Run 'BibKG_parser/bibkg_parser.py' file. 

## Wikidata Parser

Wikidata Parser is a data preprocessor that allows Wikidata Linker to read Wikidata information more quickly, filtering entities from it and simplifying its structure. It should be noted that if you want to use Wikidata Linker using the original JSON file from the Wikidata dump, you will need to modify Wikidata Linker in such a way that it can correctly read the data from the Wikidata file.

To use this parser, you must follow the following steps:

1. Download Wikidata dump [here](https://dumps.wikimedia.org/wikidatawiki/entities/). You must download the file called 'latest-all.json.gz'.
2. Modify paths in the 'Wikidata_parser/wikidata_parser.py' file, if necessary.
3. Run 'Wikidata_parser/wikidata_parser.py' file.

## Wikidata Linker



## Data files


