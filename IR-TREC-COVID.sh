#!/bin/bash
python3 src/getData.py
python3 src/indexer.py -af 'all'
python3 src/searcherf1.py
python3 src/searcherf2.py
python3 src/searcherf3.py