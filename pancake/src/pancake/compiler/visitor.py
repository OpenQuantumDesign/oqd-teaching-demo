from typing import Any

from pydantic import BaseModel

########################################################################################

__all__ = ["Visitor", "Transformer", "PrettyPrint"]

########################################################################################


class Visitor:
    def visit(self, model: Any) -> Any:
        for cls in model.__class__.__mro__:
            visit_func = getattr(self, "visit_{}".format(cls.__name__), None)
            if visit_func:
                break
        if not visit_func:
            visit_func = self._visit

        new_model = visit_func(model)
        return new_model

    def _visit(self, model: Any) -> Any:
        if isinstance(
            model,
            (list,),
        ):
            [self.visit(element) for element in model]

        if isinstance(model, BaseModel):
            for key in model.__fields__.keys():
                self.visit(model.__dict__[key])
        pass


class Transformer(Visitor):
    def _visit(self, model: Any) -> Any:
        new_model = model

        if isinstance(
            model,
            (list,),
        ):
            new_model = model.__class__([self.visit(element) for element in model])

        if isinstance(model, BaseModel):
            new_fields = {}
            for key in model.__fields__.keys():
                new_fields[key] = self.visit(model.__dict__[key])
            new_model = model.__class__(**new_fields)

        return new_model


class PrettyPrint(Transformer):
    def _visit(self, model):
        if isinstance(
            model,
            (list,),
        ):
            _s = ""
            for i, element in enumerate(model):
                _s += f"-> {i}: {self.visit(element)}\n"
            _s = _s.split("\n")
            _s = [f"  {s}\n" for s in _s]
            _s = "".join(_s)
            s = f"{model.__class__.__name__}\n{_s}"
            s = s.rstrip(" \n")
            return s
        if isinstance(model, BaseModel):
            _s = ""
            for key in model.__fields__.keys():
                _s += f"-> {key}: {self.visit(model.__dict__[key])}\n"
            _s = _s.split("\n")
            _s = [f"  {s}\n" for s in _s]
            _s = "".join(_s)
            s = f"{model.__class__.__name__}\n{_s}"
            s = s.rstrip(" \n")
            return s
        return f"{model.__class__.__name__} = {model}"

    def visit_str(self, model):
        return f'{model.__class__.__name__} = "{model}"'
