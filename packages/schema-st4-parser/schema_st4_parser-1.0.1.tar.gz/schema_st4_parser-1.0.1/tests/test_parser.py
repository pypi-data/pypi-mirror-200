from src.schema_st4_parser import St4Entry, parse, get_namespaces

def test_can_parse_file():
    results = parse("./tests/test.xml")
    assert len(results) == 1
    result = results[0]
    assert isinstance(result, St4Entry)
    assert result.label == "label"
    assert result.node_id == "nID"
    assert result.link_id == "lID"
    assert result.titles["en"] == "title_en"
    assert result.titles["de"] == "title_de"
    assert "en" in result.content
    assert "de" in result.content
    assert result.thumbnail == "thumbnail"
    assert "GraficResource" in result.type
    assert result.data_web["en"] == "data_web_en"
    assert result.data_web["de"] == "data_web_de"
    assert result.data_web_data["en"] == "data_web_data_en"
    assert result.data_web_data["de"] == "data_web_data_de"
    
    
    