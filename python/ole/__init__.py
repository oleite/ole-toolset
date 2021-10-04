import os
import sys
import inspect
import hou
import json
from datetime import datetime


TOOL_ROOT = inspect.getfile(inspect.currentframe()).replace('\\', '/').replace('/python/ole/__init__.pyc', '').replace('/python/ole/__init__.py', '')
excludedDirs = ["backup", "icons", "images"]


def error(msg):
    hou.ui.displayMessage(msg, buttons=('OK',), severity=hou.severityType.Error, default_choice=0, close_choice=-1, help=None, title="OLE")
    return
    
def confirm(msg):
    return hou.ui.displayConfirmation(msg, severity=hou.severityType.Warning, help=None, title="OLE", details=None, details_label=None, suppress=hou.confirmType.OverwriteFile)

def flashMessage(msg = "OLE", duration = 5.0, icon="$OLE_HDAs/icons/default.png"):
    getCurrentNetworkEditorPane().flashMessage(icon, msg, duration)

def goToNode(node):
    getCurrentNetworkEditorPane().setCurrentNode(node)

def jsonRead(filepath):
    file = open(filepath)
    data = json.load(file)
    file.close()
    return data

def jsonWrite(filepath, data):
    file = open(filepath, "w")
    file.write(json.dumps(data, indent=2))
    file.close()
    return True

def jsonBeautyDump(data, uuid=""):
    data = dict(data)
    if not len(uuid) is 0:
        data.pop(uuid)
    result = json.dumps(data, indent=2)
    result = result.replace("{","").replace("}","\n").replace("\""," ").replace(",", "")
    return result.strip()

def time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def listdirs(rootdir):
    dirs = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            dirs.append(d)
            dirs.extend(listdirs(d))
    return dirs

def isHDA(node):
    if node is None:
        return False
    return node.type().definition() is not None

def isTempHDA(node):
    if not isHDA(node):
        return False
    else:
        is_temp_hda = node.userData("is_temp_hda")
        if is_temp_hda is None:
            return False
        else:
            is_temp_hda = bool(int(is_temp_hda))
            return is_temp_hda

def isBeingEdited(node):
    if node.isLockedHDA():
        return False
    if not isHDA(node):
        return False
    is_being_edited = node.userData("is_being_edited")
    if is_being_edited is None:
        return False
    else:
        is_being_edited = bool(int(is_being_edited))
        return is_being_edited

def user():
    return "oleite"

#From https://forums.odforce.net/topic/12406-getting-the-current-active-network-editor-pane/
def getCurrentNetworkEditorPane():
    editors = [pane for pane in hou.ui.paneTabs() if isinstance(pane, hou.NetworkEditor) and pane.isCurrentTab()]
    return editors[-1]