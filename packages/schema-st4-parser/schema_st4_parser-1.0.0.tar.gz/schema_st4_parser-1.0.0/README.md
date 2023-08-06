# Schema ST4 Python Parser

Parse [Schema St4](https://www.quanos-content-solutions.com/en/software/schema-st4) XML Files into simple,flat python objects.

## Installation

via pip: `pip install schema_st4_parser`

## Usage
Simply pass the xml file  into the parse methode. A list of St4Entry objects will be returned.

```pytohn
from schema_st4_parser import parse, St4Entry

entries = parse("MyFile.xml")
print(entries[0])
```