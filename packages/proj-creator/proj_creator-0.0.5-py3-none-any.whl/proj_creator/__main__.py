import os, argparse
from .template.template import get_license_str, get_framework, get_build_str, get_setup_str
from .lib import write_file





def gen(name, template, root_dir, add_license):
    if add_license:
        license = get_license_str()
        with open(os.path.join(root_dir, 'LICENSE'), 'w') as f:
            f.write(license)

    file_content_list = [
        ['.gitlab/build.yaml', get_build_str(template, name)],
        ['src/version.py', "__version__='0.0.1'"],
        ['src/__init__.py', "from .version import __version__"],
        ['.gitignore', '__pycache__\ndist\ndata\n*.egg-info\n.pypirc'],
        ['.gitlab-ci.yml', """
default:
  image: registry.cn-zhangjiakou.aliyuncs.com/wangxb/fastapi:vpc-control-test

stages:
  - unit-test
  - before-merge
  - publish

include:
  - local: '.gitlab/unit-test.yaml'
  - local: '.gitlab/build.yaml'
            """],
        ['src/domain/repository/base.py', 
         'from ddd_objects.domain.repository import Repository'],
        ['src/infrastructure/repository_impl/base.py', 
         'from ddd_objects.infrastructure.repository_impl import RepositoryImpl'],
        ['src/infrastructure/converter/base.py', 
         'from ddd_interface.infrastructure.converter import Converter'],
        ['unit_test/test_repo.py', """
import os, sys
try:
    import src
except ImportError:
    sys.path.append(os.getcwd())
         """],
        ['unit_test/test_ao.py', """
import os, sys
try:
    import src
except ImportError:
    sys.path.append(os.getcwd())
         """]
    ]
    for fn, s in file_content_list:
        write_file(root_dir, fn, s)


def ddd(args):
    name = args.name
    root_dir = args.root_dir
    template = args.template
    add_license = args.license
    
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    
    framework = get_framework(template)
    for fn, f_type in framework:
        fn = os.path.join(root_dir, fn)
        if f_type=='d':
            os.makedirs(fn)
        elif f_type=='f':
            with open(fn, 'w') as f:
                f.write('')
        else:
            raise ValueError(f'Wrong file type is set: {f_type}')

    gen(name, template, root_dir, add_license)



def lib(args):
    name = args.name
    root_dir = args.root_dir
    template = args.template
    add_license = args.license
    
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    
    framework = get_framework(template, name)
    for fn, f_type in framework:
        fn = os.path.join(root_dir, fn)
        if f_type=='d':
            os.makedirs(fn)
        elif f_type=='f':
            with open(fn, 'w') as f:
                f.write('')
        else:
            raise ValueError(f'Wrong file type is set: {f_type}')

    gen(name, template, root_dir, add_license)
    with open(os.path.join(root_dir, 'setup.py'), 'w') as f:
        f.write(get_setup_str(template, name))



def run():
    parser = argparse.ArgumentParser(description='Project creator')
    subparser = parser.add_subparsers(help='subcommand help')

    ddd_parser = subparser.add_parser('ddd', help='ddd project')
    ddd_parser.add_argument('--name', type=str, default='', help='project name')
    ddd_parser.add_argument('--root_dir', type=str, default='.', help='root dir')
    ddd_parser.add_argument('--template', type=str, default='base', help='project template')
    ddd_parser.add_argument('--license', action='store_true', help='add license file')
    ddd_parser.set_defaults(func=ddd)
    
    lib_parser = subparser.add_parser('lib', help='pip lib project')
    lib_parser.add_argument('--name', type=str, default='', help='project name')
    lib_parser.add_argument('--root_dir', type=str, default='.', help='root dir')
    lib_parser.add_argument('--template', type=str, default='lib', help='project template')
    lib_parser.add_argument('--license', action='store_true', help='add license file')
    lib_parser.set_defaults(func=lib)
    

    args = parser.parse_args()
    args.func(args)



if __name__=='__main__':
    run()