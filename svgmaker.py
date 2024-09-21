#==DEKL================================
from io import open
from typing import Tuple, Union

#==FUNK================================
def concat_params(params: dict, style: dict, other_params: dict, invisible: bool) -> dict:
    params |= other_params
    if invisible:
        params |= {"opacity": "0"}
    if len(style):
        params |= {"style": format_style_dict(style)}
    return params

def format_style_dict(style: dict) -> str:
    return "; ".join(f"{key}: {val}" for key, val in style.items())


#==KLAS================================
class Document:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.text = []
        self.current_indent = 0
        self.opened_tags = []

        # ds = docstyle
        self.ds_attr_indent = False


    # -----------------------
    def adjust_docstyle(self, indented_attrs: bool = False):
        self.ds_attr_indent = indented_attrs

    # -----------------------
    def write_lines(self, lines: Union[list[str], str]) -> None:
        if type(lines) == str:
            tabbed = ["    "*self.current_indent + lines]
        else:
            tabbed = ["    "*self.current_indent + line for line in lines]
        self.text.extend(tabbed)
    
    def open_indent(self, closing_tag: str) -> None:
        self.current_indent += 1
        self.opened_tags.append(closing_tag)
    
    def close_indent(self) -> None:
        tag = self.opened_tags.pop()
        self.current_indent -= 1
        self.write_lines(tag)



    # -----------------------
    def make_obj(self, obj_type: str, obj_params: dict, closer = "/>", indented_attrs: bool = None):
        """
        obj_type:   e.g. rect, path, ...\n
        obj_params: e.g. {"height": "100"}\n
        indented_attrs: if attributes are organised with indents (if not given, the document standard applies)
        """
        if not len(obj_params):
            self.write_lines(f"<{obj_type}{closer}")
            return
        
        if indented_attrs == None:
            # if no value given, indented_attrs is set to the document standard for attr indents
            indented_attrs = self.ds_attr_indent
        
        if indented_attrs:
            text_params = [f"{key}=\t\"{val}\"" for key,val in obj_params.items()]
            self.write_lines(f"<{obj_type}")
            self.open_indent(closer)
            self.write_lines(text_params)
            self.close_indent()
            return
        
        text_params = [f"{key}=\"{val}\"" for key,val in obj_params.items()]
        text = f"<{obj_type} " + " ".join(param for param in text_params) + closer
        self.write_lines(text)

    def open_obj(self, obj_type: str, obj_params: dict, indented_attrs: bool = None):
        """open an object, for example a <g> or <svg> like an opening bracket that will be closed with the next close_indent """
        self.make_obj(obj_type, obj_params, ">", indented_attrs)
        self.open_indent(f"</{obj_type}>")
    
    def close_objs(self, indent_levels: int = None):
        if indent_levels:
            for _ in range(indent_levels):
                self.close_indent()
            return
        for _ in range(self.current_indent-1):
                self.close_indent()



    # -----------------------
    def start_document(self):
        self.write_lines("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>")
        params = {
            "width": str(self.width),
            "height": str(self.height),
            "xmlns": "http://www.w3.org/2000/svg"
        }
        self.open_obj("svg", params)
    
    def end_document(self):
        tags_to_be_closed = self.opened_tags[:] #copying by value
        for tag in tags_to_be_closed:
            self.close_indent()
    
    def export_document(self, filename: str):
        writex = "\n".join(line for line in self.text)

        with open(filename, "w", encoding="utf-8") as wri:
            wri.write(writex)
    


    # -----------------------
    def draw_circle(self, x: float, y: float, r: float, style: dict = {}, other_params: dict = {}, centered: bool = True, invisible: bool = False, indented_attrs: bool = None, open: bool = False):
        if not centered:
            x += r
            y += r
        params = {
            "cx": str(x),
            "cy": str(y),
            "r": str(r)
        }
        params = concat_params(params, style, other_params, invisible)
        if open:
            self.open_obj("circle", params, indented_attrs=indented_attrs)
        else:
            self.make_obj("circle", params, indented_attrs=indented_attrs)
    
    def open_circle(self, x: float, y: float, r: float, style: dict = {}, other_params: dict = {}, centered: bool = True, invisible: bool = False, indented_attrs: bool = None):
        self.draw_circle(x, y, r, style, other_params, centered, invisible, indented_attrs, True)


    def draw_ellipse(self, x: float, y: float, rx: float, ry: float, style: dict = {}, other_params: dict = {}, centered: bool = True, invisible: bool = False, indented_attrs: bool = None, open: bool = False):
        if not centered:
            x += rx
            y += ry
        params = {
            "cx": str(x),
            "cy": str(y),
            "rx": str(rx),
            "ry": str(ry)
        }
        params = concat_params(params, style, other_params, invisible)
        if open:
            self.open_obj("ellipse", params, indented_attrs=indented_attrs)
        else:
            self.make_obj("ellipse", params, indented_attrs=indented_attrs)

    def open_ellipse(self, x: float, y: float, rx: float, ry: float, style: dict = {}, other_params: dict = {}, centered: bool = True, invisible: bool = False, indented_attrs: bool = None):
        self.draw_ellipse(x, y, rx, ry, style, other_params, centered, invisible, indented_attrs, True)
    

    def draw_rect(self, x: float, y: float, w: float, h: float, style: dict = {}, other_params: dict = {}, centered: bool = False, invisible: bool = False, indented_attrs: bool = None, open: bool = False):
        if centered:
            x -= w/2
            y -= h/2
        params = {
            "x": str(x),
            "y": str(y),
            "width": str(w),
            "height": str(h)
        }
        params = concat_params(params, style, other_params, invisible)
        if open:
            self.open_obj("rect", params, indented_attrs=indented_attrs)
        else:
            self.make_obj("rect", params, indented_attrs=indented_attrs)
    
    def open_rect(self, x: float, y: float, w: float, h: float, style: dict = {}, other_params: dict = {}, centered: bool = True, invisible: bool = False, indented_attrs: bool = None):
        self.draw_rect(x, y, w, h, style, other_params, centered, invisible, indented_attrs, True)
    

    def draw_polygon(self, points: list[Tuple[float, float]], style: dict = {}, other_params: dict = {}, invisible: bool = False, indented_attrs: bool = None, open: bool = False):
        params = {
            "points": " ".join(f"{point[0]},{point[1]}" for point in points)
        }
        params = concat_params(params, style, other_params, invisible)
        if open:
            self.open_obj("polygon", params, indented_attrs=indented_attrs)
        else:
            self.make_obj("polygon", params, indented_attrs=indented_attrs)
    
    def open_polygon(self, points: list[Tuple[float, float]], style: dict = {}, other_params: dict = {}, centered: bool = True, invisible: bool = False, indented_attrs: bool = None):
        self.draw_polygon(points, style, other_params, centered, invisible, indented_attrs, True)
    

    def draw_line(self, x1: float, y1: float, x2: float, y2: float, style: dict = {}, other_params: dict = {}, centered: bool = False, invisible: bool = False, indented_attrs: bool = None, open: bool = False):
        if centered:
            x1 -= (x2-x1)
            y1 -= (y2-y1)
        params = {
            "x1": str(x1),
            "y1": str(y1),
            "x2": str(x2),
            "y2": str(y2),
        }
        params = concat_params(params, style, other_params, invisible)
        if open:
            self.open_obj("line", params, indented_attrs=indented_attrs)
        else:
            self.make_obj("line", params, indented_attrs=indented_attrs)
    
    def open_line(self, x1: float, y1: float, x2: float, y2: float, style: dict = {}, other_params: dict = {}, centered: bool = True, invisible: bool = False, indented_attrs: bool = None):
        self.draw_line(x1, y1, x2, y2, style, other_params, centered, invisible, indented_attrs, True)
    

    def draw_polyline(self, points: list[Tuple[float, float]], style: dict = {}, other_params: dict = {}, invisible: bool = False, indented_attrs: bool = None, open: bool = False):
        params = {
            "points": " ".join(f"{point[0]},{point[1]}" for point in points)
        }
        params = concat_params(params, style, other_params, invisible)
        if open:
            self.open_obj("polyline", params, indented_attrs=indented_attrs)
        else:
            self.make_obj("polyline", params, indented_attrs=indented_attrs)
    
    def open_polyline(self, points: list[Tuple[float, float]], style: dict = {}, other_params: dict = {}, centered: bool = True, invisible: bool = False, indented_attrs: bool = None):
        self.draw_polyline(points, style, other_params, centered, invisible, indented_attrs, True)
    

    def draw_text(self, x: float, y: float, text: str, style: dict = {}, other_params: dict = {}, invisible: bool = False, indented_attrs: bool = None):
        params = {
            "x": str(x),
            "y": str(y)
        }
        params = concat_params(params, style, other_params, invisible)
        self.open_obj("text", params, indented_attrs=indented_attrs)
        self.write_lines(text)
        self.close_objs(1)


    # -----------------------
    def add_blank_lines(self, linenumber: int):
        self.write_lines(["" for _ in range(linenumber)])

    def add_comment(self, text: str):
        self.make_obj("!--", {}, f" {text} -->")


    # -----------------------
    def add_animate(self, attributeName: str, dur: float, values: list):
        pass

    def animate_appear(self, begin: float, dur: float):
        if dur == 0:
            params = {
            "attributeName": "opacity",
            "to": "1",
            "begin": str(begin)
            }
            self.make_obj("set", params)
            return
        
        params = {
            "attributeName": "opacity",
            "from": "0",
            "to": "1",
            "begin": str(begin),
            "dur": str(dur),
            "fill": "freeze"
        }
        self.make_obj("animate", params)
    
    def animate_disappear(self, begin: float, dur: float):
        if dur == 0:
            params = {
            "attributeName": "opacity",
            "to": "0",
            "begin": str(begin)
            }
            self.make_obj("set", params)
            return
        
        params = {
            "attributeName": "opacity",
            "from": "1",
            "to": "0",
            "begin": str(begin),
            "dur": str(dur),
            "fill": "freeze"
        }
        self.make_obj("animate", params)
