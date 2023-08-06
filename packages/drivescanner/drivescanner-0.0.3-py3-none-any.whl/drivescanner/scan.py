import multiprocessing
from multiprocessing import Pool
import subprocess
from drivescanner import file_index, ingest, rules
from typing import Tuple


def _scan_file(file_tuple: tuple, NER: bool = False) -> Tuple[str, dict]:
    """
    It takes a tuple of a file name and a dictionary of file information, reads the file, and then
    updates the dictionary with the results of the file scan
    
    Args:
      file_tuple (Tuple): Tuple
    
    Returns:
      A tuple of the dictkey and the file_dict
    """
    # input test before we go
    assert isinstance(file_tuple, tuple), "Input should be a tuple"

    dictkey = file_tuple[0]
    file_dict = file_tuple[1]

    content, errormsg = ingest.ingest_file(file_dict["filepath"])

    # unsync file from OneDrive (unclear if it works for other cloud providers)
    subprocess.run('attrib +U -P "' + file_dict["filepath"] + '"')

    if content is None:
        file_dict["content_processed"] = False
        file_dict["processing_error"] = errormsg
    else:
        file_dict["content_processed"] = True
        
        if NER == True:  
            file_dict["entities"] = rules.extract_NER(content, NER_select=["PERSON"])
            rules_dict = rules.search_text_file(content)
            file_dict.update(rules_dict)
        else:    
            rules_dict = rules.search_text_file(content)
            file_dict.update(rules_dict)

    return (dictkey, file_dict)


def scan_drive(list_files: list[str], NER: bool = False) -> dict:
    """
    It takes a list of files, creates a dictionary of those files, then uses the multiprocessing library
    to scan each file in parallel
    
    Args:
      list_files (list[str]): list[str]
    
    Returns:
      A dictionary of dictionaries.
    """
    resultdict = file_index.create_file_dict(list_files=list_files)

    pool = Pool(multiprocessing.cpu_count())
    results = pool.starmap(_scan_file, [(i, NER) for i in resultdict.items()] )

    return dict(results)
