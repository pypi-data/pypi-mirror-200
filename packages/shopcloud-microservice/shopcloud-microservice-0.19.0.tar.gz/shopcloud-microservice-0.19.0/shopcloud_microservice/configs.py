from pathlib import Path
from typing import List

import yaml

from . import exceptions


class Config:
    FILENAME = 'microservices.yaml'
    VERSION = 'V1'

    def __init__(self):
        pass

    def dict(self) -> dict:
        return {}

    def load_projects(self) -> List[str]:
        filename = 'projects.yaml'
        if not Path(filename).exists():
            raise exceptions.ProjectFileNotFound()

        projects = []

        with open(filename) as f:
            data = yaml.safe_load(f.read())
            projects = data.get('projects', [])

        return projects
