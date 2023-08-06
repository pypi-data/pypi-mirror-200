from typing import List, Dict, Optional, Union
from dataclasses import dataclass
import xml.etree.ElementTree as ET
import os

@dataclass(frozen=True)
class St4Entry():
    type:str
    label:str
    node_id:str
    link_id:str
    titles:Dict[str,str]
    content:Dict[str,str]
    thumbnail:Optional[str]=None
    data_web:Optional[Dict[str,str]]=None
    data_web_data:Optional[Dict[str,str]]=None
    
    @property
    def languages(self)->List[str]:
        if len(self.content) == 0:
            return list(self.titles.keys())
        return list(self.content.keys())
    
    
def get_namespaces(xml_file:Union[str, os.PathLike])->Dict[str,str]:
    """
    Extracts the namespaces from a schema st4 xml file
    """
    namespaces = {}
    for event, elem in ET.iterparse(xml_file, events=("start", "start-ns")):
        if event == "start-ns":
            prefix, url = elem
            namespaces[prefix] = url
    return namespaces

def parse(xml_file:Union[str, os.PathLike])->List[St4Entry]:
    """
    Parses a schema st4 xml file and returns a list of St4Entry objects
    """
    namespaces = get_namespaces(xml_file)
    assert "n" in namespaces and  "l" in namespaces , "No namespaces found! Is this a valid ST4 file?"
     
    extracted_entries=[]
    
    def extract_language_and_values(element:ET.Element,with_entry=False)->Dict[str,str]:
        extracted={}
        value_elements = element.findall("./n:Value",namespaces)
        for value_element in value_elements:
            language = value_element.attrib[(f"{'{'+namespaces['n']+'}'}Aspect")]
            if with_entry:
                entry_element = value_element.find(".//n:Entry",namespaces)
                if entry_element is not None:
                    extracted[language]=entry_element.text
            else:
                extracted[language]=value_element.text         
        return extracted
            
            
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Find all 'n:SystemFolder' elements
    system_folder_elements = root.findall(".//n:SystemFolder",namespaces)
    for system_folder_element in system_folder_elements:
        
        #get info elements
        
        info_elements = system_folder_element.findall(".//n:Data-Title/..",namespaces) #Just dont ask me why, but im not gonna hardcode the InfoType02 element 
        if info_elements is None:
            continue
        
        
        for info_element in info_elements:
            #extract label and ids
            type=info_element.tag
            label  = info_element.attrib[(f"{'{'+namespaces['l']+'}'}Label")]
            node_id =  info_element.attrib[(f"{'{'+namespaces['n']+'}'}Id")]
            link_id  = info_element.attrib[(f"{'{'+namespaces['l']+'}'}Id")]
            
            #extract the titles in all languages
            title_element = info_element.find(".//n:Data-Title",namespaces)
            titles=extract_language_and_values(title_element,with_entry=True)
            
            #get the content in all languages
            data_content_element = info_element.find(".//n:Data-Content",namespaces)
            content={}
            if data_content_element is not None:
                value_elements = data_content_element.findall("./n:Value",namespaces)
                
                for value_element in value_elements:
                    language = value_element.attrib[(f"{'{'+namespaces['n']+'}'}Aspect")]
                    content_element = value_element.find(".//n:Entry//content",namespaces)
                    content[language]= ET.tostring(content_element, encoding='unicode')
             
            #check if we got content or titles, if not, skip this entry         
            if len(titles)==0 and len(content)==0:
                continue
                       
            #get thumbnail if it exists
            thumbnail=None
            thumbnail_element = info_element.find(".//n:Data-Thumbnail",namespaces)
            if thumbnail_element is not None:
                thumbnail = thumbnail_element.text
                
            #get data web if it exists
            data_web = None
            data_web_element = info_element.find(".//n:Data-Web",namespaces)
            if data_web_element is not None:
                data_web = extract_language_and_values(data_web_element)
                
            # get data web.data if it exists // dont ask me why it is named this way, its just stupid
            data_web_data = None
            data_web_data_element = info_element.find(".//n:Data-Web.Data",namespaces)
            if data_web_data_element is not None:
                data_web_data = extract_language_and_values(data_web_data_element)
            
            extracted_entries.append(St4Entry(type,label,node_id,link_id,titles,content,thumbnail,data_web,data_web_data))
                
    return extracted_entries
    
    
    
    
    
    
