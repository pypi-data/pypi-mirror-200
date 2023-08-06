import time
import os
import pathlib
import sys
from rich import print as rprint
from rich.console import Console
import typer

from watchdog.observers import Observer
from pyfiglet import Figlet

# add the base directory to the path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from menu import menu
from wrapperComponents import WrapperComponents as wp

# handlers
from wrs import WrsHandler
from wro import WroHandler
from wtch import WatchForHandler

# Version Control
from versionControl import VersionControl
from GLOBALS import VARS as v


class Entries:
    def __init__(self):
        self.entries = {}
        self.c = Console()

    def add(self, name: str, value):
        self.entries[name] = value

    def get(self, name: str) -> str | list | None | bool | int | list[str]:
        return self.entries[name]

    def makeMode(self):
        MODE = menu(
            "Choose the mode you want to use:",
            "select",
            [("Watch and Run Self (WRS)", "wrs"), ("Watch and Run Other (WRO)", "wro")],
        )
        self.add("mode", MODE)

    def makeLang(self):
        self.language = menu(
            "Choose the language you want to use:",
            "select",
            [("python", "python"), ("ruby", "ruby"), ("c", "c"), ("c++", "c++")],
        )
        self.add("lang", self.language)

    def makeCParams(self):
        wywu = wp.textWrapBold("Enter the compiler name you want to use : ")
        ccho = wp.textWrapBold("( g++ | gcc | ...) ", "green")
        CMD = self.c.input(f"{wywu}{ccho}")
        self.add("cmd", CMD)
        opt1 = wp.textWrapBold("Enter flags you want to use : ")
        default = wp.textWrapBold("(none) ", "green")
        FLAGS = self.c.input(f"{opt1}{default}").split(" ")
        if FLAGS in ["none", "", " "]:
            FLAGS = [""]
        self.add("flags", FLAGS)
        output = wp.textWrapBold("Enter the output attributes you want to use: ")
        default = wp.textWrapBold("(-o) ", "green")
        OUTPUT_ATTRIBUTE = self.c.input(f"{output}{default}")
        if OUTPUT_ATTRIBUTE in ["", " "]:
            OUTPUT_ATTRIBUTE = "-o"
        self.add("output_attr", OUTPUT_ATTRIBUTE)
        output_name = wp.textWrapBold("Enter the output name you want: ")
        default = wp.textWrapBold("(out) ", "green")
        OUTPUT_FILE = self.c.input(f"{output_name}{default}").lower()
        if OUTPUT_FILE in ["", " "]:
            OUTPUT_FILE = "out"
        self.add("output_file", OUTPUT_FILE)

    def makeCommand(self):
        try:
            if self.language == "python":
                CMD = ["py", "python3"]
                self.add("cmd", CMD)
            elif self.language == "ruby":
                CMD = ["ruby", "ruby"]
                self.add("cmd", CMD)
            elif self.language in ["c++", "c"]:
                self.makeCParams()
            else:
                err = wp.textWrapBold("Wrong language", "red")
                rprint(f"❌ {err}")
                sys.exit(1)
        except KeyboardInterrupt:
            rprint(
                f"{wp.textWrapBold('Error: ', 'red')}{wp.textWrapBold('KeyboardInterrupt')}"
            )
            sys.exit(1)

    def makePaths(self):
        # Automatic detection of the working directory
        BASE_DIR = pathlib.Path(__file__).parent.absolute().cwd()
        self.add("base_dir", BASE_DIR)
        try:
            if self.get("lang") == "python":
                # print(python_files)
                FILE = menu("Choose the file you want to run:", "file")
            elif self.get("lang") == "ruby":
                # print(ruby_files)
                FILE = menu("Choose the file you want to run:", "file")

            elif self.get("lang") == "c":
                FILE = menu("Choose the file you want to run:", "file")

            elif self.get("lang") == "c++":
                # print(cpp_files)
                FILE = menu("Choose the file you want to run:", "file")

            if self.get("mode") == "wro":
                # print(all_files)
                FILE_TO_WATCH = menu("Choose the file you want to watch:", "file")

        except KeyboardInterrupt:
            rprint(
                f"{wp.textWrapBold('Error: ', 'red')}{wp.textWrapBold('KeyboardInterrupt')}"
            )
            sys.exit(1)
        THE_FILE = os.path.join(self.get("base_dir"), f"{FILE}")
        self.add("the_file", THE_FILE)
        if self.get("mode") == "wro":
            THE_FILE_TO_WATCH = os.path.join(self.get("base_dir"), f"{FILE_TO_WATCH}")
            self.add("the_file_to_watch", THE_FILE_TO_WATCH)
        rprint(self.get("the_file"))
        # Check if the file's path is valid exist
        if not os.path.exists(THE_FILE):
            err = wp.textWrapBold(f"The file {THE_FILE} doesn't exist", "red")
            rprint(f"❌ {err}")
            sys.exit(1)

        # Check if the file's path to watch is valid exist
        if self.get("mode") == "wro" and not os.path.exists(THE_FILE_TO_WATCH):
            err = wp.textWrapBold(
                f"The file {THE_FILE_TO_WATCH} doesn'tOUTPUT_FILE exist", "red"
            )
            rprint(f"❌ {err}")
            sys.exit(1)

        if self.get("lang") in ["c++", "c"]:
            COMMAND_LIST = [self.get("cmd")]
            if self.get("flags")[0] != "":
                COMMAND_LIST.extend(iter(self.get("flags")))
            COMMAND_LIST.append(self.get("the_file"))
            COMMAND_LIST.append(self.get("output_attr"))
            COMMAND_LIST.append(self.get("output_file"))
            self.add("command_list", COMMAND_LIST)
        else:
            self.add("command_list", None)

    def make(self):
        self.makeMode()
        self.makeLang()
        self.makeCommand()
        self.makePaths()

    def __str__(self):
        return str(self.entries)

    def __repr__(self):
        return str(self.entries)


class BeautifulOutput:
    def __init__(self, e: Entries = None) -> None:
        self.lang = e.get("lang") if e else None
        self.the_file = e.get("the_file") if e else None

    def _start(self):
        os.system("cls" if os.name == "nt" else "clear")
        f = Figlet(font="colossal", width=80)
        print(f.renderText("Change"))
        print(f.renderText("Detect"))

    def _out(self, lang: str):
        if v.verbose:
            custom_fig = Figlet(font="colossal")
            print(custom_fig.renderText(lang))
            rprint(
                f"{wp.textWrapBold('[FILE] ')}{wp.format_file_path_link(self.the_file)}"
            )
        else:
            rprint(
                f"{wp.textWrapBold('[FILE] ')}{wp.format_file_path_link(self.the_file)}"
            )

    def _run(self):
        # clear the terminal
        os.system("cls" if os.name == "nt" else "clear")
        if self.lang in ["ruby", "rb"]:
            self._out("Ruby")
        elif self.lang in ["python", "py", "python3"]:
            self._out("Python")
        elif self.lang in ["c++", "cpp"]:
            self._out("C++")
        elif self.lang == "c":
            self._out("C")

    def __str__(self):
        return f"BeautifulOutput({self.lang}, {self.the_file})"


class _Watcher:
    def __init__(self, handler_type: WrsHandler, dir_to_watch: str = os.getcwd()):
        self.DIRECTORY_TO_WATCH = dir_to_watch
        self.observer = Observer()
        self.handler_type = handler_type

    def run(self):
        event_handler = self.handler_type
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except Exception or KeyboardInterrupt as e:
            self.observer.stop()
            rprint(f"{wp.textWrapBold('Error: ', 'red')}{wp.textWrap(e)}")

    def runFor(self, seconds: int):
        event_handler = self.handler_type
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            time.sleep(seconds + 3)
            self.observer.stop()
        except Exception or KeyboardInterrupt as e:
            self.observer.stop()
            rprint(f"{wp.textWrapBold('Error: ', 'red')}{wp.textWrap(e)}")

        self.observer.join()


def activate() -> None:
    """
    ACTIVATE
    --------
    Detect change in the working directory and execute the program chosen.
    Two modes of execution are available to you:
            * Based on observing a specific file for changes and executing another file. (Watch and Run Other) `WRO`
            * Observing a certain file and using the same file to conduct the test. (Watch and Run Self) `WRS`
    """

    BeautifulOutput()._start()

    try:
        e = Entries()
        e.make()

        if e.get("mode") == "wrs":
            wh = WrsHandler(
                the_file=e.get("the_file"),
                command_list=e.get("command_list"),
                language=e.get("lang"),
                base_dir=e.get("base_dir"),
                cmd=e.get("cmd"),
            )
            BeautifulOutput(e)._run()
            mode = wp.textWrapBold("(WRS)", "green")
        else:
            wh = WroHandler(
                the_file=e.get("the_file"),
                the_file_to_watch=e.get("the_file_to_watch"),
                command_list=e.get("command_list"),
                language=e.get("lang"),
                base_dir=e.get("base_dir"),
                cmd=e.get("cmd"),
            )
            BeautifulOutput(e)._run()
            mode = wp.textWrapBold("(WRO)", "green")
        w = _Watcher(wh, e.get("base_dir"))
        print(" ")
        rprint(f"Watching in {mode} mode...")
        print(" ")
        w.run()
    except KeyboardInterrupt:
        # pipe the error number to the shell
        rprint(
            f"{wp.textWrapBold('Error: ', 'red')}{wp.textWrap('Keyboard Interrupt')}"
        )
        sys.exit(0)


def watchFor(ms: int):
    """
    WATCH FOR
    ---------
    Watch for changes in the currentdir and return a json
    """
    res = _Watcher(WatchForHandler(ms)).runFor(ms / 1000)
    rprint(res)


class Assets:
    base_dir = os.path.dirname(os.path.abspath(__file__))

    @classmethod
    def get_version(cls):
        v = VersionControl()
        return f"changedetector\n{v.getVersion()}"

    @classmethod
    def check_version(cls):
        v = VersionControl()
        v.main()


app = typer.Typer(add_completion=True, name="detectchange")


@app.command(help="Get the version of the program")
def version():
    rprint(f"{Assets.get_version()}")
    sys.exit(0)


@app.command(help="Check if there is a new version of the program")
def check():
    Assets.check_version()


@app.command(
    help="Watch for changes in the current directory and execute the program chosen",
    name="watch",
)
def run(
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    if verbose:
        v.verbose = True
    else:
        v.verbose = False
    activate()


if __name__ == "__main__":
    app()
