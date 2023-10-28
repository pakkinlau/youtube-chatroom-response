import re
from bs4 import BeautifulSoup

def extract_info(soup):
    """
    Extracts information from the given BeautifulSoup object.

    This function takes a BeautifulSoup object as input and extracts
    attribute information from the first tag within the soup. It also
    finds the first child of the base tag and returns information about
    it.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing HTML.

    Returns:
        dict: A dictionary containing attribute information of the base tag.
        Tag: The first child element of the base tag.
        int: The number of child elements under the base tag.
    """
    info_dict = {}
    base_tag = soup.find()  # Find the first tag within the soup

    if base_tag:
        attributes = base_tag.attrs  # Get all attributes of the tag

        for attr, value in attributes.items():
            if attr in info_dict:
                if isinstance(info_dict[attr], str):
                    info_dict[attr] = [info_dict[attr]]  # Convert existing value to a list
                info_dict[attr].append(value)
            else:
                info_dict[attr] = value

    childs_of_base_tag = soup.find()  # Find the first child
    num_of_child = len(childs_of_base_tag)

    return info_dict, childs_of_base_tag, num_of_child

element = """
<a id="sj_af3baf95cd788b8f" data-mobtk="1h7bas884jqkr800" data-jk="af3baf95cd788b8f" class="abc"><a id="abcda" class="ed">...</a></a>
"""
soup = BeautifulSoup(element, "html.parser")

info_dict, childs_of_base_tag, num_of_child = extract_info(soup)

print("The resulting dictionary is:", info_dict)
print("Number of child elements:", num_of_child) 
for index, child in enumerate(childs_of_base_tag, start=1):
    print(f"Child {index}: {child}")
