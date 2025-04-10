import os
import shlex
import sys
import time

parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
if parent_path not in sys.path:
    sys.path.insert(0, parent_path)

# isort: split
from pyonepassword import OP  # noqa: E402
from pyonepassword._op_cli import _OPCLIExecute as OPCLI  # noqa: E402
from pyonepassword.api.exceptions import OPDesktopAppException  # noqa: E402
from pyonepassword.logging import console_debug_logger  # noqa: E402
from pyonepassword.py_op_exceptions import OPCmdFailedException  # noqa: E402


class OPARGV(list):
    """
    stand-in for _OPCLIArgv class
    """

    def cmd_str(self):
        """
        return a shell-escaped command string from this argv
        """

        # ensure we get redacted versions of any strings where
        # applicable
        args = [str(arg) for arg in self]
        cmd_str = shlex.join(args)
        return cmd_str


def simulate_1password_failure():
    # This simulates 1Password dying or becoming unresponsive
    # this should be equivalent to:
    # kill $(pgrep "1Password")
    match_pattern = "1Pass"
    argv = OPARGV(["pgrep", match_pattern])
    # we're lazy so we're going to use _OPCLIExecute.run() here
    # since it already handles all the subprocess stuff
    matches = OPCLI._run(argv, capture_stdout=True, decode="utf-8")

    pid_list = matches.splitlines()
    print(f"matching pids:\n{matches}")
    args = ["kill"]
    args.extend(pid_list)
    argv = OPARGV(args)
    OPCLI._run(argv)


if __name__ == "__main__":
    logger = console_debug_logger("pyonepassword")

    try:
        # We're going to kill all 1Password processes
        # This *simulates* 1Password dying or becoming unresponsive in order
        # to demonstrate OPCmdFailedException being raised.
        # NOTE: This is not a required step for normal use
        simulate_1password_failure()
    except OPCmdFailedException:
        pass
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
