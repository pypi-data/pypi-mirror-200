from abml_dataclass import Abml_Registry

# from abml_helpers import cprint
from abaqus import mdb
from abaqusConstants import ANALYSIS, DEFAULT, OFF
import os
from shutil import copy, move


@Abml_Registry.register("jobs")
class Abml_Job:
    def __init__(self, name, model, **kwargs):  # noqa
        self.name = str(name)
        self.model = model
        self.kwargs = kwargs
        self.create()

    def create(self):
        subroutine_flag = self.kwargs.get("subroutine", False)
        if subroutine_flag:
            subroutine_path = os.path.abspath("subs.for")
        else:
            subroutine_path = None

        kwargs = {
            "name": self.name,
            "model": self.model.name,
            "description": self.kwargs.get("description", ""),
            "type": ANALYSIS,
            "userSubroutine": subroutine_path,
            "numCpus": self.kwargs.get("cpus", 1),
            "numGPUs": self.kwargs.get("gpus", 0),
            "multiprocessingMode": DEFAULT,
        }

        mdb.Job(**kwargs)

    def write_input(self):
        mdb.jobs[self.name].writeInput(consistencyChecking=OFF)

    def write_and_copy_input_to_path(self, path):
        self.write_input()
        filename = "{}.inp".format(self.name)
        copy(filename, os.path.join(path, filename))

    def write_and_move_input_to_path(self, path):
        self.write_input()
        filename = "{}.inp".format(self.name)
        move(filename, os.path.join(path, filename))
