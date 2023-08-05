# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdg_model_builder',
 'gdg_model_builder.completion_stream',
 'gdg_model_builder.completion_stream.providers',
 'gdg_model_builder.completion_stream.providers.redis',
 'gdg_model_builder.completion_stream.sc_stream',
 'gdg_model_builder.context.bounds',
 'gdg_model_builder.context.bounds.execution',
 'gdg_model_builder.context.bounds.session',
 'gdg_model_builder.context.bounds.user',
 'gdg_model_builder.context.context',
 'gdg_model_builder.context.execution',
 'gdg_model_builder.context.session',
 'gdg_model_builder.context.user',
 'gdg_model_builder.environment',
 'gdg_model_builder.event',
 'gdg_model_builder.libutil',
 'gdg_model_builder.libutil.np',
 'gdg_model_builder.libutil.sync',
 'gdg_model_builder.lock',
 'gdg_model_builder.lock.rem_lock',
 'gdg_model_builder.model',
 'gdg_model_builder.model.redis_model',
 'gdg_model_builder.model_builder_cli',
 'gdg_model_builder.modifiers',
 'gdg_model_builder.sdk',
 'gdg_model_builder.sdk.mlb',
 'gdg_model_builder.sdk.ncaab',
 'gdg_model_builder.sdk.weather',
 'gdg_model_builder.serializer',
 'gdg_model_builder.serializer.model_serializer',
 'gdg_model_builder.serializer.providers',
 'gdg_model_builder.serializer.providers.redis',
 'gdg_model_builder.structs',
 'gdg_model_builder.task.listener',
 'gdg_model_builder.task.listener.cbq_listener',
 'gdg_model_builder.task.listener.providers',
 'gdg_model_builder.task.listener.serialized_listener',
 'gdg_model_builder.task.listener.sleepy_listener',
 'gdg_model_builder.task.listener.std_listener',
 'gdg_model_builder.task.tasker',
 'gdg_model_builder.task.tasker.serialized_tasker',
 'gdg_model_builder.util',
 'gdg_model_builder.util.lru',
 'gdg_model_builder.watcher']

package_data = \
{'': ['*'], 'gdg_model_builder.model_builder_cli': ['assets/docker/*']}

install_requires = \
['attrs>=21.4.0,<22.0.0',
 'cattrs>=22.1.0,<23.0.0',
 'checksumdir>=1.2.0,<2.0.0',
 'fastapi[all]>=0.78.0,<0.79.0',
 'numpy>=1.23.0,<2.0.0',
 'polars>=0.16.2,<0.17.0',
 'pycron>=3.0.0,<4.0.0',
 'redis>=4.3.4,<5.0.0']

setup_kwargs = {
    'name': 'gdg-model-builder',
    'version': '2.2.5',
    'description': '',
    'long_description': None,
    'author': 'Liam Monninger',
    'author_email': 'l.mak.monninger@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.9,<4.0',
}


setup(**setup_kwargs)
