import json
import os


def plugin_settings(settings):
    DEREX_PROJECT = os.environ.get("DEREX_PROJECT")

    settings.ENABLE_PROFILE_MICROFRONTEND = True
    settings.PROFILE_MICROFRONTEND_URL = os.environ.get(
        "DEREX_PROFILE_MICROFRONTEND_URL",
        "http://profile.{}.localhost".format(DEREX_PROJECT),
    )

    PROFILE_MICROFRONTEND_ALIASES = os.environ.get(
        "DEREX_PROFILE_MICROFRONTEND_ALIASES", []
    )
    if PROFILE_MICROFRONTEND_ALIASES:
        PROFILE_MICROFRONTEND_ALIASES = json.loads(PROFILE_MICROFRONTEND_ALIASES)

    if settings.PROFILE_MICROFRONTEND_URL not in PROFILE_MICROFRONTEND_ALIASES:
        PROFILE_MICROFRONTEND_ALIASES.append(settings.PROFILE_MICROFRONTEND_URL)

    default_alias = "profile.{}.localhost".format(DEREX_PROJECT)
    if default_alias not in PROFILE_MICROFRONTEND_ALIASES:
        PROFILE_MICROFRONTEND_ALIASES.append(default_alias)

    try:
        settings.CORS_ORIGIN_WHITELIST.extend(PROFILE_MICROFRONTEND_ALIASES)
        settings.LOGIN_REDIRECT_WHITELIST.extend(PROFILE_MICROFRONTEND_ALIASES)
    except AttributeError:
        # This is the lms.envs.common settings loading the plugins
        # We simply pass here since plugins will be properly loaded
        # by derex django default settings
        pass
