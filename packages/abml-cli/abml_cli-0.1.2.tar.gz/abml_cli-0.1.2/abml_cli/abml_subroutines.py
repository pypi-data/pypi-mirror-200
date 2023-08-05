from jinja2 import Environment, FileSystemLoader
from collections import OrderedDict
from collections import defaultdict
from rich.console import Console
import os

console = Console()
path = os.path.dirname(os.path.abspath(__file__))


class Abml_Registry:
    registry = defaultdict(lambda: OrderedDict)

    @classmethod
    def register(cls, key):
        def decorator(dataclass):
            cls.registry[key] = dataclass
            return dataclass

        return decorator


def to_object_subroutines(data, **kwargs):
    object_ = {}
    for key, value in data.items():
        object_[key] = Abml_Registry.registry[key](cmds=value, **kwargs)

    return object_


@Abml_Registry.register("subroutines")
class Abml_Subroutine:
    def __init__(self, data, cwd=None):
        self.render = ""
        self.subroutines = to_object_subroutines(data)
        self.join_subs()
        self.save_file(cwd=cwd)

    def join_subs(self):
        for subroutine in self.subroutines.values():
            self.render = f"{subroutine.render}\n"

    def save_file(self, cwd=None):
        name = "subs.for"
        if cwd is None:
            with open(name, mode="w", encoding="utf-8") as f:
                f.write(self.render)
        else:
            with open(os.path.join(cwd, name), mode="w", encoding="utf-8") as f:
                f.write(self.render)


@Abml_Registry.register("dload")
class Abml_Dload:
    def __init__(self, cmds, **kwargs):
        self.env = Environment(
            loader=FileSystemLoader(os.path.join(path, "subroutines", "dload", "templates")),
            trim_blocks=False,
            lstrip_blocks=False,
            keep_trailing_newline=True,
        )

        render_map = {
            "rect": self.render_rect,
            "circle": self.render_circle,
        }

        self.render_head()
        for i, cmd in enumerate(cmds):
            key = list(cmd.keys())[0]
            values = list(cmd.values())[0]
            if i == 0:
                render = render_map[key](condition="if", **values)
            else:
                render = render_map[key](condition="else if", **values)

            self.render = f"{self.render}\n{render}"
        self.render_tail()

    def render_head(self):
        head = self.env.get_template("head.j2.f")
        head_render = head.render()
        self.render = head_render

    def render_tail(self):
        head = self.env.get_template("tail.j2.f")
        render_tail = head.render()
        self.render = f"{self.render }\n{render_tail}"

    def render_rect(self, condition, **kwargs):
        p1 = kwargs["p1"]
        p2 = kwargs["p2"]
        load = kwargs["load"]
        body = self.env.get_template("rect.j2.f")

        if "x" in kwargs:
            c1 = "y"
            c2 = "z"
        elif "y" in kwargs:
            c1 = "z"
            c2 = "x"
        else:
            c1 = "x"
            c2 = "y"

        body_render = body.render(
            condition=condition, c1=c1, c2=c2, p11=p1[0], p12=p2[0], p21=p1[1], p22=p2[1], load=load
        )
        return body_render

    def render_circle(self, condition, **kwargs):
        center = kwargs["center"]
        radius = kwargs["radius"]
        load = kwargs["load"]

        if "x" in kwargs:
            c1 = "y"
            c2 = "z"
            plane = "x"
        elif "y" in kwargs:
            c1 = "z"
            c2 = "x"
            plane = "y"
        else:
            c1 = "x"
            c2 = "y"
            plane = "z"

        body = self.env.get_template("circle.j2.f")
        body_render = body.render(
            condition=condition, c1=c1, c2=c2, plane=plane, p1=center[0], p2=center[1], r=radius, load=load
        )
        return body_render

    def save_file(self, cwd=None):
        if cwd is None:
            with open("subs.for", mode="w", encoding="utf-8") as f:
                f.write(self.render)
        else:
            with open(os.path.join(cwd, "subs.for"), mode="w", encoding="utf-8") as f:
                f.write(self.render)
