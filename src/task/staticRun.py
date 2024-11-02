import os
import sys
import json
import shutil
from .static_tmp.slither_detector import slither_detector_run
from .static_tmp.slither_printer import slither_printer_run
import subprocess
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

def semgrep_raw(src):
    cmd = 'semgrep --config "p/smart-contracts" {} --emacs'.format(src)
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res
def staticRunByCode(timeHash,codeHash, src):
    from layers.Loader import Loader
    from attr import asdict
    response = {}
    response["timeHash"] = timeHash
    response["codeHash"] = codeHash
    code = Loader().read_code(src)
    assert len(code) > 0
    print(src)
    code = Loader().read_code(src)
    assert len(code) > 0
    from layers.Aggregator import Aggregator
    aggregator = Aggregator()
    res = aggregator.aggregate(code)
    # can store the result as json using attr
    from attr import asdict
    import json

    # _path = Loader().read_code(f"{file_name}.sol")
    _path = Loader().read_code(src)
    res = get_analysis_result_with_threats(_path, get_model_suite())
    response["result"] = asdict(res, recurse=True)
    from engine.run_semgrep import run_semgrep_one
    semgrep_res = semgrep_raw(src)
    response["semgrep"] = semgrep_res.stdout #run_semgrep_one("", src)#이름 비우면 에러남
    response["mode"] = 4
    return response

'''
[2024-11-03 03:02:03,334: ERROR/MainProcess] Task task.tasks.static_by_code[b163fe20-20ba-437a-bf71-fe6332565349] raised unexpected: KeyError('')
Traceback (most recent call last):
  File "/Users/sori/backend/api/lib/python3.12/site-packages/celery/app/trace.py", line 453, in trace_task
    R = retval = fun(*args, **kwargs)
                 ^^^^^^^^^^^^^^^^^^^^
  File "/Users/sori/backend/api/lib/python3.12/site-packages/celery/app/trace.py", line 736, in __protected_call__
    return self.run(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/sori/backend/api/fix-run/src/task/tasks.py", line 223, in static_by_code
    tmp = staticRunByCode(timeHash, codeHash,src)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/sori/backend/api/fix-run/src/task/staticRun.py", line 139, in staticRunByCode
    response["semgrep"] = run_semgrep_one("", src)
                          ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/sori/backend/api/fix-run/src/task/../../engine/gamza-static/lib/engine/run_semgrep.py", line 38, in run_semgrep_one
    _msg_raw_schema = read_message_schema_by_rule_name(_rule_name)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/sori/backend/api/fix-run/src/task/../../engine/gamza-static/lib/engine/run_semgrep.py", line 13, in read_message_schema_by_rule_name
    return read_rule_by_name(_rule_name)["message"]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/sori/backend/api/fix-run/src/task/../../engine/gamza-static/lib/engine/run_semgrep.py", line 18, in read_rule_by_name
    with open(f"rules/{rule_rel_path_by_name(_rule_name)}", "r") as f:
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/sori/backend/api/fix-run/src/task/../../engine/gamza-static/lib/utils/paths.py", line 18, in rule_rel_path_by_name
    class_name = "info" if "info-" in rule_name else rules["class"][rule_name]
                                                     ~~~~~~~~~~~~~~^^^^^^^^^^^
KeyError: ''
'''