# `pyonepassword` Authentication

This document an attempt to describe how `pyonepassword`, specifically the `OP` class handles authenticaiton to the caller's 1Password account via the `op` CLI command. Authentication with `op` has become sufficiently complex that in-lin pydoc documentation is no longer sufficient.

As the `op` command has evolved, it has added additional support scenarios for authentication. As such, `pyonepassword` has eveolved to support those scenarious as closely as possible. As those two evolve together, this document should also be kept up to date to reflect the

## Authentication Scenarios

The following scenarios are supported by `op`:

- Without biometric (unavailable or disabled):
  - Interactive password prompt via `op signin`
  - Passing password over standard input to `op signin`
  - A valid session token stored in an `OP_SESSION_<user uuid>` environment variable
- With biometric enabled:
  - Biometric prompt via `op signin`
  - `op` previously authenticated via biometric and has not timed out
- (coming soon) An OP_SERVICE_ACCOUNT_TOKEN environment variable is set to a valid sevice account token

If there is more than one account configured, you can either tell `op` which to use, or let it choose. How it chooses depends on circumstances and is not documented. In some cases it will prompt on the console with an interactive menu.

If you tell `op` which account to use via the `--account` flag, the identifier may be any of:
- account shorthand (if biometric is disabled)
- sign-in address (i.e., URL),
- account ID
- user ID

`pyonepassword` handles the above scenarios with the following keyword arguments:
- `account`: If provided, this account should be used to authenticate
- `password`: pass the caller-provided password to `op` over standard input.
  - If biometric is enabled, password is still provided to `op` which ignores it
- `existing_auth`: tells `OP` whether authentication has already been established, such as via password, biometric, or service account token. Possible values are:
  - `EXISTING_AUTH_AVAIL`: Use existing authentication if available
  - `EXISTING_AUTH_IGNORE`: Assume there is no existing authentication
  - `EXISTING_AUTH_REQD`: Use existing authentication, failing if there isn't a valid session available
- `password_prompt`: allow `1Password` to prompt interactively for the master password
  - If biometric is enabled, this has no effect
