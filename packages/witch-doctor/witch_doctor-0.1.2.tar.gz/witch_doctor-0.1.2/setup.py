# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['witch_doctor']

package_data = \
{'': ['*']}

modules = \
['__init__']
setup_kwargs = {
    'name': 'witch-doctor',
    'version': '0.1.2',
    'description': 'Dependency injection for python',
    'long_description': '<img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2Fe6%2Fff%2F86%2Fe6ff86db1ad224c37d328579786e13f3.jpg&f=1&nofb=1&ipt=448de94a888dd920ca7383f804f09f69d49ad4d226d9bee06115bbc9b188e1d2&ipo=images" alt="drawing" style="width:400px;display: block;  margin-left: auto;margin-right: auto;"/>\nBy: CenturyBoys\n\n# Witch-doctor\n\nA simple dependency injection for python\n\n## Register \n\nWitch Doctor provides a method to register interfaces and his implementation. The interface and implementation inheritance will be check and will raise a TypeError if was some error.\n\n```python\nclass WitchDoctor:\n    @classmethod\n    def register(cls, interface: Type[ABC], class_ref: Any):\n        """\n        WitchDoctor.register will check inherit of the interface and class_ref.\n        Will raise a TypeError on validation error\\n\n        :param interface: Interface that inherits from ABC\n        :param class_ref: A implementation of the interface\n        """\n        pass\n```\n\n## Injection \n\nWitch Doctor must be used as decorator. The function signature will ber check and if some values was not provide Witch Doctor will search on the registered interfaces to inject the dependencies.\n\n```python\nclass WitchDoctor:\n    @classmethod\n    def injection(cls, function: Callable):\n        """\n        WitchDoctor.injection is a function decorator that will match the\n        function params signature and inject the  dependencies.\n        Will raise AttributeError is some args was pass throw\\n\n\n        :type function: Callable\n        """\n        pass\n```\n\n## Usage example\n\n```python\nfrom abc import ABC, abstractmethod\n\nfrom witch_doctor import WitchDoctor\n\nclass IStubFromABCClass(ABC):\n    @abstractmethod\n    def sum(self, a: int, b: int):\n        pass\n    \nclass StubFromABCClass(IStubFromABCClass):\n    def sum(self, a: int, b: int):\n        return a + b\n    \nWitchDoctor.register(IStubFromABCClass, StubFromABCClass)\n\n@WitchDoctor.injection\ndef func_t(a: int, b: int, c: IStubFromABCClass):\n    return c.sum(a, b), c\n\nresult_a1, reference_a1 = func_t(a=1, b=2)\nresult_a2, reference_a2 = func_t(a=2, b=2)\n\nassert result_a1 == 3\nassert result_a2 == 4\nassert reference_a1 == reference_a2\n```',
    'author': 'Marco Sievers de Almeida Ximit Gaia',
    'author_email': 'im.ximit@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
