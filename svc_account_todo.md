# TODO Items for Service Account Support

github issue: [38](https://github.com/zcutlip/pyonepassword/issues/38)

- [ ] verify op operations requiring a vault to be specified have a vault kwarg
- [ ] test the following cases
  - [ ] simulate valid service account token & permitted operation
  - [ ] simulate valid service account token, but non-permitted operation (e.g., create, but svc acct is read-only)
  - [ ] service account token is corrupted (normal svc account token but with characters missing or replaced)
  - [ ] service account token is completely invalid (e.g., "foo")
  - [ ] service account token is valid
  - [ ] simulate a service account token having been revoked
  - [ ] simulate a valid service account token, but non-permitted vault
- [ ] raise meaningful exception if caller attempts an operation not supported by service accounts
  - [ ] what operations are/are not supported by service accounts?
- [ ] proper behavior if caller to `OP()` provides a password or other parameter not compatible with service accounts
  - [ ] Probably raise an exception since caller may be confused about proper API use, or not realize they have a service account token set
- [ ] delete this list when everything above is done
