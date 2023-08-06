def get_base_framework():
    return [
        ['.gitlab', 'd'],
        ['.gitlab/build.yaml', 'f'],
        ['.gitlab/unit-test.yaml', 'f'],
        ['unit_test', 'd'],
        ['.gitignore', 'f'],
        ['.gitlab-ci.yml', 'f'],
        ['doc', 'd'],
        ['src', 'd'],
        ['src/application', 'd'],
        ['src/application/__init__.py', 'f'],
        ['src/domain', 'd'],
        ['src/domain/__init__.py', 'f'],
        ['src/infrastructure', 'd'],
        ['src/infrastructure/__init__.py', 'f'],
        ['src/settings.py', 'f'],
        ['src/__init__.py', 'f'],
        ['src/version.py', 'f'],
        ['src/application/action', 'd'],
        ['src/application/action/__init__.py', 'f'],
        ['src/application/assembler', 'd'],
        ['src/application/assembler/__init__.py', 'f'],
        ['src/application/dto', 'd'],
        ['src/application/dto/__init__.py', 'f'],
        ['src/domain/entity', 'd'],
        ['src/domain/entity/__init__.py', 'f'],
        ['src/domain/repository', 'd'],
        ['src/domain/repository/__init__.py', 'f'],
        ['src/domain/repository/base.py', 'f'],
        ['src/domain/value_obj', 'd'],
        ['src/domain/value_obj/__init__.py', 'f'],
        ['src/infrastructure/converter', 'd'],
        ['src/infrastructure/converter/__init__.py', 'f'],
        ['src/infrastructure/converter/base.py', 'f'],
        ['src/infrastructure/ao', 'd'],
        ['src/infrastructure/ao/__init__.py', 'f'],
        ['src/infrastructure/do', 'd'],
        ['src/infrastructure/do/__init__.py', 'f'],
        ['src/infrastructure/repository_impl', 'd'],
        ['src/infrastructure/repository_impl/__init__.py', 'f'],
        ['src/infrastructure/repository_impl/base.py', 'f'],
        ['unit_test/test_repo.py', 'f']
    ]

def get_base_build_str(name):
    name = name.replace('_', '-')
    return f"""
add-tag:
  image: registry.cn-shanghai.aliyuncs.com/wangxb/git
  stage: publish
  only:
    refs:
      - dev
    changes:
      - src/version.py
  except:
    - pipelines
  script:
    - ls
    - VERSION=$(cat src/version.py | grep __version__)
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
    """