It has been observed that in some cases 'op' will return anomalous item dictionaries. These anomalies include things like:

- multiple fields with empty-string IDs, resulting in field ID collisions
- Sections that are duplicated such that the ID and label are identical, resulting in section ID collisions
- Sections that lack an ID altogether

These these test modules are intended to test the following:

- Appropriate exceptions are raised when strict valiation is enforced
- Object instantiation succeeds when relaxed validation is enabled, and the object matches expected data
- Various relaxed/strict validation policy toggles work as expected
