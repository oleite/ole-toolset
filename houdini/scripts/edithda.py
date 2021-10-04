# -*- coding: utf-8 -*-

import os
import hou
import eva
import sys
import xml.etree.ElementTree as ET
import json
from datetime import datetime
import uuid

   
def editHDA(node):
    if not eva.isHDA(node):
        eva.error("Node "+node.name()+" não é um HDA")
        return

    filepath = node.type().definition().libraryFilePath() + ".json"
    dir = os.path.dirname(filepath)

    if not os.path.isfile(filepath):
        file = open(filepath, "w")
        file.write(json.dumps({}))
        file.close()
     f
    data = eva.jsonRead(filepath)

    keyname = "being_edited"
    vals = data.get(keyname, {})

    if not len(vals) is 0:
        #whos_editing = ", ".join(vals)
        msg = "Este node já está sendo editado:\n\n" + eva.jsonBeautyDump(vals) + "\n\nDeseja continuar mesmo assim?"
        if not eva.confirm(msg):
            print("[EVA] editHDA: Acao cancelada pelo usuario")
            return

    d_user = eva.user()
    d_file = hou.hipFile.path()
    d_node = node.path()
    d_datetime = eva.time()
    d_uuid = uuid.uuid4().hex

    vals[d_uuid] = {
        'user': d_user,
        'file': d_file,
        'node': d_node,
        'date': d_datetime,
    }
    data[keyname] = vals

    color = hou.Color()
    color.setHSV((300,1,1))

    if node.isInsideLockedHDA():
        #Creating EVATEMP node
        obj = hou.node("/obj")
        temp = obj.createNode(node.type().name(), node.name() + "__EVATEMP." + d_uuid)
        temp.setColor(color)
        temp.setPicked(True)
        temp.setUserData("is_temp_hda", "1")
        eva.flashMessage("Node temporário criado")
    else:
        temp = node
        temp.setUserData("is_temp_hda", "0")
        eva.flashMessage("Node desbloqueado")

    if len(temp.children()) is 0:
        temp.createNode('null')
    eva.goToNode(temp.children()[0])

    temp.setUserData("is_being_edited", "1")

    temp.setUserData("edit_uuid", d_uuid)
    temp.allowEditingOfContents()

    eva.jsonWrite(filepath, data)    
try:
    node = kwargs.get("node", None)
except:
    node = hou.selectedNodes()[-1]
editHDA(node)