import sys
import logging as log
from collections import defaultdict
from utils import report, all_files_by_ext

from openvino.frontend import FrontEndManager as fem

log.basicConfig(format='[ %(levelname)s ]  %(msg)s', level='INFO')


def per_model_collect(manager: fem, model_path: str) -> [defaultdict, str]:
    ops = defaultdict(int)

    frontend = manager.load_by_model(model_path)
    if frontend is None:
        err_msg = "Suitable FrontEnd wasn't found"
        log.error(err_msg)
        return ops, err_msg

    try:
        fe_input_model = frontend.load(model_path)
        model = frontend.decode(fe_input_model)
    except Exception as e:
        err_msg = str(e).strip()
        log.error(err_msg)
        return ops, err_msg

    for op in model.get_ops():
        if 'Framework' in op.get_type_name():
            attrs = op.get_attributes()
            op_type = ".".join([attrs[attr] for attr in sorted(attrs) if 'type' in attr or 'domain' in attr])
        else:
            op_type = op.get_type_name()
        if not op_type:
            log.error("Operation type is empty for node: {}".format(op))
        ops[op_type] += 1
    return ops, ""


if __name__ == '__main__':
    argv = sys.argv

    if len(argv) != 3:
        print("usage example:")
        print("{} {} /path/to/directory extension".format(sys.executable, argv[0]))
        sys.exit(1)

    directory = argv[1]
    extension = argv[2]

    ops_per_model, summary, errors = dict(), defaultdict(int), dict()

    manager = fem()

    all_files = all_files_by_ext(directory, extension)
    for i, path in enumerate(all_files):
        log.info("{}/{} {}".format(i + 1, len(all_files), path))
        ops, err = per_model_collect(manager, path)
        ops_per_model[path] = ops
        for op_name, op_num in ops.items():
            summary[op_name] += op_num
        if err:
            errors[path] = err

    report(ops_per_model, summary, errors)
