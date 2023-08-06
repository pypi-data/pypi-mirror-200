from src.schema_st4_parser import get_namespaces
import io
import pytest

def test_should_parse_namespaces_from_valid_input():
    valid_string = '''
    <d:xie d:version="12.0.3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:n="http://www.schema.de/2004/ST4/XmlImportExport/Node" xmlns:d="http://www.schema.de/2004/ST4/XmlImportExport/Data" xmlns:l="http://www.schema.de/2004/ST4/XmlImportExport/Link" xmlns:m="http://www.schema.de/2004/ST4/XmlImportExport/Meta" m:Dimension-GuiLanguage="de" m:Dimension-Sprache="de" xsi:schemaLocation="http://www.schema.de/2004/ST4/XmlImportExport/Node schemas/node.xsd http://www.schema.de/2004/ST4/XmlImportExport/Data schemas/data.xsd http://www.schema.de/2004/ST4/XmlImportExport/Link schemas/link.xsd">
    </d:xie>
    '''
    file = io.StringIO(valid_string)
    result = get_namespaces(file)
    assert "n" in result  
    assert "l" in result
    assert "d" in result
    assert "xsi" in result
    
def test_should_raise_exception_from_invalid_input():
    invalid_string = '''
    <d:xie d:version="12.0.3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:n="http://www.schema.de/2004/ST4/XmlImportExport/Node" xmlns:d="http://www.schema.de/2004/ST4/XmlImportExport/Data" xmlns:l="http://www.schema.de/2004/ST4/XmlImportExport/Link" xmlns:m="http://www.schema.de/2004/ST4/XmlImportExport/Meta" m:Dimension-GuiLanguage="de" m:Dimension-Sprache="de" xsi:schemaLocation="http://www.schema.de/2004/ST4/XmlImportExport/Node schemas/node.xsd http://www.schema.de/2004/ST4/XmlImportExport/Data schemas/data.xsd http://www.schema.de/2004/ST4/XmlImportExport/Link schemas/link.xsd">
    '''
    file = io.StringIO(invalid_string)
    with pytest.raises(Exception):
        result = get_namespaces(file)
