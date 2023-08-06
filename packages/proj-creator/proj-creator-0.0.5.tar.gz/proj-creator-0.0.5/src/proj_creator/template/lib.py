def get_lib_framework(name):
    name = name.replace('-', '_')
    return [
        ['.gitlab', 'd'],
        ['.gitlab/build.yaml', 'f'],
        ['.gitlab/unit-test.yaml', 'f'],
        ['unit_test', 'd'],
        ['.gitignore', 'f'],
        ['.gitlab-ci.yml', 'f'],
        ['src', 'd'],
        [f'src/{name}/application', 'd'],
        [f'src/{name}/application/__init__.py', 'f'],
        [f'src/{name}/domain', 'd'],
        [f'src/{name}/domain/__init__.py', 'f'],
        [f'src/{name}/infrastructure', 'd'],
        [f'src/{name}/infrastructure/__init__.py', 'f'],
        [f'src/{name}/settings.py', 'f'],
        [f'src/{name}/__init__.py', 'f'],
        [f'src/{name}/version.py', 'f'],
        [f'src/{name}/application/action', 'd'],
        [f'src/{name}/application/action/__init__.py', 'f'],
        [f'src/{name}/application/assembler', 'd'],
        [f'src/{name}/application/assembler/__init__.py', 'f'],
        [f'src/{name}/application/dto', 'd'],
        [f'src/{name}/application/dto/__init__.py', 'f'],
        [f'src/{name}/domain/entity', 'd'],
        [f'src/{name}/domain/entity/__init__.py', 'f'],
        [f'src/{name}/domain/repository', 'd'],
        [f'src/{name}/domain/repository/__init__.py', 'f'],
        [f'src/{name}/domain/value_obj', 'd'],
        [f'src/{name}/domain/value_obj/__init__.py', 'f'],
        [f'src/{name}/infrastructure/converter', 'd'],
        [f'src/{name}/infrastructure/converter/__init__.py', 'f'],
        [f'src/{name}/infrastructure/ao', 'd'],
        [f'src/{name}/infrastructure/ao/__init__.py', 'f'],
        [f'src/{name}infrastructure/do', 'd'],
        [f'src/{name}infrastructure/do/__init__.py', 'f'],
        [f'unit_test/test_ao.py', 'f']
    ]

def get_lib_build_str(name):
    name = name.replace('_', '-')
    name2 = name.replace('-', '_')
    return f"""
add-tag:
  image: registry.cn-shanghai.aliyuncs.com/wangxb/git
  stage: publish
  only:
    refs:
      - dev
    changes:
      - src/{name2}/version.py
  except:
    - pipelines
  script:
    - ls
    - VERSION=$(cat src/{name2}/version.py | grep __version__)
    - VERSION=${{VERSION#*\\'}}
    - VERSION=${{VERSION%\\'*}}
    - git remote remove origin
    - git remote add origin https://"$GIT_USERNAME:$GIT_PASSWORD"@git.dhel.top/wangziling100/{name}.git
    - git config user.name gitlab-ci
    - git config user.email example@gitlab.com
    - git tag -a $VERSION -m "Version created by gitlab-ci Build"
    - git push --tags
  allow_failure: false
  tags:
    - tiny

build-release:
  image: registry-vpc.cn-zhangjiakou.aliyuncs.com/wangxb/python:build
  stage: publish
  variables:
    IS_BUILD_MODE: "1"
  only:
    refs:
      - dev
    changes:
      - src/{name2}/version.py
  except:
    - pipelines
  script:
    - python3 -m build
    - python3 -m twine upload --non-interactive -u __token__ -p $PYPI_TOKEN dist/*
  allow_failure: false
  timeout: 5 minutes
  retry: 2
  tags:
    - tiny
    """

def get_lib_setup_str(name):
    name2 = name.replace('-', '_')
    return f"""
from setuptools import setup, find_packages
version_fn = 'src/{name2}/version.py'
with open(version_fn, 'r') as f:
    verstr = f.read()
version = verstr.split('=')[1]
version = version.replace("'", "").strip()


setup(
    name="{name}",
    version=version,
    author="wangziling100",
    author_email="wangziling100@163.com",
    description="",
    package_dir={{"": "src"}},
    packages=find_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
    """