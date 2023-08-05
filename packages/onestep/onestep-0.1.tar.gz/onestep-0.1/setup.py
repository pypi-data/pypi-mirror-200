# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['onestep', 'onestep.broker', 'onestep.middleware', 'onestep.store']

package_data = \
{'': ['*']}

install_requires = \
['asgiref>=3.6.0,<4.0.0', 'blinker>=1.5,<2.0']

extras_require = \
{'rabbitmq': ['amqpstorm>=2.10.6,<3.0.0']}

setup_kwargs = {
    'name': 'onestep',
    'version': '0.1',
    'description': '',
    'long_description': '# OneStep\n\n内部测试阶段，请勿用于生产。\n\n## Brokers\n\n- [x] MemoryBroker\n- [x] RabbitMQBroker\n- [x] WebHookBroker\n- [ ] RedisBroker\n- [ ] KafkaBroker\n\n## example\n\n```python\nfrom onestep import step, WebHookBroker\n\n\n# 对外提供一个webhook接口，接收外部的消息\n@step(from_broker=WebHookBroker(path="/push"))\ndef waiting_messages(message):\n    print("收到消息：", message)\n\n\nif __name__ == \'__main__\':\n    step.start(block=True)\n```\n\n更多例子请参阅：[examples](example)',
    'author': 'miclon',
    'author_email': 'jcnd@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
