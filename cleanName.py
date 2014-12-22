import maya.cmds as mc
import maya.mel as mm


def show() : 
	if mc.window('clearNameWin', exists = True) : 
		mc.deleteUI('clearNameWin')

	mc.window('clearNameWin', t = 'Remove name')
	mc.columnLayout(adj = 1, rs = 4)
	mc.text(l = 'Remove text')
	mc.textField('nameTX', tx = 'pasted__')

	mc.button(l = 'Remove name from all scene', h = 30, bgc = [0.2, 0.4, 0.9], c = removeNameCmd)

	mc.showWindow()
	mc.window('clearNameWin', e = True, wh = [200, 120])


def removeNameCmd(arg = None) : 
	allNodes = mc.ls()
	text = mc.textField('nameTX', q = True, tx = True)

	for each in allNodes : 
	    newName = each.replace(text, '')
	    try : 
	        mc.rename(each, newName)
	        
	    except : 
	        pass