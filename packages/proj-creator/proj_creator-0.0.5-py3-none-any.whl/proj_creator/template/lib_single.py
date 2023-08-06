def get_lib_single_framework(name):
    name = name.replace('-', '_')
    return [
        ['.gitlab', 'd'],
        ['.gitlab/build.yaml', 'f'],
        ['.gitlab/unit-test.yaml', 'f'],
        ['unit_test', 'd'],
        ['.gitignore', 'f'],
        ['.gitlab-ci.yml', 'f'],
        [f'{name}.py', 'f'],
        ['unit_test/test_ao.py', 'f']
    ]


def get_lib_single_build_str(name):
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
      - {name2}.py
  except:
    - pipelines
  script:
    - ls
    - VERSION=$(cat {name2}.py | grep __version__)
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
      - {name2}.py
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
  
def get_lib_single_setup_str(name):
    return f"""
from setuptools import setup
from proj_creator import __version__

setup(
    name="{name}",
    version=__version__,
    author="wangziling100",
    author_email="wangziling100@163.com",
    description="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
    """