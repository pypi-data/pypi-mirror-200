# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecs_service_discovery']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'compose-x-common>=1.2,<2.0',
 'prometheus-client>=0.16,<0.17']

entry_points = \
{'console_scripts': ['ecs-sd = ecs_service_discovery.cli:main',
                     'ecs-service-discovery = ecs_service_discovery.cli:main']}

setup_kwargs = {
    'name': 'ecs-service-discovery',
    'version': '0.1.0',
    'description': 'ECS Service Discovery',
    'long_description': '=====================\nECS Service Discovery\n=====================\n\n.. image:: https://img.shields.io/pypi/v/ecs_service_discovery.svg\n        :target: https://pypi.python.org/pypi/ecs_service_discovery\n\nYet another tool to perform ECS API based service discovery.\nPrimarily aimed at gapping the lack of integrations for ECS Anywhere.\n\nFeatures\n==========\n\n* Creates Prometheus scraping configuration, from scanning ECS clusters & services, based on docker labels\n\nInstallation\n==============\n\nDocker\n--------\n\nHead to `Public ECR`_ to obtain the image\n\n.. code-block::\n\n    docker run --rm -it -v ~/.aws:/root/.aws public.ecr.aws/compose-x/ecs-service-discovery\n\n\nPython\n---------\n\nFor your user only\n\n.. code-block::\n\n    pip install pip --user ecs-service-discovery\n\nVia virtual environment\n\n.. code-block::\n\n    pip install ecs-service-discovery\n\n\nUsage\n=======\n\n.. code-block::\n\n    usage: ecs-sd [-h] [-d OUTPUT_DIR] [--profile PROFILE] [-p PROMETHEUS_PORT] [--intervals INTERVALS] [--prometheus-output-format PROMETHEUS_OUTPUT_FORMAT] [_ ...]\n\n    positional arguments:\n      _\n\n    options:\n      -h, --help            show this help message and exit\n      -d OUTPUT_DIR, --output_dir OUTPUT_DIR\n      --profile PROFILE     aws profile to use. Defaults to SDK default behaviour\n      -p PROMETHEUS_PORT, --prometheus-port PROMETHEUS_PORT\n      --intervals INTERVALS\n                            Time between ECS discovery intervals\n      --prometheus-output-format PROMETHEUS_OUTPUT_FORMAT\n                            Change the format of generated files. JSON or YAML.\n\nExamples\n==========\n\nECS Compose-X\n-----------------\n\nInstall `ecs-compose-x`_ & deploy to AWS\n\n.. hint::\n\n    you will need to use the `x-vpc`_ extension to deploy the service in the right VPC to get prometheus scraping.\n    you can use the `x-cluster`_ extension to specify the ECS Cluster you want to deploy the service to.\n\nDocker Compose\n-----------------\n\nAfter cloning the repository, run `docker compose up`. It will spin the service discovery, along with prometheus & grafana to run the demo with.\nYou can access prometheus via `localhost:9090` and grafana via `localhost:3000` (admin:admin by default).\n\nIn prometheus, you can look at the configuration and service discovery. You should see the discovered targets that prometheus is going to try\nto scrape.\n\nAWS Policy requirements\n=========================\n\n.. code-block:: yaml\n\n          PolicyName: ECSServiceDiscoverySimple\n          PolicyDocument:\n            Version: "2012-10-17"\n            Statement:\n              - Effect: Allow\n                Action:\n                  - ecs:ListClusters\n                  - ecs:ListContainerInstances\n                  - ecs:ListTasks\n                  - ecs:DescribeContainerInstances\n                  - ssm:DescribeInstanceInformation\n                  - ecs:DescribeTasks\n                  - ecs:DescribeTaskDefinition\n                Resource: \'*\'\n\n\n.. _Public ECR: https://gallery.ecr.aws/compose-x/ecs-service-discovery\n.. _ecs-compose-x: https://docs.compose-x.io/installation.html\n.. _x-cluster: https://docs.compose-x.io/syntax/compose_x/ecs_cluster.html\n.. _x-vpc: https://docs.compose-x.io/syntax/compose_x/vpc.html\n',
    'author': 'John Preston',
    'author_email': 'john@ews-network.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
