# CLI Version Support

`pyonepassword` depends on the 1Password CLI, and in particular the most recent versions of it. For convenience, API is provided to verify and compare versions.

## Inspecting Version Support

The `OP` class exposes class methods for inspecting CLI version support. These can be used early in your code to verify compatibility before performing any 1Password operations.

```python
OP.check_op_version(op_path="op")
```

Optionally specify a path to `op`.

Verify whether the installed `op` is supported.
  - If it is supported, there is no response
  - If it is supported but deprecated, a `DeprecationWarning` is issued
  - If the `op` version is no longer supported, `OPCLIVersionSupportException` is raised

---

```python
OP.supported_op_version()
```

Get the minimum supported CLI version. Versions below this are either deprecated but supported or completely unsupported.

Returns an `OPCLIVersion` object, described below.

---

```python
OP.minimum_op_version()
```

Get the minimum compatible CLI version. Versions greater than or equal to this and less than the supported version are considered deprecated. A deprecation warning is issued they they are used. Versions less than this are not supported, and an exception is raised as described above.

Returns an `OPCLIVersion` object, described below.


## Version Objects

Additionally, `pyonepassword` provides a class representing `op` CLI versions:

```python
OPCLIVersion
```

Version objects have the following features:

- Supports mathematical comparison (equality, greater-than, less-than, etc):
  - Between objects
  - Between an object and a version string
- Supports conversion back to version string
- Recognizes beta versions
  - A beta version of the same major, minor, and patch as a non-beta version is considered strictly less-than the non-beta version

Comparing two `OPCLIVersion` objects:

```Python console
In [1]: from pyonepassword.api.cli_version import OPCLIVersion

In [2]: version_string_1 = "2.26.0"

In [3]: version_string_2 = "2.27.0"

In [4]: version_obj_1 = OPCLIVersion(version_string_1)

In [5]: version_obj_2 = OPCLIVersion(version_string_2)

In [6]: version_obj_1 < version_obj_2
Out[6]: True
```

Comparing an `OPCLIVersion` object to a version string:

```Python console
In [7]: version_obj_2 > "2.26.0"
Out[7]: True
```

Comparing beta and non beta versions:

```Python console
In [10]: version_string_beta = "2.26.0-beta.12"

In [11]: version_obj_beta = OPCLIVersion(version_string_beta)

In [12]: version_obj_1 > version_obj_beta
Out[12]: True

In [14]: version_obj_beta.is_beta
Out[14]: True
```

String representation:

```Python console
In [9]: str(version_obj_2)
Out[9]: '2.27.0'
```
