import maya.cmds as mc
import maya.mel as mm
from functools import partial

def run() : 
    a = rigUtils()
    a.ui()


class rigUtils() : 
    def __init__(self) : 
        self.win = 'rigUtils'
        
    def ui(self) : 
        if mc.window(self.win, exists = True) : 
            mc.deleteUI(self.win)
            
        mc.window(self.win, t = 'edit model')
        mc.columnLayout(adj = 1, rs = 4)
        mc.text(l = 'Edit Model')
        mc.button('%s_editBT' % self.win, l = 'Edit', h = 30, c = partial(self.editObjectCmd), bgc = (0.9, 0.6, 0.5))
        mc.button('%s_doneBT' % self.win, l = 'Done', h = 30, en = False, c = partial(self.copyWeight), bgc = (0.4, 0.8, 0.4))
        
        mc.showWindow()
        
        mc.window(self.win, e = True, wh = [200, 100])
        
    def editObjectCmd(self, arg = None) : 
        sel = mc.ls(sl = True)
        
        editObj = sel[0]

        nodes = mc.listHistory(editObj, ag = True)
        validObj = 0

        for each in nodes : 
            if mc.objectType(each, isType = 'skinCluster') : 
                validObj = 1

        if validObj : 
            newObj = mc.duplicate(editObj)
            newObj = mc.rename(newObj, '%s' % editObj)
            mc.setAttr('%s.visibility' % editObj, 0)
            self.editObj = editObj
            self.newObj = newObj

            mc.button('%s_editBT' % self.win, e = True, en = False)
            mc.button('%s_doneBT' % self.win, e = True, en = True)

        else : 
            mm.eval('warning "Invalid object";')
        
    def copyWeight(self, arg = None) : 
        joints = mc.skinCluster(self.editObj, q = True, inf = True)
        mc.skinCluster(joints, self.newObj, tsb = True)
        
        mc.select(self.editObj, self.newObj)
        mm.eval('CopySkinWeights;')
        mc.select(self.newObj)

        mc.button('%s_editBT' % self.win, e = True, en = True)
        mc.button('%s_doneBT' % self.win, e = True, en = False)


    def checkSkin(self, obj) : 
        nodes = mc.listHistory(obj, ag = True)

        for each in nodes : 
            if mc.objectType(each, isType = 'skinCluster') : 
                return True
        
