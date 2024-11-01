import os
import sys
import json
import shutil
from .static_tmp.slither_detector import slither_detector_run
from .static_tmp.slither_printer import slither_printer_run

def base_paths(x: str) -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), x))

# to run `python main.py` in root dir, add path of library to sys.path
src = os.path.dirname(os.path.abspath(__file__))

engine_path = os.path.join(src, '..', '..', 'engine', 'gamza-static', 'lib')
sys.path.append(engine_path)
engine_path = os.path.join(src, '..', '..', 'engine', 'gamza-static')
sys.path.append(engine_path)
project_root = base_paths("../../engine/gamza-static")
origin = base_paths(".")


import engine.foundry
import engine.slither

from utils.unichain import store_foundry_toml, store_remappings, store_all_dependencies, get_contract_json
from utils import foundry_dir

from custom_rules import get_model_suite
from layers.Aggregator import ThreatDetectionResult, ThreatModelBase, Aggregator
from layers.dataclass.Components import SimpleDetectionLog


def get_analysis_result_with_threats(code: str, models: list[ThreatModelBase]) -> ThreatDetectionResult:
    if not models:
        raise ValueError("No models provided")
    _res: ThreatDetectionResult = ThreatDetectionResult(
        info=Aggregator().aggregate(code),
        threats=[]
    )
    for model in models:
        detection_log = model.run(code)
        if detection_log and len(detection_log.scopes) > 0:
            _res.threats.append(SimpleDetectionLog.from_log(detection_log))
    return _res


def staticRun(timeHash, hook):
    shutil.rmtree("/app/engine/gamza-static/code/unichain", ignore_errors=True)
    os.chdir(engine_path)
    _address = hook
    contract_json = get_contract_json(_address)
    _paths = store_all_dependencies(_address)
    store_remappings(_address)
    store_foundry_toml()

    _diff = engine.foundry.format_code(foundry_dir)  # "code/unichain" directory
    # print(_diff)

    # linting the target contract recursively lints all dependencies
    _res: tuple[str, str] = engine.slither.lint_code(_paths[0])
    # print(res)

    from layers.Loader import Loader
    # code in "code/*" dir can simply be read by Loader
    file_name = contract_json["name"]
    tmp_path = contract_json["file_path"]
    print(bytes(file_name, 'utf-8'))
    code = Loader().read_code(f"/app/engine/gamza-static/code/unichain/{tmp_path}")
    assert len(code) > 0
    print(_paths[0].split("/")[1])  
    # can also read code from absolute path

    # file_path = os.path.join(engine_path, "code", "{}.sol".format(file_name))
    file_path = f"/app/engine/gamza-static/code/unichain/{tmp_path}"
    print(file_path)
    code = Loader().read_code(file_path)
    assert len(code) > 0

    from layers.Aggregator import Aggregator
    aggregator = Aggregator()
    res = aggregator.aggregate(code)

    # can store the result as json using attr
    from attr import asdict
    import json
    json.dump(asdict(res, recurse=True), open(f"out/{file_name}.json", "w"), indent=4)

    # _path = Loader().read_code(f"{file_name}.sol")
    _path = Loader().read_code(f"/app/engine/gamza-static/code/unichain/{tmp_path}")
    res = get_analysis_result_with_threats(_path, get_model_suite())
    print("this")
    print(res)
    assert type(res) == ThreatDetectionResult
    outfile = "out/{}_{}_{}.json".format(123,123,file_name)
    print(outfile)
    with open(outfile, "w") as f:
        json.dump(asdict(res, recurse=True), f, indent=4)
    print("end")
    os.chdir(origin)
    print("asd")

    response = {}
    response["timeHash"] = timeHash
    response["hooks"] = hook
    response["result"] = asdict(res, recurse=True)
    response["slither"] = {}
    response["slither"]["detector"] = slither_detector_run()
    response["slither"]["printer"] = slither_printer_run(_paths[0].replace("src/","").replace(".sol",""))
    response["mode"] = 3


    
    return response