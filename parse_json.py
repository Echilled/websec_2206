import json
import validator


def json_hash_indexer(location="WebHash.Json"):
    with open(location, "r") as file:
        try:
            index = {}
            data = json.load(file)
            for url, properties in data['URLs'].items():
                index[url] = properties['properties']['hash']
                # print(properties)
            return index
        except Exception as e:
            pass


def json_construct(id, hash, date, times_it_changed):
    website_dic = {id: {'properties': {}}}
    values = [{'hash': hash}, {'archival_date': date}, {'number of times URL content change': times_it_changed}]
    for val in values:
        website_dic[id]['properties'].update(val)
    return website_dic


def update_json(filename, data_dict):
    with open(filename, "w") as outfile:
        json_object = json.dumps(data_dict, indent=4)
        outfile.write(json_object)


def json_verifier(json_filename, decryption_password=123, ):
    properties_tuple = ("hash", "archival_date", "number of times URL content change")
    try:
        # json_filename = decrypt_file(json_filename, decryption_password)
        with open(json_filename, "r") as j_file:
            data = json.load(j_file)
            if type(data) is not dict or "URLs" not in data.keys():
                print("Ensure input file is in the correct format")
                return False
            else:
                for url, properties in data["URLs"].items():
                    if not validator.is_valid_url(url):
                        print("URLs may be missing or not in correct format, please check")
                        return False
                    key, value = list(properties.items())[0]
                    if key != 'properties':
                        print("properties for " + url + " not found, ensure file is in correct format")
                        return False
                    else:
                        if not {"hash", "archival_date", "number of times URL content change"} \
                               <= list(properties.values())[0].keys():
                            print("The missing keys for " + url + " are")
                            out = [k for k in properties_tuple if k not in list(properties.values())[0].keys()]
                            print(out)
                            print("Please ensure these properties are present")
                            return False
                        else:
                            print("checks completed")
                            return True
                        # prop_values = list(properties.values())[0].keys()
                        # print(list(prop_values))

    except ValueError as e:
        print("Invalid json")
        print(e)
    except TypeError as t:
        print("Invalid json")
        print(t)


def main():
    json_verifier("WebHash.Json")


if __name__ == "__main__":
    main()


