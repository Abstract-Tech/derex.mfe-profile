from enum import Enum

from derex.runner.utils import abspath_from_egg

DEFAULT_BUILD_DIR = abspath_from_egg(
    "derex.mfe_profile", "derex/mfe_profile/docker_build/Dockerfile.j2"
).parent
DEFAULT_CADDYFILE_PATH = abspath_from_egg(
    "derex.mfe_profile", "derex/mfe_profile/docker_build/Caddyfile"
)
DEFAULT_DOCKERFILE_TEMPLATE_PATH = abspath_from_egg(
    "derex.mfe_profile", "derex/mfe_profile/docker_build/Dockerfile.j2"
)
DEFAULT_ENV_FILE_TEMPLATE_PATH = abspath_from_egg(
    "derex.mfe_profile", "derex/mfe_profile/docker_build/.env.derex.j2"
)
DEFAULT_DEV_ENV_FILE_TEMPLATE_PATH = abspath_from_egg(
    "derex.mfe_profile", "derex/mfe_profile/docker_build/.env.development.derex.j2"
)


class MfeProfileVersions(Enum):
    # Values will be passed as uppercased named arguments to the docker build
    # e.g. --build-arg MFE_VERSION_RELEASE="open-release/lilac.master"
    lilac = {
        "docker_image_prefix": "ghcr.io/abstract-tech/derex-mfe-profile-lilac",
        "MFE_REPOSITORY": "https://github.com/edx/frontend-app-profile.git",
        "MFE_BRANCH": "open-release/lilac.master",
        "NODE_VERSION": "12-alpine",
    }
