import os
import sys
import inspect
import hou


msg_path = os.path.expanduser("~/mensagem.txt")
if not os.path.isfile(msg_path):
    with open(msg_path, "a") as f:
        f.write("vose foi haseado por le lait")
with open(msg_path, "r") as f:
    print ''.join(f.readlines())


tool_root = os.path.dirname(inspect.getfile(inspect.currentframe()).replace('\\', '/').replace('/python2.7libs/pythonrc.pyc', '').replace('/python2.7libs/pythonrc.py', ''))

python_root = '%s/python' % tool_root
if python_root not in sys.path:
	sys.path.append(python_root)
 
lib_root = '%s/ole/lib' % python_root
if lib_root not in sys.path:
	sys.path.append(lib_root)
 
houdini_program_directory = hou.getenv('HFS')
pyside2_root = '%s/python27/lib/site-packages-ui-forced/PySide2' % houdini_program_directory.replace('\\', '/')
if pyside2_root not in sys.path:
	sys.path.append(pyside2_root)





import ole

olepath = tool_root.replace('/00_Pipeline/oleldir','')
hdas = olepath+"/houdini/HDAs"

hou.putenv('OLE_TOOL', tool_root)
hou.putenv('OLE_HDAs', hdas)





#===================================
#quase o mesmo codigo do createhda.py
rootdir = hdas
excludedDirs = ole.excludedDirs
treeDirs = ole.listdirs(rootdir)
treeDirs = [s.replace('\\', '/') for s in treeDirs]

#Remover excludedDirs[] da treeDirs[]
treeDirsN = []
for dir in treeDirs:
    if not any(excluded in dir for excluded in excludedDirs):
        treeDirsN.append(dir)
treeDirs = treeDirsN
#=====================================

dirs = ";".join(treeDirs)
otlscanpath = hdas + ";" + dirs + ";&"
hou.allowEnvironmentToOverwriteVariable("HOUDINI_OTLSCAN_PATH", True)
os.environ["HOUDINI_OTLSCAN_PATH"] = otlscanpath
hou.putenv("HOUDINI_OTLSCAN_PATH",os.environ["HOUDINI_OTLSCAN_PATH"])





# hou.allowEnvironmentToOverwriteVariable("JOB", True)
# os.environ["JOB"] = someJobPath
# hou.putenv("JOB",os.environ["JOB"])