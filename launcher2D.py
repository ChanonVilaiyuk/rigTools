import maya.cmds as mc
import maya.mel as mm
from functools import partial

from tools import fileUtils
reload(fileUtils)
from rigTools import gen2DRig
reload(gen2DRig) 
from rigTools import nonRoll
reload(nonRoll)


def run() : 
	myApp = MyApp()
	myApp.show()

class MyApp() : 
	def __init__(self) : 
		self.win = 'Launcher2DWin'
		self.ui = '%s_win' % self.win


	def show(self) : 
		if mc.window(self.ui, exists = True) : 
			mc.deleteUI(self.ui)

		mc.window(self.ui, t = '2D Launcher v.1.0')
		mc.columnLayout(adj = 1, rs = 4)

		mc.button(l = 'AutoRig', h = 30, bgc = [0.8, 0.8, 0.8], c = partial(self.autoRig))
		mc.button(l = '+ Non Roll', h = 30, bgc = [0.8, 0.8, 0.8], c = partial(self.addNonRoll))
		mc.button(l = '+ Rig Extrude', h = 30, bgc = [0.8, 0.8, 0.8], c = partial(self.rigExtrudePlane))
		mc.button(l = '+ Skin Curve', h = 30, bgc = [0.8, 0.8, 0.8], c = partial(self.skinCurve))
		mc.button(l = '+ Arm Sleeve', h = 30, bgc = [0.8, 0.8, 0.8], c = partial(self.armSleeve))
		mc.button(l = '+ Arm Scale', h = 30, bgc = [0.8, 0.8, 0.8], c = partial(self.armScale))
		mc.button(l = '+ pelvisExtran Jnt ', h = 30, bgc = [0.8, 0.8, 0.8], c = partial(self.pelvisExtraJnt))
		mc.button(l = 'Import Jnt template', h = 30, bgc = [0.7, 0.7, 0.7], c = partial(self.importJntTemplate))
		mc.button(l = 'Import image to plane', h = 30, bgc = [0.7, 0.7, 0.7], c = partial(self.importImage2Plane))
		mc.button(l = 'Make curve from 2 vertices', h = 30, bgc = [0.6, 0.6, 0.6], c = partial(self.makeCurve2point))
		mc.button(l = 'Rename curve set1', h = 30, bgc = [0.6, 0.6, 0.6], c = partial(self.rename1))
		mc.button(l = 'Rename curve set2', h = 30, bgc = [0.5, 0.5, 0.5], c = partial(self.rename2))
		mc.button(l = 'Rig depth joint', h = 30, bgc = [0.5, 0.5, 0.5], c = partial(self.rigDepthJoint))
		mc.button(l = 'Add depth joint attr', h = 30, bgc = [0.4, 0.4, 0.4], c = partial(self.addJntAttr))
		mc.button(l = 'Add depth XY attr', h = 30, bgc = [0.4, 0.4, 0.4], c = partial(self.addDepthXY))
		mc.button(l = 'Import face ctrl', h = 30, bgc = [0.4, 0.4, 0.4], c = partial(self.importFaceCtrl))
		mc.button(l = 'Rig Face', h = 30, bgc = [0.3, 0.3, 0.3], c = partial(self.rigFace))
		mc.button(l = 'Rig Face2', h = 30, bgc = [0.3, 0.3, 0.3], c = partial(self.rigFace2))
		mc.button(l = 'Clean Name', h = 30, bgc = [0.3, 0.3, 0.3], c = partial(self.cleanNameCmd))
		mc.button(l = 'Hide unused', h = 30, bgc = [0.3, 0.3, 0.3], c = partial(self.hideUnused))

		mc.showWindow()

		mc.window(self.ui, e = True, wh = [200, 600])

	def autoRig(self, arg = None) : 
		mm.eval('source taAutoRigUI.mel;')


	def addNonRoll(self, arg = None) : 
		nonRoll.runWithRig()


	def rigExtrudePlane(self, arg = None) : 
		nonRoll.rigExtrudePlane()


	def importJntTemplate(self, arg = None) : 
		mc.file('D:/kan/2D/Maya/template/joint.ma', i = True)


	def importFaceCtrl(self, arg = None) : 
		mc.file('D:/kan/2D/Maya/template/face_ctrl.ma', i = True)


	def importImage2Plane(self, arg = None) : 
		from rigTools import image2PolyPlane as im
		reload(im)
		im.run()


	def makeCurve2point(self, arg = None) : 
		from rigTools import createCurve as cc
		reload(cc)
		cc.run()


	def rename1(self, arg = None) : 
		naming1 = ['L_arm_profileCrv', 'L_arm_pathCrv', 'R_arm_profileCrv', 'R_arm_pathCrv']

		sels = mc.ls(sl = True)

		for i in range(len(sels)) :  
		    mc.rename(sels[i], naming1[i])

	def rename2(self, arg = None) : 
		naming2 = ['L_leg_profileCrv', 'L_leg_pathCrv', 'R_leg_profileCrv', 'R_leg_pathCrv']

		sels = mc.ls(sl = True)

		for i in range(len(sels)) :  
		    mc.rename(sels[i], naming2[i])


	def rigDepthJoint(self, arg = None) : 
		gen2DRig.rigJntDepth()


	def addJntAttr(self, arg = None) : 
		gen2DRig.addDepthJntAttr()


	def addDepthXY(self, arg = None) : 
		gen2DRig.addXYJntAttr('layer_setting')


	def rigFace(self, arg = None) : 
		gen2DRig.rigFace()


	def rigFace2(self, arg = None) : 
		gen2DRig.rigFace2()


	def cleanNameCmd(self, arg = None) : 
		from rigTools import cleanName
		reload(cleanName)
		cleanName.show()


	def hideUnused(self, arg = None) : 
		gen2DRig.hideUnused()


	def skinCurve(self, arg = None) : 
		gen2DRig.skinCurve()


	def armScale(self, arg = None) : 
		gen2DRig.armScale()


	def armSleeve(self, arg = None) : 
		gen2DRig.armSleeve()


	def pelvisExtraJnt(self, arg = None) : 
		gen2DRig.pelvisExtraJnt()