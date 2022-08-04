from typing import Optional

import click
from derex.runner.build import build_microfrontend_image
from derex.runner.cli import ensure_project
from derex.runner.cli.build import build as derex_build_cli
from derex.runner.project import Project

from derex.mfe_profile import __version__
from derex.mfe_profile.constants import (
    DEFAULT_BUILD_DIR,
    DEFAULT_CADDYFILE_PATH,
    DEFAULT_DEV_ENV_FILE_TEMPLATE_PATH,
    DEFAULT_DOCKERFILE_TEMPLATE_PATH,
    DEFAULT_ENV_FILE_TEMPLATE_PATH,
    MfeProfileVersions,
)


@derex_build_cli.command("mfe-profile")
@click.pass_obj
@ensure_project
@click.argument(
    "version",
    type=click.Choice(MfeProfileVersions.__members__),
    required=False,
    callback=lambda _, __, value: value and MfeProfileVersions[value],
)
@click.option(
    "-T",
    "--target",
    type=click.Choice(["sourceonly", "dev", "final"]),
    required=False,
    help="Target to build",
)
@click.option(
    "-o",
    "--output",
    type=click.Choice(["docker", "registry"]),
    default="docker",
    help="Where to push the resulting image",
)
@click.option("-r", "--registry", type=str)
@click.option("-t", "--tag", type=str)
@click.option("--latest", "tag_latest", is_flag=True, default=False)
@click.option(
    "--only-print-image-name",
    is_flag=True,
    default=False,
    help="Only print the name which will be assigned to the image",
)
@click.option(
    "--pull",
    is_flag=True,
    default=False,
    help="Always try to pull the newer version of the image",
)
@click.option("--no-cache", is_flag=True, default=False)
@click.option("--cache-from", is_flag=True, default=False)
@click.option("--cache-to", is_flag=True, default=False)
def mfe_profile_build(
    project: Project,
    version: Optional[str],
    target: str,
    output: str,
    registry: Optional[str],
    tag: Optional[str],
    tag_latest: bool,
    only_print_image_name: bool,
    pull: bool,
    no_cache: bool,
    cache_from: bool,
    cache_to: bool,
):
    """Build microfrontend image using docker. Defaults to final image target."""
    try:
        config = project.config.get("plugins").get("derex.mfe-profile") or {}
    except AttributeError:
        config = {}

    if not version:
        version = project.openedx_version
    if not target:
        target = "final"
        if project.runmode.name == "debug":
            target = "dev"

    default_config = MfeProfileVersions[version.name]

    default_docker_image_prefix = default_config.value["docker_image_prefix"]
    tag = config.get("docker_image_tag", f"{default_docker_image_prefix}:{__version__}")
    if only_print_image_name:
        click.echo(tag)
        return 0

    build_dir = DEFAULT_BUILD_DIR
    caddyfile_path = DEFAULT_CADDYFILE_PATH
    dockerfile_template_path = DEFAULT_DOCKERFILE_TEMPLATE_PATH
    env_file_template_path = DEFAULT_ENV_FILE_TEMPLATE_PATH
    dev_env_file_template_path = DEFAULT_DEV_ENV_FILE_TEMPLATE_PATH

    if config.get("build_dir"):
        build_dir = project.root / config.get("build_dir")

    if not build_dir.exists() or not build_dir.is_dir():
        raise click.ClickException(
            f"Build dir {build_dir} does not exist or is not a directory. Aborting."
        )

    if build_dir != DEFAULT_BUILD_DIR:
        if (build_dir / DEFAULT_CADDYFILE_PATH.name).exists() and (
            build_dir / DEFAULT_CADDYFILE_PATH.name
        ).is_file():
            caddyfile_path = build_dir / DEFAULT_CADDYFILE_PATH.name
        if (build_dir / DEFAULT_DOCKERFILE_TEMPLATE_PATH.name).exists() and (
            build_dir / DEFAULT_DOCKERFILE_TEMPLATE_PATH.name
        ).is_file():
            dockerfile_template_path = build_dir / DEFAULT_DOCKERFILE_TEMPLATE_PATH.name
        if (build_dir / DEFAULT_ENV_FILE_TEMPLATE_PATH.name).exists() and (
            build_dir / DEFAULT_ENV_FILE_TEMPLATE_PATH.name
        ).is_file():
            env_file_template_path = build_dir / DEFAULT_ENV_FILE_TEMPLATE_PATH.name
        if (build_dir / DEFAULT_DEV_ENV_FILE_TEMPLATE_PATH.name).exists() and (
            build_dir / DEFAULT_DEV_ENV_FILE_TEMPLATE_PATH.name
        ).is_file():
            dev_env_file_template_path = (
                build_dir / DEFAULT_DEV_ENV_FILE_TEMPLATE_PATH.name
            )

    paths_to_copy = [path for path in build_dir.iterdir()]
    for path in [
        caddyfile_path,
        dockerfile_template_path,
        env_file_template_path,
        dev_env_file_template_path,
    ]:
        if path not in paths_to_copy:
            paths_to_copy.append(path)

    build_args = {
        "NODE_VERSION": config.get(
            "NODE_VERSION", default_config.value["NODE_VERSION"]
        ),
        "MFE_REPOSITORY": config.get(
            "MFE_REPOSITORY", default_config.value["MFE_REPOSITORY"]
        ),
        "MFE_BRANCH": config.get("MFE_BRANCH", default_config.value["MFE_BRANCH"]),
    }

    build_microfrontend_image(
        project,
        target,
        paths_to_copy,
        output,
        registry,
        tag,
        tag_latest,
        pull,
        no_cache,
        cache_from,
        cache_to,
        build_args=build_args,
        dockerfile_template_path=dockerfile_template_path,
    )
