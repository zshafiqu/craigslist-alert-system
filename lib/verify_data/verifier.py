class Verifier:

    def __init__(self):
        pass

    def get_data_from_file(self, file_path):
        # Load a JSON file into a Python dictionary that 
        # can live on memory temporarily
        try:
            import json
            with open(file_path) as f:
                payload = json.load(f)
            return payload
        except Exception as e:
            return []

    def filter_new_items(self, existing_data, new_data):
        # Creates a set of the existing items, and then
        # does a lookup with the new data to see if there's
        # anything that is not in the existing data.. if so
        # return that, as its a new item that needs to be mailed
        temp = set()
        results = []

        for item in existing_data:
            temp.add(item["post-id"])

        for item in new_data:
            if item["post-id"] not in temp:
                results.append(item)

        return results

    def write_to_json_file(self, json_data, file_path):
        # Write any Python dict to a JSON file using this interface
        import json
        with open(file_path, "w") as w:
            json.dump(json_data, w)
        return None


        
    

    