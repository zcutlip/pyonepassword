# Changelog

All notable changes to this project will be documented in this file.

## [3.6.0] - 2023-03-01

## Added

- Ability to delete multiple items at once via `OP.item_delete_multiple()` (gh-82)
- Ability to create items with tags applied (gh-83)
- `tags` property to all items and item descriptors (gh-93)

## [3.5.0] - 2023-02-15

### Summary

Support creating item objects from non-conformant item data and unknown item types

### Fixed

Non-conformant item dictionaries returned by `op` can now optionally be parsed with relaxed validation (gh-85). See "Added" below.

### Added

- An API to relax validation of item dictionaries in the case that `op` returns non-conforming dictionaries. See `ITEM_VALIDATION.md`.
- The ability to instantiate item objects and item descriptor lists (e.g., OP.item_get() & OP.item_list()) where an item is an unknown type.
  - Where appropriate, a `generic_okay` kwargs has been added, enabling generic item objects to be returned

## [3.4.1.post1] - 2023-01-29

## Summary

Minor update to .pre-commit-config.yaml.

*Note*: No PyPI release will be generated for this update.

## [3.4.1.post0] - 2023-01-12

### Summary

Missed a few housekeeping commits from the development branch

### Fixed

Fixed a shellcheck complaint in a docker testing script

### Changed

- update .pre-commit-config: bump isort 5.11.3 -> 5.11.4
- refactor `pypi_password.py` script

###

## [3.4.1] - 2023-01-11

### Fixed

- Initialize url_obj in `OP.login_item_create()` to not crash if no URL provided (gh-78)

### Changed

- minor tweaks to docker testing scripts

## [3.4.0] - 2022-12-19

### Added

- OP.item_delete() method (gh-52)
- about & version clas methods:
  - OP.about()
  - OP.version()

## [3.3.5] - 2022-11-27

### Fixed

- Include all `pyonepassword` subpackages by wildcard during build/installation (gh-64)
- Clean `*.egg-info` during build/installation to ensure proper things get included/excluded

## [3.3.4.post0] - 2022-11-26

### Changed

- Updated Renovate bot's `rennovate.json` to target `development` branch rather than `main`

### Note

No release will be generated for this update

## [3.3.4] - 2022-11-24

### Changed

- Added `py.typed` marker for `mypy` type analysis when imported into other projects (gh-48)
- Extensive improvements with type-hinting throughout project
- Added `mypy` testing to `tox.ini`
- Add `mypy` testing to Docker infrastructure

### Fixed

- A few bugs found by `mypy` where the wrong type was being passed to or returned from a method
- A few cases where the wrong type being passed by a caller would have crashed rather than passed back up as a meaningful error
- Properly export all symbols exposed under `pyonepassword.api`s

## [3.3.3] - 2022-11-18

### Changed

- Fix an issue where `op.item_delete()` would blow up if the item to be deleted was an unknown (to pyonepassword) type (gh-54)

## [3.3.2] - 2022-11-16

### Changed

Minor updates to ITEM_CREATION.md

## [3.3.1] - 2022-11-15

### Added

New item creation API!

Primarily
- OP.item_create()
- OP.login_item_create()

Additionally, there are a number of new types in support of item creation. See ITEM_CREATION.md for a variety of examples.

Item deletion API:
- OP.item_delete()

## [3.2.1] - 2022-10-17

### Changed

- Bug where `op` config having no accounts was not handled properly (#43)

## [3.2.0] - 2022-09-27

### Added

- This CHANGELOG file to hopefully serve as a summary of notable changes

### Changed

- This release is primarily a refactor of the `OP()` constructor in order to organize authentication steps
- This should be mostly transparent to the caller, with the following exceptions:
  - New exception class: `pyonepassword.api.OPUnknownAccountException`
  - New kwargs for `OP()`: `existing_auth` and `account`
  - New constants for `existing_auth`: `EXISTING_AUTH_AVAIL`, `EXISTING_AUTH_IGNORE`, `EXISTING_AUTH_REQD`

### Deprecated
- The following kwargs to `OP()` are deprecated:
  - `use_existing_session`: use `existing_auth` instead
  - `account_shorthand`: use `account` instead
