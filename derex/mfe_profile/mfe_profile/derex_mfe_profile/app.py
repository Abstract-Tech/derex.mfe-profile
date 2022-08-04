from django.apps import AppConfig
from openedx.core.djangoapps.plugins.constants import (
    PluginSettings,
    ProjectType,
    SettingsType,
)


class DerexMfeProfileAppConfig(AppConfig):
    name = "derex_mfe_profile"

    plugin_app = {
        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.COMMON: {PluginSettings.RELATIVE_PATH: "settings"},
            },
            ProjectType.CMS: {
                SettingsType.COMMON: {PluginSettings.RELATIVE_PATH: "settings"},
            },
        },
    }

    def ready(self):
        from waffle.models import Flag
        from openedx.features.learner_profile.toggles import REDIRECT_TO_PROFILE_MICROFRONTEND
        flag = Flag.objects.get_or_create(
            name=REDIRECT_TO_PROFILE_MICROFRONTEND.name, everyone=True
        )
