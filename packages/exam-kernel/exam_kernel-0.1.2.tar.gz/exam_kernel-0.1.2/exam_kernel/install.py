import json
import argparse
import os
import tempfile
import sys
from jupyter_client.kernelspec import KernelSpecManager

kernel_json = {
    "argv": ["python", "-m",
             "exam_kernel", "-f",
             "{connection_file}"],
    "display_name": "ExamKernel",
    "name": "ExamKernel",
    "language": "python"
}

def install_exam_kernel(user=True, prefix=None):
    with tempfile.TemporaryDirectory() as tmp:
        os.chmod(tmp, 0o755)
        with open(os.path.join(tmp, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)
        KernelSpecManager().install_kernel_spec(tmp, 'exam_kernel', user=user, prefix=prefix)

def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False

def main(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument('--user', action='store_true',
        help='Install to the per-user kernels registry. Default if not root')

    parser.add_argument('--sys-prefix', action='store_true',
        help='Install to the sys.prefix.')

    args = parser.parse_args(argv)

    if args.sys_prefix:
        args.prefix = sys.prefix
    if not args.prefix and not _is_root():
        args.user = True


    install_exam_kernel(user=args.user, prefix=args.prefix)

if __name__ == '__main__':
    main()
    

