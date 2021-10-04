# -*- coding: utf-8 -*-

import os
import hou
import eva
import sys
import json


def cancelEditingHDA(node):
    uuid = node.userData("edit_uuid")
    
    if not eva.confirm("Você tem certeza que deseja cancelar a edição desse HDA?\n Todas suas alterações feitas serão perdidas."):
        print("[EVA] Acao cancelEditingHDA() cancelada pelo usuario")
        return    

    filepath = node.type().definition().libraryFilePath() + ".json"
    dir = os.path.dirname(filepath)
    data = eva.jsonRead(filepath)

    keyname = "being_edited"
    vals = data.get(keyname, {})

    if eva.isTempHDA(node):
        previous_node = hou.node(vals[uuid]["node"])
        eva.goToNode(previous_node)
        node.destroy()
        eva.flashMessage("Edição Cancelada. Node temporário destruído")
    else:
        eva.goToNode(node)
        node.destroyUserData("is_being_edited")
        node.destroyUserData("edit_uuid")
        node.matchCurrentDefinition()
        eva.flashMessage("Edição cancelada.")

    del vals[uuid]
    data[keyname] = vals
    eva.jsonWrite(filepath, data)  
try:
    node = kwargs.get("node", None)
except:
    node = hou.selectedNodes()[-1]
cancelEditingHDA(node)