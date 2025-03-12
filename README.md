# Name Scrapper - crowdstrike exercise 

The app scrapes the following Wikipedia page: https://en.wikipedia.org/wiki/List_of_animal_names, extracts collateral adjectives and their corresponding animals, downloads an image for each animal, and outputs the results as an HTML file.

## How to Run

1. Create and activate the conda environment:
   ```
   conda env create -f environment.yml
   conda activate animal_names_env
   ```
2. Run the main program:
   ```
   python -m src.main
   ````

## Running tests
1. Ensure that dev dependencies are installed:
   ```
   pip install -r ./requirements-dev.txt
   ```
2. Run pytest:
   ```
   pytest
   ```
