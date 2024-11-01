import json

import os
import subprocess
import random



def slither_detector(slither_detector_name, project_location,json_output):
    print("gogo")
    hook_data = {
        "success": True,
        "error": None,
        "detector": f"{slither_detector_name}",
        "data": [
            # {
            #     "description": "",
            #     "markdown": "",
            #     "check": "",
            #     "impact": "",
            #     "confidence": ""
            # }
        ]
    }

    ####################################################################################################

    # Load the JSON data from the input file
    input_file_path = f'./{slither_detector_name}.json'
    output_file_path = f'./{json_output}.json'

    temp = f"{random.randint(0, 0xffffffff)}.json"
    #../engine/gamza-static/code/unichain
    ret = subprocess.run(["slither", project_location, "--detect", f"{','.join(slither_detector_name)}" ,"--json", temp], stdout=subprocess.DEVNULL).returncode
    print(["slither", project_location, "--detect", f"{slither_detector_name}" ,"--json", temp])

    with open(temp, 'r') as file:
        data = json.load(file)


    if data["success"] == True and len(data["results"]) == 0:
        hook_data["data"].append({"description": "No issues found"})
        
    else:
        for detection in data["results"]["detectors"]:
            p = {}
            p["description"] = detection["description"]
            p["markdown"] = detection["markdown"]
            p["check"] = detection["check"]
            p["impact"] = detection["impact"]
            p["confidence"] = detection["confidence"]
            hook_data["data"].append(p)
        if hook_data["data"].__len__() == 0:
            hook_data["success"] = False
            hook_data["error"] = "Slither test failed to run"

    with open(output_file_path, 'w') as output_file:
        json.dump(hook_data, output_file, indent=4)
    if os.path.exists(temp):
        os.remove(temp)
    return hook_data

def slither_detector_run():
    detectors = [
        "encode-packed-collision", "shadowing-state",
        "uninitialized-state","controlled-delegatecall",
        "delegatecall-loop", "msg-value-loop",
        "reentrancy-eth", "unchecked-transfer",
        "shadowing-abstract","divide-before-multiply"
    ]
    ret = {}
    src = os.path.dirname(os.path.abspath(__file__))
    code_path = os.path.join(src,'..', '..', '..', 'engine', 'gamza-static', 'code', 'unichain')
    ret = slither_detector(detectors, code_path , "slither_detector")
    return ret

# print(f"Parsed data saved to {output_file_path}")
if __name__ == "__main__":
    r = slither_detector_run()
    print(r)
