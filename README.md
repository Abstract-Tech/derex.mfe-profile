# Derex Profile Microfrontend

[![Github Actions](https://github.com/Abstract-Tech/derex.mfe-profile/actions/workflows/daily.yml/badge.svg?branch=master)](https://github.com/Abstract-Tech/derex.mfe-profile/actions/workflows/daily.yml)

Derex Plugin to integrate Open edX Profile Microfrontend

## Setup

- Install this package inside a derex project environment
- Add to the project derex.config.yaml

  ```yaml
  plugins:
    derex.mfe_profile: {}
  ```

## Customizations

There are some options that can be passed to the plugin configuration in your derex.config.yaml file.

- docker_image: Then tag which will be given to the built docker image
- build_dir: An optional build directory which content will be included in the build context. Some files will you'll probably want to include here:

  - `.env.derex.j2` and `.env.development.derex.j2` files
  - a `Caddyfile`
  - a `Dockerfile.j2` Jinja template which will compiled and used for the build
  - the whole microfrontend repository. This is especially useful when doing local development
  - any additinal file you might need in your build. `.j2` files will be compiled with the derex `Project` object in the context

  If `.env.derex.j2`, `.env.development.derex.j2`, `Caddyfile` and `Dockerfile.j2` are not present default one will be used.

- aliases: Additional network aliases for the docker container. This list will also be used to populate the `CORS_ORIGIN_WHITELIST` and `LOGIN_REDIRECT_WHITELIST` LMS settings
- NODE_VERSION: The node version which will be given as a build argument
- MFE_REPOSITORY: A repository URL which will be given as a build argument or a path to a local repository in the `build_dir`
- MFE_BRANCH: A Git branch which will be checked out after cloning the Microfrontend repository

e.g.:

```yaml
plugins:
  derex.mfe-profile:
    {
      "build_dir": "mfe_profile_build",
      "docker_image": "my-custom-image-name",
      "aliases": [
        "profile.mydomain.com",
      ]
      "MFE_REPOSITORY": "https://github.com/edx/frontend-app-profile.git",
      "MFE_BRANCH": "open-release/lilac.master",
      "NODE_VERSION": "12-alpine",
    }
```

## Build

You can build the microfrontend image by running:

`derex build mfe-profile`

## Development

- Install [direnv](https://direnv.net/docs/installation.html)
- Allow direnv to create the virtualenv

  ```sh
  direnv allow
  ```

- Install with pip

  ```sh
  pip install -r requirements_dev.txt
  pre-commit install --install-hooks
  ```
