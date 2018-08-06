from os import listdir
from bs4 import BeautifulSoup
import re

# Constants
LOCAL_DATA_PATH = "./data/"

class CardDetails:
  def __init__(self, condition, price, quantity):
    self.condition = condition
    self.price = price
    self.quantity = quantity

class Card:
  def __init__(self, name, url, magic_block, magic_set, card_variants):
    self.name = name
    self.url = url
    self.magic_block = magic_block
    self.magic_set = magic_set
    self.card_variants = card_variants

def get_all_file_names_from_path(path):
  """Returns all of the file names in the specified path with the path prepended"""
  print("Local directory \"{}\" has \"{}\" different files.".format(path,
      len(listdir(path))))
  return [path + file_name for file_name in listdir(path)]

def read_contents(file_name):
  """Open the file specified and return the BeautifulSoup obj of it to the caller"""
  with open(file_name, 'r') as f:
    print("Opening file \"{}\".".format(file_name))
    return BeautifulSoup(f.read(), "lxml")

def split_content_into_rows(file_content):
  """Split the contents of the file into rows (which each hold an individual card's
     information) and return it to the caller"""
  even_rows = file_content.find_all("tr", "even product")
  odd_rows = file_content.find_all("tr", "odd product")
  return even_rows + odd_rows

def parse_url(section):
  """Parse the url out of the section, it is assumed the section that is given
     to this function is the correct one"""
  link = section.find("a", "highslide thumbnail")
  return link["href"]

def parse_name_and_printing(section):
  name = section.find("a", "name")
  href = name["href"]
  if "magic_singles" in href:
    regex = "/catalog/.*?-(.*?)-(.*?)/"
    matches = re.search(regex, href)
    magic_block = matches.group(1)
    magic_set = matches.group(2)
  else:
    regex = "/catalog/(.*?)/"
    matches = re.search(regex, href)
    magic_block = "Stand Alone Sets"
    magic_set = matches.group(1)
  return (name.contents[0], magic_block, magic_set)

def parse_variants(section):
  card_variants = []
  variants = section.find_all("tr", "variantRow")
  if len(variants) is not 0:
    for variant in variants:
      condition = variant.find("td", "variantInfo").contents[0].strip()
      price = variant.find("td", "price").contents[0].strip()
      quantity = variant.find_all("td")[2].contents[0].strip()
      card_details = CardDetails(condition, price, quantity)
      card_variants.append(card_details)
  else:
    # TODO: Need to fix a bug here
    pass
  return card_variants

def parse_card(section):
  card_name, magic_block, magic_set = parse_name_and_printing(section)
  card_variants = parse_variants(section)
  return (card_name, magic_block, magic_set, card_variants)

def parse_content(file_content):
  """Break the file contents into only meaningful data"""
  cards = []
  rows = split_content_into_rows(file_content)
  print("Current file has \"{}\" different cards.".format(len(rows)))
  for row in rows:
    # There are two tds in each row, one with the url information and one with the
    # card variant details
    card_sections = row.find_all("td")
    card_url = parse_url(card_sections[0])
    card_name, magic_block, magic_set, card_variants = parse_card(card_sections[1])
    card = Card(card_name, card_url, magic_block, magic_set, card_variants) 
    """
    print(card.name)
    print(card.url)
    print(card.magic_block)
    print(card.magic_set)
    print(card.card_variants[0].condition)
    print(card.card_variants[0].price)
    print(card.card_variants[0].quantity)
    """
    cards.append(card)
  return cards

if __name__ == "__main__":
  """The main function which drives the program"""
  # 1. Get all of the files names from the specified directory
  file_names = get_all_file_names_from_path(LOCAL_DATA_PATH)
  # 2. Loop over each file name, opening each one to read it's contents
  for file_name in file_names:
    file_content = read_contents(file_name)
    # 3. Parse the contents of the file
    cards = parse_content(file_content)
