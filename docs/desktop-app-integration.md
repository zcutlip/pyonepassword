# 1Password Desktop App Integration

The 1Password desktop app has an option to enable integration with the `op` CLI executable. This enables authentication, among other things, to be handled by the desktop app.

## App and `op` Failure

Very rarely, however, the 1Password application may be unavailable to communicte with `op`. This may be because the application's IPC is saturated, or a process has died, Or potentially other reasons. If you were to run `op` when this happens you would see output like so:

```shell-session
❱ op account list
[ERROR] 2025/04/11 18:30:32 connecting to desktop app: 1Password CLI couldn't connect to the 1Password desktop app. To fix this, update the 1Password app to the latest version and restart the app. If you're still having trouble, visit https://developer.1password.com/docs/cli/app-integration#troubleshooting for more help.
```

`pyonepassword` attempts to detect when this happens and raise an appropriate exception: `OPDesktopAppException`.

If you're encountering this error, which should be rare, it may be worth handling the exception and retrying the attempt. In some cases it can take two or three attempts for `op` to resume communicating with the application.

Below is example code handling the exception:

```python
import time

from pyonepassword import OP
from pyonepassword.api.exceptions import OPDesktopAppException
from pyonepassword.logging import console_debug_logger

if __name__ == "__main__":
    logger = console_debug_logger("pyonepassword")

    attempts = 0
    while attempts < 3:
        # It can fail twice in a row but with slightly different
        # error each time. Give it three tries to be sure
        attempts += 1
        try:
            op = OP(logger=logger)
        except OPDesktopAppException as e:
            print(e.err_output)
            print(f"Attempt {attempts}: received OPDesktopAppException")
            print("Sleeping 1 second")
            time.sleep(1)

```

An example that simulates this can be found in `examples/desktop-app-integration.py`.
