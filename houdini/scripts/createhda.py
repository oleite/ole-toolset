# -*- coding: utf-8 -*-

import os
import hou
import sys
import xml.etree.ElementTree as ET
import eva

def createHDA(node):               
    rootdir = hou.getenv("HDAs")
    excludedDirs = ["backup", "icons", "images"]
                
    treeDirs = eva.listdirs(rootdir)
    treeDirs = [s.replace('\\', '/') for s in treeDirs]
    treeDirs = [s.replace(rootdir, '') for s in treeDirs]
    
    
    #Remover excludedDirs[] da treeDirs[]
    treeDirsN = []
    for dir in treeDirs:
        if not any(excluded in dir for excluded in excludedDirs):
            treeDirsN.append(dir)
    treeDirs = treeDirsN
    
    
    #UI prompt Name
    hda_name_input = hou.ui.readInput("Insira o nome do HDA", buttons=('OK','Cancel',), title="Nome", initial_contents=str(node), default_choice=0, close_choice=1)

    if hda_name_input[0] is 0:
        hda_name = hda_name_input[1].strip()
        hda_name = hda_name.replace(" ", "_")
        hda_name = hda_name.replace("-", "_")

        # cats = hou.nodeTypeCategories()
        # for cat in hou.nodeTypeCategories():
        #     cat = cats[cat]
        #     types = cat.nodeTypes()
        #     for type in types:
        #         print type
        #         if hda_name == type:
        #             eva.error("Um HDA com o mesmo nome ("+hda_name+") já existe.")
        #             return
    
        if len(hda_name) is 0:
            eva.error("O nome do HDA não pode estar vazio")
            eva.flashMessage("Criação de HDA cancelada")
            return

        for file in hou.hda.loadedFiles():
            if hda_name + ".hda" in file:
                eva.error("Um HDA com o mesmo nome ("+hda_name+") já existe:\n\n"+file+"\n\nTente salvá-lo com outro nome.")
                eva.flashMessage("Criação de HDA cancelada")
                return

        hda_label = hda_name.replace("_", " ")
    
        #UI prompt Directory
        hda_dir_input = hou.ui.selectFromTree(treeDirs, exclusive=True, message="Selecione uma pasta para o HDA \""+hda_name+"\"", title="Pasta \""+hda_label+"\"")
        if not len(hda_dir_input) is 0:
            hda_dir = hda_dir_input[0]
        else:
            hda_dir = ""
            
        hda_dir_full = "$HDAs" + hda_dir
        hda_file_name = hda_dir_full + "/" + hda_name + ".hda"
        name = "evaldir::" + hda_name
            
        hda_node = node.createDigitalAsset(
            name = name,
            hda_file_name = hda_file_name,
            description = hda_label,
            max_num_inputs = 1,
        )
        
        hda_node.matchCurrentDefinition()
        
        # Get HDA definition
        hda_def = hda_node.type().definition()
        
        # Update and save new HDA
        hda_options = hda_def.options()
        hda_options.setSaveInitialParmsAndContents(True)
        hda_options.setMakeInitialParmsDefaults(True)
        hda_def.setOptions(hda_options)
        hda_def.save(hda_def.libraryFilePath(), hda_node, hda_options)
        
        path = "<toolSubmenu>.EVALDIR"+hda_dir+"</toolSubmenu>"
        
        hda_def.setIcon("$HDAs/icons/default.png")
    
        #xml = ET.parse("M:/E-NOIS - .prism-evaldir/00_Pipeline/customPlugins/houdini/evaldir/scripts/Tools.shelf.xml").getroot() # CONSERTAR PATH !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #xml = ET.tostring(xml).decode()
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<shelfDocument>
  <!-- This file contains definitions of shelves, toolbars, and tools.
 It should not be hand-edited when it is being used by the application.
 Note, that two definitions of the same element are not allowed in
 a single file. -->

  <tool name="$HDA_DEFAULT_TOOL" label="$HDA_LABEL" icon="$HDA_ICON">
    <toolMenuContext name="viewer">
      <contextNetType>OBJ</contextNetType>
    </toolMenuContext>
    <toolMenuContext name="network">
      <contextOpType>$HDA_TABLE_AND_NAME</contextOpType>
    </toolMenuContext>
    <toolSubmenu>Digital Assets</toolSubmenu>
    <script scriptType="python"><![CDATA[import objecttoolutils

objecttoolutils.genericTool(kwargs, '$HDA_NAME')]]></script>
  </tool>
</shelfDocument>"""
        
        xml = xml.replace("<toolSubmenu>Digital Assets</toolSubmenu>", path)
        
        if hda_def.hasSection("Tools.shelf"):
            hda_def.sections()["Tools.shelf"].setContents(xml)
        
            # Change Content
            #content = tools.contents()
            #content = content.replace("<toolSubmenu>Digital Assets</toolSubmenu>", path)
            #tools.setContents(content)
        else:
            hda_def.addSection("Tools.shelf", xml)
            
        #hou.ui.displayMessage("HDA "+hda_name+" criado com sucesso!", buttons=('OK',), severity=hou.severityType.Message, default_choice=0, close_choice=-1)
        eva.flashMessage("HDA "+hda_name+" criado com sucesso")
    else:
        hou.ui.displayMessage("Criação do hda cancelada.", buttons=('OK',), severity=hou.severityType.Message, default_choice=0, close_choice=-1)


node = kwargs.get("node", None)
if node.canCreateDigitalAsset():
    createHDA(node)
else:
    hou.ui.displayMessage("Nao e possível criar um HDA a partir de outro HDA", buttons=('OK',), severity=hou.severityType.Error, default_choice=0, close_choice=-1)