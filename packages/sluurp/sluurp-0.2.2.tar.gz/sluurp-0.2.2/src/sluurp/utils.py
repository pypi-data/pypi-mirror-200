import subprocess
import platform as _platform_mod
from shutil import which


def has_sbatch_available(platform="Linux"):
    return which("sbatch") is not None


def has_scancel_available():
    return which("scancel") is not None


def has_scontrol_available():
    return which("scontrol") is not None


def get_partitions() -> tuple:
    """
    return a list of existing partition
    """
    # sinfo -O partition
    process = SubProcessCommand(command="sinfo -O partition")
    try:
        res = process.run()
    except Exception:
        pass
    else:
        return filter(
            lambda x: x != "",
            [str(line).replace(" ", "") for line in res.split("\n")],
        )


class SubProcessCommand:
    def __init__(self, command, platform="Linux"):
        if platform != _platform_mod.system():
            raise ValueError
        self._command = command
        self.raw_stdout = None
        self.raw_stderr = None

    def run(self):
        stdout, stderr = self.launch_command()
        self.raw_stdout = stdout.decode("utf-8")
        self.raw_stderr = stderr.decode("utf-8")
        return self.interpret_result(self.raw_stdout, self.raw_stderr)

    def interpret_result(self, stdout, stderr):
        return stdout

    def launch_command(self):
        process = subprocess.Popen(
            self._command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return process.communicate()

    __call__ = run
