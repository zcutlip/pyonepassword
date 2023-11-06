# `pyonepassword` Authentication

This document an attempt to describe how `pyonepassword`, specifically the `OP` class, handles authentication to the user's 1Password account via the `op` CLI command. Authentication with `op` has become sufficiently complex that in-line pydoc documentation is no longer sufficient.

As the `op` command has evolved, it has added additional support scenarios for authentication. As such, `pyonepassword` has evolved to support those scenarious as closely as possible. As those two evolve together, this document should also be kept up to date to reflect the

## Authentication Scenarios

The following scenarios are supported by `op`:

- Without biometric (unavailable or disabled):
  - Interactive password prompt via `op signin`
  - Passing password over standard input to `op signin`
  - A valid session token stored in an `OP_SESSION_<user uuid>` environment variable
- With biometric enabled:
  - Biometric prompt via `op signin`
  - `op` previously authenticated via biometric and has not timed out
- An OP_SERVICE_ACCOUNT_TOKEN environment variable is set to a valid sevice account token

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

## Service Accounts

As of version 3.10.0 `pyonepassword` supports service accounts. You can read more about 1Password service accounts [here](https://developer.1password.com/docs/service-accounts).

Using service accounts with `pyonepassword` is straightforward. In the simplest case, do one of the following:

- set your `OP_SERVICE_ACCOUNT_TOKEN` environment variable outside of your Python environment
- create an environment file protected with appropriate permissions and use the Python package `python-dotenv` to load it from within your script


Having set your service account token, you should be able to create and use an `OP` object with no further authentication.

There are a few restricitons to be aware of, however.

- The minimum `op` CLI version supported with service accounts is 2.18.0-beta.01
  - Any earlier version will cause an exception to be raised if `OP_SERVICE_ACCOUNT_TOKEN` is set
- Certain `op` operations are either not allowed with service accounts or allowed with restrictions. See more below.
- It is an error to pass the `password=` kwarg to `OP()` if a service account token is set

### Service Account Supported Operations

Operation support with service accounts breaks down into following four categories:

- Supported
- Supported with one or more required options (e.g., `--vault`)
- Supported with one or more prohibited options
- Not supported

An example of a supported operation is `OP.item_list()`. This method works with service accounts without caveat.

A supported operation requiring a specific option is `OP.item_get()` which requires the `vault=` kwarg to be specified.

A supported option that prohibits specific options is `OP.vault_list()`. When authenticated as a service account, this operation cannot be used with the `group_name_or_id=` or `user_name_or_id=` kwargs

Currently none of `pyonepassword`'s operations are strictly unsupported with service accounts.

If the `OP_SERVICE_ACCOUNT_TOKEN` environment variable is set and an unsupported operation (or an operation with an unsupported set of options) is requested, an exception will be raised (more below).

### Service Account-Related Exceptions

There are a number of circumstances that result in exceptions specifically when a service account token is set. The are:

- `OPAuthenticationException`:
  - if the version of the `op` CLI command is less than the minimum supported version, currently 2.18.0-beta.01
  - if a `password=` kwarg is provided, since sign-in authentication has no effect
- `OPSvcAcctCommandNotSupportedException`:
  - if an unsupported operation is requested
  - if a supported operation is reqested that has unsatisfied option constraints
- `OPCmdMalformedSvcAcctTokenException`:
  - if the `op` command fails to decode a service account token
- `OPRevokedSvcAcctTokenException`:
  - if the `op` command reports the service account token has been revoked
