"""Setup for Derex Profile Microfrontend support package."""

from setuptools import setup

setup(
    name="derex-mfe-profile",
    version="0.0.1",
    description="Support package for Derex Profile Microfrontend",
    packages=["derex_mfe_profile"],
    entry_points={
        "lms.djangoapp": [
            "derex_mfe_profile = derex_mfe_profile.app:DerexMfeProfileAppConfig"
        ],
        "cms.djangoapp": [
            "derex_mfe_profile = derex_mfe_profile.app:DerexMfeProfileAppConfig"
        ],
    },
)
