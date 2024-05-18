Example version support dictionary:

```json
{
  "meta" :{
    "version": 1
  },
  "version-support":{
    "deprecated": "2.23.0",
    "minimum": "2.18.0"
  },
  "feature-support": {
    "service-accounts": "2.18.0"
  },
  "bug-fixes": {
    "document-bytes": {
      "above": "0",
      "to": "2.2.0"
    },
    "example-op-bug": {
      "above": "2.23.0",
      "to": "CURRENT"
    }
  }
}
```

Explanation of keys:

- `version-support`:
  - `minimum`: versions less than this are officially not supported by `pyonepassword` and an exception will be raised
  - `deprecated`: versions less than/equal to this, and greater than/equal to the minimum are supported but deprecated. A deprecation warning will be issued
- `feature-support`: When certain features, e.g., service accounts, require a minimum `op` version, this sub-dictionary, contains those feature-name/version pairs
- `bug-fixes`: When `pyonepassword` needs to have a special code path to handle bugs in `op`, versions bracket when the bug was introduced and fixed.
  - `above`: Highest known version prior to introduction of the bug
  - `to`: Highest known version prior the bug being fixed. Special value: `CURRENT` - the bug remains unfixed on the current version
