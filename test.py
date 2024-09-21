from random import randint

from svgmaker import Document

doc = Document(800, 800)
doc.adjust_docstyle(True)
doc.start_document()

for i in range(50):
    doc.draw_line(
        randint(0,800),
        randint(0,800),
        randint(0,800),
        randint(0,800),
        {"stroke": f"rgb({randint(0,255)},{randint(0,255)},{randint(0,255)})", "stroke-width": "5"}
    )

rand1 = randint(0,255)
rand2 = randint(0,255)
doc.open_rect(400, 400, 300, 300, {"fill": f"rgb({rand1},0,{rand2})", "opacity": 0})
doc.animate_appear(1, 1)
doc.close_objs(1)

doc.end_document()
doc.export_document("test.svg")