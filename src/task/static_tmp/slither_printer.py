import json
import os
import subprocess
import random



def slither_printer(hook_contract, code_location ,slither_test_name, json_output):
    hook_data = {
        "contract": hook_contract,
        "success": True,
        "error": None,
        "data": [
        ]
    }
    ####################################################################################################
    # Load the JSON data from the input file
    output_file_path = f'./{json_output}.json'

    temp = f"{random.randint(0, 0xffffffff)}.json"
    print(temp)
    ret = subprocess.run(["slither", code_location, "--print", f"{','.join(slither_test_name)}" ,"--json", temp], stdout=subprocess.DEVNULL).returncode
    print(ret)
    print(["slither", code_location, "--print", f"{','.join(slither_test_name)}" ,"--json", temp])
    with open(temp, 'r') as file:
        data = json.load(file)


    for printer in data["results"]["printers"]:
        q = {
                "printer": "",
                "fields_names": [],
                "result": []
            }
        for element in printer["elements"]:
            if element["type"] == "pretty_table" and element["name"]["name"] == hook_contract:
                rows = element["name"]["content"]["rows"]
                fields_names = element["name"]["content"]["fields_names"]
                for row in rows:
                    p = {}
                    for i in range(len(fields_names)):
                        e = row[i]
                        p[fields_names[i]] = e
                    q["printer"] = printer["printer"]
                    q["result"].append(p)
                    q["fields_names"] = fields_names
        hook_data["data"].append(q)

    if hook_data["data"].__len__() == 0:
        hook_data["success"] = False
        hook_data["error"] = "Slither test failed to run"


    with open(output_file_path, 'w') as output_file:
        json.dump(hook_data, output_file, indent=4)

    if os.path.exists(temp):
        os.remove(temp)
    return hook_data
def slither_printer_run(contractName):
    printer_list = ["require", "modifiers", "vars-and-auth"]
    src = os.path.dirname(os.path.abspath(__file__))
    code_path = os.path.join(src, '..','..', '..', 'engine', 'gamza-static', 'code', 'unichain')
    r = slither_printer(contractName, "{}".format( code_path ),printer_list, contractName )
    return r

# print(f"Parsed data saved to {output_file_path}")
if __name__ == "__main__":
    r = slither_printer_run("TakeProfitsHook")
    print(r)
