import hou
import ole
def colorChange(color, alpha):
    for i in hou.selectedItems(): i.setColor(color)
initial_color = kwargs["node"].color()
hou.ui.openColorEditor(colorChange, initial_color=initial_color)