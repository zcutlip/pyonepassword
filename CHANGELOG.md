# Changelog

All notable changes to this project will be documented in this file.

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
