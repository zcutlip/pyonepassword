# TODO Items for Service Account Support

github issue: [38](https://github.com/zcutlip/pyonepassword/issues/38)

- [x] verify op operations requiring a vault to be specified have a vault kwarg (see below re: supported/unsupported operations)
- [ ] test the following cases
  - [x] simulate valid service account token & permitted operation
    * This is done in `test_svc_acct_support/test_svc_acct_primary_api.py`
  - [x] simulate valid service account token, but non-permitted operation (e.g., create, but svc acct is read-only)
    * This is done in `test_svc_acct_support/test_svc_acct_primary_api.py`
  - [ ] service account token is corrupted (normal svc account token but with characters missing or replaced)
    * it may not be practical to simulate this in a way that actually tests how we handle `op`'s behavior
  - [ ] service account token is completely invalid (e.g., "foo")
    * it may not be practical to simulate this in a way that actually tests how we handle `op`'s behavior
  - [x] service account token is valid
    * This is done in `test_svc_acct_support/test_svc_acct_primary_api.py`
  - [x] simulate a service account token having been revoked
  - [x] simulate a valid service account token, but non-permitted vault
- [x] raise meaningful exception if caller attempts an operation not supported by service accounts
  * supported/unsupported operations break down into the following categories:
    * operation is supported unconditionally, e.g., `op item list`
    * operation is supported but has one or more mandatory options, e.g., `op item get` requires `--vault`
    * operation is supported but has one or more prohibited options, e.g., `op vault list` can't be used with `--user` or `--group`
    * operation is not supported
  - [x] System for checking if an operation and its options are/are not supported *before* executing the command
    - [x] This is done via `OPSvcAcctSupportRegistry` and the JSON registry under `pyonepassword/data/svc_acct_commands`
- [x] proper behavior if caller to `OP()` provides a password or other parameter not compatible with service accounts
  - [x] Probably raise an exception since caller may be confused about proper API use, or not realize they have a service account token set
    * Now raising OPAuthenticationException if existing_auth == EXISTING_AUTH_REQD and password != None
  - [x] Test above behavior
- [ ] Document service account support
  - [x] API docstrings
  - [ ] README or other .md doc
  - [ ] example code in `examples`
- [x] Minimum version check
- [ ] delete this list when everything above is done
