#!/usr/bin/python
import os
import pycountry
import csv
from pathlib import Path


def map_country_alpha2_to_country_name():
    """Return a dict of ISO Alpha2 country codes to country names."""
    return {x.alpha_2: x.name for x in pycountry.countries}


def create_country_mapping_CSV(destination,fields,map):
    """Convert dictionary to CSV with relevant fields."""
    try:
        with open(destination, 'w',newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            data = [dict(zip(fields, [k, v])) for k, v in map.items()]
            writer.writerows(data)
        print("\nINIT: External data source - Sourced from country dictionary API to CSV format (with relevant fields).")
    except IOError:
        print("I/O error")


def main():
    # create Path mappings to source files (OS-agnostic)
    raw_data_folder = Path(os.path.realpath('../raw data sources/'))
    countrymapping = raw_data_folder / "CountryMapping.csv"

    # CSV column names for mapping country codes
    fields = ['alpha_2', 'Country']

    # retrieve country mapping dictionary object from pycountry API
    map = map_country_alpha2_to_country_name()
    create_country_mapping_CSV(countrymapping,fields,map)


if __name__ == '__main__':
    main()
