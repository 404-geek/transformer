from typing import List


def check_and_add_xml_header(data: List[str], start: int) -> List[str]:
    if start == 0 and len(data) and (not '<?xml' in data[0]):
        data.insert(0, '<?xml version="1.0" encoding="UTF-8"?>')
    return data