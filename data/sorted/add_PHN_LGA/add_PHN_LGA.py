'''
-----------Team 48------------
| Name          | Student ID |
|---------------|------------|
| Yifei ZHANG   | 1174267    |
| Yibo HUANG    | 1380231    |
| Hanzhang SUN  | 1379790    |
| Liyang CHEN   | 1135879    |
| Yueyang WU    | 1345511    |
'''

import json

def load_data(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def restructure_data(data):
    """Restructure the data according to the correct PHN and LGA hierarchy."""
    new_structure = []

    # Iterate through each PHN and its LGAs
    for phn, lgas in data.items():
        for lga, details in lgas.items():
            for period, diseases in details.items():
                if not isinstance(diseases, dict):
                    continue  # Skip non-dict items to ensure correct handling
                for disease, stats in diseases.items():
                    if not isinstance(stats, dict):
                        continue  # Skip non-dict items to ensure correct handling
                    # Build the new entry for each disease under each period
                    entry = {
                        "PHN": phn,
                        "LGA": lga,
                        "Period": period,
                        "Disease": disease,
                        "ASR": stats.get("ASR"),
                        "SR": stats.get("SR"),
                        "NUM": stats.get("NUM")
                    }
                    new_structure.append(entry)

    return new_structure

def save_data(data, file_path):
    """Save the restructured data to a new JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    original_data = load_data('PM.json')
    restructured_data = restructure_data(original_data)
    save_data(restructured_data, 'newPM.json')

if __name__ == "__main__":
    main()
