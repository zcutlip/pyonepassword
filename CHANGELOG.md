# Changelog

All notable changes to this project will be documented in this file.

## [4.1.0] 2023-11-28

### Added

- Document editing (gh-150):
  - `OP.document_edit()`

### Documentation

- Describe document editing in `docs/document-editing.md`
- Added set of document editing examples under `examples/document_editing`

### Misc

Substantial reorganization of `tests/`

## [4.0.0] 2023-11-15

### Fixed

Raise `OPItemEditException` when editing item fields if the item does not exist.

## [4.0.0] 2023-11-06

### Added
- Item editing (gh-143):
  - `OP.item_edit_add_password_field()`
  - `OP.item_edit_add_url_field()`
  - `OP.item_edit_add_text_field()`
  - `OP.item_edit_set_password()`
  - `OP.item_edit_set_url_field()`
  - `OP.item_edit_set_text_field()`
  - `OP.item_edit_delete_field()`
  - `OP.item_edit_favorite()`
  - `OP.item_edit_generate_password()`
  - `OP.item_edit_tags()`
  - `OP.item_edit_title()`
  - `OP.item_edit_url()`

- `OPAbstractItem.field_value_by_section_label()` (gh-144)
  - replacement for poorly named `field_value_by_section_title()`

- Support for `op` new `whoami` behavior version 2.20.0 (gh-146)
  - new `whoami` dict
  - On `OP()` initialization, accomodate `whoami` failure when the token hasn't been used recently

### Changed
- Added Python 3.12 support (gh-152)
- Removed Python 3.8 support (gh-152)
- Ensure all methods for section lookup by label raise `OPSectionNotFound` if no section is found matching the given label (gh-144)
- Ensure all methods for field lookup by label raise `OPFieldNotFound` if no field is found matching the given label (gh-144)

### Deprecated

- `OPAbstractItem.field_value_by_section_title()` (gh-144)
  - call `OPAbstractItem.field_value_by_section_label()` instead

### Removed

- Deprecated kwargs to `OP()`: (gh-161)
  - `use_existing_session` (replaced by `existing_auth`)
  - `account_shorthand` (replaced by `account`)
- Deprecated exception `OPNotSignedInException` class (gh-161)
  - replaced with `OPAuthenticationException`

### Documentation
- Documented item editing in `docs/item-editing.md`
- Added set of item editing examples under `examples/item_editing`

### Misc
- Updated testing configuration in conjuncton with refactored `mock-op`
- Add `FUNDING.yml`
- Have `setup.py` automatically convert relative URLs in `long_description` to absolute GitHub URLs so they work on PyPI

## [3.12.1] 2023-06-26

### Fixed

- `OP.item_create()` broken due to subcommand args not added to arugment list (gh-136)

### Miscellaneous

- Fixed `scripts/batch_create.py` not setting tags properly
- Enable console debug logging in `scripts/batch_create.py`


## [3.12.0] 2023-06-22

### Added

- Account and user UUIDs are now partially masked when logged (gh-130)
- New class, RedactedString, for automatically redacting strings when appropriate (gh-130)

## [3.11.1] - 2023-06-21

### Fixed

- Properly package up JSON data files under `data/svc_acct_commands` (gh-131)
- Change `pytest` behavior under `tox` to better detect files not properly packaged (gh-131)

## [3.11.0] - 2023-06-07

Fix support for removing an account from the `op` CLI config (gh-121)

### Added

- `OP.account_forget()` method with support for `op account forget` in CLI version >= 2

### Removed
- `OP.forget()`
  - This has been broken since the CLI version 2 refactor in `pyonepassword` version 3.0.0

## [3.10.0] - 2023-05-30

### Added

Support for authentication via service accounts: Set `OP_SERVICE_ACCOUNT_TOKEN` prior to initializing `OP` object. See `docs/AUTHENTICATION.md` for more details.

**Note:** The minimum supported `op` command version is 2.18.0-beta.01.

- New exception classes:
  - `OPAuthenticationException`
    - For any issue with authentication during `OP()` initialization
    - If authentication has exipired prior to performing an operation
  - `OPCLIPanicException`
    - the rare case the `op` command itself crashes
  - `OPCmdMalformedSvcAcctTokenException`
    - in the case that the `op` command is unable to parse a service account token
  - `OPRevokedSvcAcctTokenException`
    - The service account token in use has been revoked and is no longer valid

### Deprecated

- The exception class `OPNotSignedInException` is now deprecated:
  - handle `OPAuthenticationException` instead

## [3.9.0] - 2023-04-06

### Added

- OPServerItem properties corresponding to "hosting provider" fields (gh-115)

### Misc

- Significant refactor of testing of item types (`tests/test_item_types`) (gh-41)

## [3.8.0] - 2023-03-27

### Added

- Support for database item creation via `OPDatabaseItemTemplate` (gh-111)

## [3.7.1] - 2023-03-13

### Fixed

- Check if authorization has expired or is otherwise invalid before performing `op` operations (gh-84)
  - Raise `OPNotSignedInException` rather than the generic `OPCmdFailedException`
- Detect if an `op` command failure was actually `mock-op` failing to find a response definition
  - This was masking test failures that are expecting simulated command failures

## [3.7.0] - 2023-03-10

## Added

  - `OPDatabaseItem` class for retrieving database 1Password items (gh-98)


## Misc

Substantial refactor of automated test expected data for item objects

## Contributors

- @Rom3dius: gh-97 pull request


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
