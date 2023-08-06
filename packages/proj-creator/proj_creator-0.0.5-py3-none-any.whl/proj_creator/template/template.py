import datetime
from .base import get_base_framework, get_base_build_str
from .lib import get_lib_build_str, get_lib_framework, get_lib_setup_str
from .lib_single import get_lib_single_build_str, get_lib_single_framework, get_lib_single_setup_str



def get_framework(template, name=None):
    if template=='base':
        return get_base_framework()
    elif template=='lib':
        return get_lib_framework(name)
    elif template=='lib_single':
        return get_lib_single_framework(name)
    else:
        raise NotImplementedError


def get_build_str(template, name):
    if template=='base':
        return get_base_build_str(name)
    elif template=='lib':
        return get_lib_build_str(name)
    elif template=='lib_single':
        return get_lib_single_build_str(name)
    else:
        raise NotImplementedError


def get_license_str():
    y = datetime.datetime.utcnow().year
    return f"""
Copyright (c) {y} The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
    """


def get_setup_str(template, name):
    if template=='lib':
        return get_lib_setup_str(name)
    elif template=='lib_single':
        return get_lib_single_setup_str(name)
    else:
        raise ValueError(f'Wrong template is given when create setup file: {template}')


def get_repository_header():
    return 'from ddd_objects.domain.repository import Repository'