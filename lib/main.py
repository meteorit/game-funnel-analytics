#!/usr/bin/python

import retrieveCountryMapping as rcm
import populateDatabase as pd


def main():
    """Run module scripts to (re)process datasets and (re)generate the Sqlite database."""
    rcm.main()
    pd.main()


if __name__ == '__main__':
    main()
