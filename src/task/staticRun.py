import os
import sys
from pprint import pprint
import subprocess



def staticRun(timeHash, hook):    
    src = os.path.dirname(os.path.abspath(__file__))
    engine_path = os.path.join(src, '..', '..', 'engine', 'gamza-static', 'lib')
    print(engine_path)
    sys.path.append(engine_path)
    from utils.paths import rule_rel_path_by_name
    from engine import layer_0
    from etherscan.unichain import store_foundry_toml, store_remappings, store_all_dependencies, foundry_dir
    from parser.layer_2 import get_variables
    from parser.run_semgrep import get_semgrep_output           
    
    dirs = os.path.join(src, '..')
    os.chdir("../../engine/gamza-static/")
    
    ret = {}   
    # _address: str = "0x38EB8B22Df3Ae7fb21e92881151B365Df14ba967"  # Uniswap v4 PoolManager in unichain
    #_address: str = "0x7d61d057dD982b8B0A05a5871C7d40f8b96dd040"  # Entropy First Initialized Hook in unichain
    _address: str = hook

    _paths = store_all_dependencies(_address)
    store_remappings(_address)
    store_foundry_toml()

    _diff = layer_0.format_code(foundry_dir)  # "code/unichain" directory
    # print(_diff)

    # linting the target contract recursively lints all dependencies
    _res: list[str] = layer_0.lint_code(_paths[0])
    # print(res)

    # to run semgrep rules,
    # path needs to start with "code"
    _target_path = os.path.join(foundry_dir, _paths[0])

    _output_l1: list = get_semgrep_output(
        rule_rel_path_by_name("misconfigured-Hook"),
        _target_path,
        False
    )


    _output_l2: list = get_semgrep_output(
        rule_rel_path_by_name("info-variable"),
        _target_path,
        False
    )

    ret["misconfigured-Hook"] = _output_l1
    ret["info-variable"] = _output_l2
    ret["slither_pass"] = _res[0].split("\n")
    ret["slither_fail"] = _res[1].split("\n")
    _output_d: dict = get_variables(_target_path)
    ret["output"] = _output_d

    ret["__path"] = _paths
    os.chdir(dirs)
    return ret