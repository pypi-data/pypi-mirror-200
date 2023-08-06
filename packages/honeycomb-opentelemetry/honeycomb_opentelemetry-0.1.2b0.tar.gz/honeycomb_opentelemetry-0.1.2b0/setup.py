# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['honeycomb', 'honeycomb.opentelemetry']

package_data = \
{'': ['*']}

install_requires = \
['opentelemetry-api>=1.16.0,<2.0.0',
 'opentelemetry-exporter-otlp>=1.16.0,<2.0.0',
 'opentelemetry-instrumentation>=0.37b0,<0.38',
 'opentelemetry-sdk>=1.16.0,<2.0.0']

entry_points = \
{'opentelemetry_distro': ['distro = '
                          'honeycomb.opentelemetry.distro:HoneycombDistro']}

setup_kwargs = {
    'name': 'honeycomb-opentelemetry',
    'version': '0.1.2b0',
    'description': 'Honeycomb OpenTelemetry Distro for Python',
    'long_description': "# Honeycomb OpenTelemetry Distro for Python\n\n[![OSS Lifecycle](https://img.shields.io/osslifecycle/honeycombio/honeycomb-opentelemetry-python)](https://github.com/honeycombio/home/blob/main/honeycomb-oss-lifecycle-and-practices.md)\n[![CircleCI](https://circleci.com/gh/honeycombio/honeycomb-opentelemetry-python.svg?style=shield)](https://circleci.com/gh/honeycombio/honeycomb-opentelemetry-python)\n\nThis is Honeycomb's Distribution of OpenTelemetry for Python.\nIt makes getting started with OpenTelemetry and Honeycomb easier!\n\nLatest release built with:\n\n- [OpenTelemetry version 1.16.0/0.37b0](https://github.com/open-telemetry/opentelemetry-python/releases/tag/v1.16.0)\n\n## Requirements\n\n- Python 3.7 or higher\n\n## Getting Started\n\nHoneycomb's Distribution of OpenTelemetry for Python allows you to streamline configuration and to instrument as quickly and easily as possible.\n\n- [Documentation](https://docs.honeycomb.io/getting-data-in/opentelemetry/python/)\n- [Examples](/examples/)\n- See [DEVELOPING.md](/DEVELOPING.md) for additional instructions for building and testing this project in development.\n\n## Why would I want to use this?\n\n- Streamlined configuration for sending data to Honeycomb!\n- Easy interop with existing instrumentation with OpenTelemetry!\n- Deterministic sampling!\n- Multi-span attributes!\n- Local visualizations!\n\n## License\n\n[Apache 2.0 License](./LICENSE).\n",
    'author': 'Honeycomb',
    'author_email': 'support@honeycomb.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0',
}


setup(**setup_kwargs)
