# -*- coding: utf-8 -*-

import os
import hou
import eva
import sys
import json


def saveHDA(node):
    uuid = node.userData("edit_uuid")
    
    filepath = node.type().definition().libraryFilePath() + ".json"
    dir = os.path.dirname(filepath)
    data = eva.jsonRead(filepath)

    vals = data.get("being_edited", {})
    
    if len(vals) > 1:
        msg = "Este HDA também está sendo editado em outras sessões\n Deseja salvar mesmo assim?\n\n"
        msg += "Outras sessões ativas:\n\n"+eva.jsonBeautyDump(vals, uuid)
        if not eva.confirm(msg):
            print("[EVA] Acao saveHDA() cancelada pelo usuario")
            return

    node.type().definition().updateFromNode(node)

    d_user = eva.user()
    d_file = hou.hipFile.path()
    d_node = node.path()
    d_datetime = eva.time()
    data["last_edited"] = {
        'user': d_user,
        'file': d_file,
        'date': d_datetime,
    }
    
    if eva.isTempHDA(node):
        previous_node = hou.node(vals[uuid]["node"])
        if not previous_node is None:
            eva.goToNode(previous_node)
            if not previous_node.isLockedHDA():
                previous_node.matchCurrentDefinition()
        node.destroy()
        eva.flashMessage("As edições foram salvas. Node temporário destruído")
    else:
        eva.goToNode(node)
        node.destroyUserData("is_being_edited")
        node.destroyUserData("edit_uuid")
        node.matchCurrentDefinition()
        eva.flashMessage("As edições foram salvas")


    del vals[uuid]
    data["being_edited"] = vals

    eva.jsonWrite(filepath, data)
try:
    node = kwargs.get("node", None)
except:
    node = hou.selectedNodes()[-1]
saveHDA(node)