import maya.cmds as mc
import maya.mel as mm
from functools import partial

def run() : 
	myApp = MyApp()
	myApp.show()


class MyApp() : 

	def __init__(self) : 
		self.ui = 'customCurveWin'

	def show(self) : 
		if mc.window(self.ui, exists = True) : 
			mc.deleteUI(self.ui)

		mc.window(self.ui, t = 'Create curve v.1.0')
		mc.columnLayout(adj = 1, rs = 4)

		mc.text(l = 'cv') 
		mc.textField('%s_cvTX' % self.ui, tx = 4)

		mc.button(l = 'Create', c = partial(self.uiCmd))

		mc.showWindow()
		mc.window(self.ui, e = True, wh = [100, 100])

	def uiCmd(self, arg = None) : 
		value = int(mc.textField('%s_cvTX' % self.ui, q = True, tx = True))
		point2Curve(value)




def point2Curve(spans) : 
	sels = mc.ls(sl = True)

	if len(sels) == 2 : 
		point1 = sels[0]
		point2 = sels[1]

		pos1 = mc.xform(point1, q = True, ws = True, t = True)
		pos2 = mc.xform(point2, q = True, ws = True, t = True)

		result = mc.curve(d = 1, p=[pos1, pos2], k=[0,1] )

		mc.rebuildCurve(result, rpo = 1, rt = 0, end = 1, kr = 0, kcp = 0, kep = 1, kt = 0, s = spans, d = 3, tol = 0.0001)

		mc.select(result)
		mm.eval('CenterPivot')

		return result

def points2Curve() : 
	sels = mc.ls(sl = True)

	if len(sels) > 4 : 
		p = []
		k = [-1, 0]
		for each in sels : 
			pos = mc.xform(each, q = True, ws = True, t = True)
			p.append(pos)
