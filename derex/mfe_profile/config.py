from pathlib import Path
from typing import Dict, List, Union

import pkg_resources
from derex.runner.project import Project
from jinja2 import Template

from derex import runner  # type: ignore
from derex.mfe_profile import __version__
from derex.mfe_profile.constants import MfeProfileVersions


def generate_local_docker_compose(project: Project) -> Path:
    derex_dir = project.root / ".derex"
    if not derex_dir.is_dir():
        derex_dir.mkdir()
    local_compose_path = derex_dir / "docker-compose-mfe-profile.yml"
    template_path = Path(
        pkg_resources.resource_filename(__name__, "docker-compose-mfe-profile.yml.j2")
    )
    try:
        config = project.config.get("plugins").get("derex.mfe-profile") or {}
    except AttributeError:
        config = {}

    default_docker_image_prefix = MfeProfileVersions[
        project.openedx_version.name
    ].value["docker_image_prefix"]
    mfe_profile_docker_image = config.get(
        "docker_image", f"{default_docker_image_prefix}:{__version__}"
    )
    mfe_profile_aliases = config.get("aliases") or []
    mfe_profile_repository = config.get("MFE_REPOSITORY") or None
    mfe_profile_build_dir = config.get("build_dir") or None

    if mfe_profile_repository and mfe_profile_build_dir:
        mfe_profile_repository = project.root / mfe_profile_build_dir / mfe_profile_repository
        if not mfe_profile_repository.exists() or not mfe_profile_repository.is_dir():
            mfe_profile_repository = None

    tmpl = Template(template_path.read_text())
    text = tmpl.render(
        project=project,
        mfe_profile_docker_image=mfe_profile_docker_image,
        mfe_profile_aliases=mfe_profile_aliases,
        mfe_profile_repository=mfe_profile_repository,
    )
    local_compose_path.write_text(text)
    return local_compose_path


class MfeProfileService:
    @staticmethod
    @runner.hookimpl
    def ddc_project_options(project: Project) -> Dict[str, Union[str, List[str]]]:
        options: List[str] = []
        if "derex.mfe-profile" in project.config.get("plugins", {}):
            local_compose_path = generate_local_docker_compose(project)
            options = ["-f", str(local_compose_path)]
        return {
            "options": options,
            "name": "mfe-profile",
            "priority": "<local-project",
        }
