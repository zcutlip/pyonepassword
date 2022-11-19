# Changelog

All notable changes to this project will be documented in this file.

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
