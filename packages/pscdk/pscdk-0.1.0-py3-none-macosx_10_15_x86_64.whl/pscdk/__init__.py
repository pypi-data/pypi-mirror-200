import os
import sys
import subprocess
import shlex
import platform
import tempfile
import shutil
import argparse
import eoscdt
from .wasm_checker import check_import_section

__version__ = "0.2.5"

src_dir = os.path.dirname(__file__).replace('\\', '/')
eoscdt_dir = os.path.dirname(eoscdt.__file__)


#https://stackabuse.com/how-to-print-colored-text-in-python/
#https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[1;33;40m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def find_target_dir():
    cur_dir = os.path.abspath(os.curdir)
    target_dir = os.path.join(cur_dir, 'target')
    target_dir = target_dir.replace('\\', '/')
    return target_dir

def print_err(msg):
    print(f'{FAIL}:{msg}{ENDC}')

def print_warning(msg):
    print(f'{WARNING}:{msg}{ENDC}')

def build_contract(package_name, build_mode, target_dir, stack_size):
    os.environ['RUSTFLAGS'] = f'-C link-arg=-zstack-size={stack_size} -Clinker-plugin-lto'
    cmd = fr'cargo +nightly build --target=wasm32-wasi --target-dir={target_dir} -Zbuild-std --no-default-features {build_mode} -Zbuild-std-features=panic_immediate_abort'
    print(cmd)
    cmd = shlex.split(cmd)
    ret_code = subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr)
    if not ret_code == 0:
        sys.exit(ret_code)

    try:
        check_import_section(f'{target_dir}/wasm32-wasi/release/{package_name}.wasm')
    except Exception as e:
        print_err(f'{e}')
        sys.exit(-1)

    if shutil.which('wasm-opt'):
        cmd = f'wasm-opt {target_dir}/wasm32-wasi/release/{package_name}.wasm -O3 --strip-debug -o {target_dir}/{package_name}.wasm'
        cmd = shlex.split(cmd)
        ret_code = subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr)
        if not ret_code == 0:
            sys.exit(ret_code)

def run_builder():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')

    init = subparsers.add_parser('init')
    init.add_argument('project_name')

    build = subparsers.add_parser('build')
    build.add_argument('-o', '--output', default='', help='output file name')
    build.add_argument('input', type=str, help='input file')

    result, others = parser.parse_known_args()
    if not result:
        parser.print_usage()
        sys.exit(-1)
    if result.subparser == "init":
        project_name = result.project_name
        files = {}
        for file_name in ['build.sh', 'test.sh', 'hello.codon', 'test.py', 'pytest.ini']:
            with open(f'{src_dir}/templates/init/{file_name}', 'r') as f:
                if file_name == 'hello.codon':
                    file_name = f'{project_name}.codon'
                files[file_name] = f.read().replace('{{name}}', project_name)
        try:
            os.mkdir(project_name)
            for file in files:
                file_path = f'{project_name}/{file}'
                with open(file_path, 'w') as f:
                    f.write(files[file])
                if file.endswith('.sh'):
                    if not 'Windows' == platform.system():
                        os.chmod(file_path, 0o755)
        except FileExistsError as e:
            print_err(f'{FAIL}: {e}')
            sys.exit(-1)
    elif result.subparser == "build":
        if not result.input:
            parser.print_usage()
            sys.exit(-1)
        linker_flags = f'-L{src_dir}/codon/lib/codon -lcodonrt-wasm32 -L{src_dir}/codon/lib -lc++ -lc'
        others = ' '.join(others)
        if result.output:
            cmd = f'{src_dir}/codon/bin/codon build --release {others} --march=wasm32 --linker-flags="{linker_flags}" -o {result.output} {result.input}'
        else:
            cmd = f'{src_dir}/codon/bin/codon build --release {others} --march=wasm32 --linker-flags="{linker_flags}" {result.input}'
        print(cmd)
        cmd = shlex.split(cmd)
        ret_code = subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr)
        if not ret_code == 0:
            sys.exit(ret_code)
        try:
            if result.output:
                output = result.output
            else:
                output = result.input.replace('.codon', '.wasm')
            check_import_section(output)

            if shutil.which('wasm-opt'):
                shutil.copy(output, f'{output}.orig')
                cmd = f'wasm-opt {output} -O3 --strip-debug -o {output}'
                cmd = shlex.split(cmd)
                ret_code = subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr)
                if not ret_code == 0:
                    sys.exit(ret_code)
            else:
                # shutil.copy(f'{target_dir}/wasm32-wasi/release/{package_name}.wasm', f'{target_dir}/{package_name}.wasm')
                print_warning('''
        wasm-opt not found! Make sure the binary is in your PATH environment.
        We use this tool to optimize the size of your contract's Wasm binary.
        wasm-opt is part of the binaryen package. You can find detailed
        installation instructions on https://github.com/WebAssembly/binaryen#tools.
        There are ready-to-install packages for many platforms:
        * Debian/Ubuntu: apt-get install binaryen
        * Homebrew: brew install binaryen
        * Arch Linux: pacman -S binaryen
        * Windows: binary releases at https://github.com/WebAssembly/binaryen/releases''')
        except Exception as e:
            print_err(f'{e}')
            sys.exit(-1)

if __name__ == '__main__':
    run_builder()
