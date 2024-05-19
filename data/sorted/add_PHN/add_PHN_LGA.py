import json

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def transform_data(original_data):
    transformed_data = {}

    # Iterate through the original data structure
    for region, lgas in original_data.items():
        for lga, phns in lgas.items():
            if lga not in transformed_data:
                transformed_data[lga] = {}

            for phn, details in phns.items():
                if phn not in transformed_data[lga]:
                    transformed_data[lga][phn] = {}

                for period, diseases in details.items():
                    for disease, stats in diseases.items():
                        if disease not in transformed_data[lga][phn]:
                            transformed_data[lga][phn][period] = {}

                        # Construct the new record with additional LGA and PHN details
                        record = stats
                        record['LGA'] = lga
                        record['PHN'] = phn
                        transformed_data[lga][phn][period][disease] = record

    return transformed_data

def save_data(transformed_data, output_path):
    with open(output_path, 'w') as file:
        json.dump(transformed_data, file, indent=4)

def main():
    input_path = 'path_to_your_PM.json'  # Update this path to where your PM.json is stored
    output_path = 'path_to_your_output_file.json'  # Update this path to where you want to save the transformed data

    # Load original data
    original_data = load_data(input_path)
    
    # Transform the data
    transformed_data = transform_data(original_data)
    
    # Save the transformed data
    save_data(transformed_data, output_path)
    print("Data transformation completed and saved to", output_path)

if __name__ == "__main__":
    main()
