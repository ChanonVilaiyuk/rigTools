import sys
import maya.cmds as mc
import maya.mel as mm

sys.path.append('C:/Users/Ta/Dropbox/scripts/python')
from rigTools import makeCurve
reload(makeCurve)


def zGrp(obj = '', mode = '') : 
	results = []

	if obj == '' : 
		obj = mc.ls(sl = True)[0]

	name = obj
	elements = name.split('_')
	capElements = []

	i = 0
	for eachElement in elements : 
		if not i == 0 : 
			capElements.append(eachElement.capitalize())

		else : 
			capElements.append(eachElement)

		i+=1

	newName = '%s_zGrp' % ('').join(capElements)
	offsetGrpName = '%s_offsetGrp' % ('').join(capElements)

	groupName = mc.group(obj, n = newName)
	offsetGroupName = ''

	if mode == 'offset' : 
		offsetGroupName = mc.group(groupName, n = offsetGrpName)

	return groupName, offsetGroupName


def fkRig(curveType = 'circle') : 
	ctrl = 'ctrl'
	selJnt = mc.ls(sl = True) 

	if selJnt : 
		mc.select(selJnt[0], hi = True)
		joints = mc.ls(sl = True)


		# loop each joint
		i = 0

		for each in joints : 
			cmd = 'makeCurve.%s()' % curveType
			fkCtrl = eval(cmd)
			ctrlName = ''

			# looking for jnt and Jnt

			if each.split('_')[-1] == 'jnt' or each.split('_')[-1] == 'Jnt' : 
				ctrlName = each.replace(each.split('_')[-1], ctrl)

			else : 
				ctrlName = '%s_%s' % (each, ctrl)

			# make ctrl
			curveCtrl = mc.rename(fkCtrl, ctrlName)

			# group zGrp ctrl
			curveCtrlGrp, curveOffsetGrp = zGrp(curveCtrl, 'offset')

			# snap to joint
			mc.delete(mc.parentConstraint(each, curveOffsetGrp))

			# parentConstraint ctrl to joint
			mc.parentConstraint(curveCtrl, each)

			# constraint to previous control
			if not i == 0 : 
				mc.parentConstraint(previousCtrl, curveOffsetGrp, mo = True)

			previousCtrl = curveCtrl

			i+=1








