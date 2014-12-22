import maya.cmds as mc
import maya.mel as mm
from functools import partial

from PIL import Image
from tools import fileUtils
reload(fileUtils)


def run() : 
	myApp = MyApp()
	myApp.show()

class MyApp() : 
	def __init__(self) : 
		self.win = 'Image2PolyWin'
		self.ui = '%s_win' % self.win

		self.defaultPath = 'D:/kan/2D/Maya/pupay/psd/modelSheet/pupeModelSheetIso'


	def show(self) : 
		if mc.window(self.ui, exists = True) : 
			mc.deleteUI(self.ui)

		mc.window(self.ui, t = 'Image2Poly Tool v.1.0')
		mc.columnLayout(adj = 1, rs = 4)

		mc.frameLayout(borderStyle = 'etchedIn', lv = False)
		mc.columnLayout(adj = 1, rs = 0)

		mc.text(l = 'Path')
		mc.textField('%s_pathTX' % self.ui, tx = self.defaultPath)
		mc.button('Load Image', c = partial(self.browseImg))

		mc.textScrollList('%s_TSL' % self.ui, numberOfRows = 8, allowMultiSelection = True)
		mc.text(l = 'size')
		mc.textField('%s_sizeTX' % self.ui, tx = 2)

		mc.button(l = 'Make', h = 30, c = partial(self.doCreatePlane))

		mc.setParent('..')
		mc.setParent('..')


		mc.showWindow()
		mc.window(self.ui, e = True, wh = [400, 400])

		self.browseImg()



	def browseImg(self, arg = None) : 
		path = mc.textField('%s_pathTX' % self.ui, q = True, tx = True)
		path = path.replace('\\', '/')

		files = fileUtils.listFile(path, 'png')

		mc.textScrollList('%s_TSL' % self.ui, e = True, ra = True)

		for each in files : 
			if not each[0] == '_' : 
				sels = mc.textScrollList('%s_TSL' % self.ui, e = True, append = each)



	def getSize(self, img, arg = None) : 

		im = Image.open(img)
		width, height = im.size

		return width, height


	def doCreatePlane(self, arg = None) : 
		path = mc.textField('%s_pathTX' % self.ui, q = True, tx = True)
		sels = mc.textScrollList('%s_TSL' % self.ui, q = True, si = True)
		size = mc.textField('%s_sizeTX' % self.ui, q = True, tx = True)

		for each in sels : 
			imgPath = '%s/%s' % (path, each)
			w, h = self.getSize(imgPath)

			poly = self.createPolyPlane(each, w, h, size)

			self.assignShader(poly, imgPath)


	def createPolyPlane(self, name, w, h, size) : 
		# 10000 px = 1 unit
		w = (float(w)/1000)*float(size)
		h = (float(h)/1000)*float(size)

		name = '%s_ply' % name.split('.')[0]

		poly = mc.polyPlane(w = 2, h = 2, sx = 4, sy = 4, ax = [0, 0, 0], cuv = 2, ch = 1, n = name)
		mc.xform(poly[0], ws = True, s = (w, h, 1.0))
		mc.makeIdentity(poly[0], apply=True, t = 1, r = 1, s = 1, n = 0)

		return poly


	def assignShader(self, obj, imgPath) : 
		# name from object
		print obj
		name = obj[0].replace('_ply', '')

		material = mc.shadingNode('lambert', asShader=True, n = '%s_shd' % name)
		fileNode = mc.shadingNode('file', asTexture = True, n = '%s_file' % name)
		placementNode = mc.shadingNode('place2dTexture', asUtility=True)

		# assign file node
		mc.setAttr('%s.fileTextureName' % fileNode, imgPath, type = 'string')

		mc.connectAttr('%s.coverage' % placementNode, '%s.coverage' % fileNode, f = True)
		mc.connectAttr('%s.translateFrame' % placementNode, '%s.translateFrame' % fileNode, f = True)
		mc.connectAttr('%s.rotateFrame' % placementNode, '%s.rotateFrame' % fileNode, f = True)
		mc.connectAttr('%s.mirrorU' % placementNode, '%s.mirrorU' % fileNode, f = True)
		mc.connectAttr('%s.mirrorV' % placementNode, '%s.mirrorV' % fileNode, f = True)
		mc.connectAttr('%s.stagger' % placementNode, '%s.stagger' % fileNode, f = True)
		mc.connectAttr('%s.wrapU' % placementNode, '%s.wrapU' % fileNode, f = True)
		mc.connectAttr('%s.wrapV' % placementNode, '%s.wrapV' % fileNode, f = True)
		mc.connectAttr('%s.repeatUV' % placementNode, '%s.repeatUV' % fileNode, f = True)
		mc.connectAttr('%s.offset' % placementNode, '%s.offset' % fileNode, f = True)
		mc.connectAttr('%s.rotateUV' % placementNode, '%s.rotateUV' % fileNode, f = True)
		mc.connectAttr('%s.noiseUV' % placementNode, '%s.noiseUV' % fileNode, f = True)
		mc.connectAttr('%s.vertexUvOne' % placementNode, '%s.vertexUvOne' % fileNode, f = True)
		mc.connectAttr('%s.vertexUvTwo' % placementNode, '%s.vertexUvTwo' % fileNode, f = True)
		mc.connectAttr('%s.vertexUvThree' % placementNode, '%s.vertexUvThree' % fileNode, f = True)
		mc.connectAttr('%s.vertexCameraOne' % placementNode, '%s.vertexCameraOne' % fileNode, f = True)
		mc.connectAttr('%s.outUV' % placementNode, '%s.uv' % fileNode, f = True)
		mc.connectAttr('%s.outUvFilterSize' % placementNode, '%s.uvFilterSize' % fileNode, f = True)

		mc.connectAttr('%s.outColor' % fileNode, '%s.color' % material, f = True)
		mc.connectAttr('%s.outTransparency' % fileNode, '%s.transparency' % material, f = True)

		mc.select(obj)
		mc.hyperShade(assign = material)

