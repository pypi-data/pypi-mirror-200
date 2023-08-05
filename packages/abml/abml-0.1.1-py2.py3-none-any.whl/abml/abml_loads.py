from abml_dataclass import Abml_Registry
from abml_helpers import Abml_Helpers, cprint
from abaqusConstants import USER_DEFINED, UNSET, UNIFORM
from regionToolset import Region


@Abml_Registry.register("loads")
class Abml_Loads(Abml_Helpers):
    def __init__(self, name, model, type, **kwargs):  # noqa
        self.name = name
        self.model = model
        self.type = type
        self.kwargs = kwargs
        self.map = {"pressure": self.pressure, "gravity": self.gravity}
        self.distribution_type_map = {
            "user_defined": USER_DEFINED,
            "uniform": UNIFORM,
        }

        self.create()

    def create(self):
        self.map[self.type]()

    def pressure(self):
        kwargs = {
            "name": self.name,
            "createStepName": self.kwargs["step"],
            "region": Region(side1Faces=self.model.assembly.get_seq_from_surface_list(self.kwargs["faces"])),
            "distributionType": self.distribution_type_map[self.kwargs.get("distribution_type", "uniform")],
            "magnitude": self.kwargs.get("magnitude", 0.0),
            "amplitude": self.kwargs.get("amplitude", UNSET),
        }

        self.model.m.Pressure(**kwargs)

    def gravity(self):
        kwargs = {
            "name": self.name,
            "createStepName": self.kwargs["step"],
            "region": None,
            "distributionType": self.distribution_type_map[self.kwargs.get("distribution_type", "uniform")],
            "comp1": self.kwargs.get("comp1", 0.0),
            "comp2": self.kwargs.get("comp2", 0.0),
            "comp3": self.kwargs.get("comp3", 0.0),
            "amplitude": self.kwargs.get("amplitude", UNSET),
        }

        self.model.m.Gravity(**kwargs)
