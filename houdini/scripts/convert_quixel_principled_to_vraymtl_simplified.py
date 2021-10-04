import os
import hou

def convert_quixel_principled_to_vraymtl(node):
    textures = {
        "diff": node.parm("basecolor_texture").eval(),
        "rough": node.parm("rough_texture").eval(),
        "normal": node.parm("baseNormal_texture").eval(),
        "opac": node.parm("opaccolor_texture").eval(),
        "disp": node.parm("dispTex_texture").eval(),
    }

    texlist = list(textures.values())
    
    prefix = os.path.commonprefix(texlist ).rstrip("_")+"/"
    prefix = os.path.basename(os.path.normpath(prefix))

    dispoffset = node.parm("dispTex_offset").eval()
    dispscale = node.parm("dispTex_scale").eval()

    node.bypass(1)
    v_matbuilder = node.parent().createNode("vray_vop_material", node.name()+"_vray")
    v_matbuilder.move((-3,0))
    v_matbuilder.parm("ogl_tex1").set(textures["diff"])
    v_matbuilder.parm("ogl_opacitymap").set(textures["opac"])

    v_mtl = hou.node(v_matbuilder.path()+"/vrayMtl")
    v_mtl.parm("bump_type").set("1") #set Bump Type to "Normal (Tangent)"
    v_mtl.parmTuple("reflect").set((1,1,1,1))

    v_invert = v_mtl.createInputNode(v_mtl.inputIndex("reflect_glossiness"), "VRayNodeTexInvert", "inv_rough_to_gloss")

    v_out = hou.node(v_matbuilder.path()+"/vrayOutput")

    v_disp = v_out.createInputNode(1, "VRayNodeGeomDisplacedMesh", "displacement")
    v_disp.parm("displacement_amount").set(dispscale)
    v_disp.parm("displacement_shift").setExpression('ch("displacement_amount") * ' + str(dispoffset))
    
    parameters = {
        "diff": {
            "out_node": v_mtl,
            "out_node_idx": v_mtl.inputIndex("diffuse"),
            "raw": False
        },
        "rough": {
            "out_node": v_invert,
            "out_node_idx": 0,
            "raw": True
        },
        "normal": {
            "out_node": v_mtl,
            "out_node_idx": v_mtl.inputIndex("bump_map"),
            "raw": True
        },
        "opac": {
            "out_node": v_mtl,
            "out_node_idx": v_mtl.inputIndex("opacity"),
            "raw": True
        },
        "disp": {
            "out_node": v_disp,
            "out_node_idx": 0,
            "raw": True
        },
    }

    for textype in parameters:
        vals = parameters[textype]
        out_node = vals["out_node"]
        out_node_idx = vals["out_node_idx"]
        raw = vals["raw"]

        file_node = out_node.createInputNode(out_node_idx, "VRayNodeMetaImageFile", textype + "_map")
        file_node.parm("BitmapBuffer_file").set(textures[textype])
        if raw:
            file_node.parm("BitmapBuffer_color_space").set("0")
            file_node.parm("BitmapBuffer_rgb_color_space").set("raw")

node = hou.selectedNodes()[-1]
convert_quixel_principled_to_vraymtl(node)