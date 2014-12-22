import maya.cmds as mc
import maya.mel as mm
import TARibbonUI
reload(TARibbonUI)
myApp = TARibbonUI.TARibbonUI()

obj1 = 'Char_lf_upArm_jnt'
obj2 = 'Char_lf_loArm_jnt'
prefix = 'gen'
side = 'lf'
element = 'upArm'
choiceAxis = '+x'

myApp.ribbonInput(obj1, obj2, prefix, side, element, choiceAxis)
mc.scaleConstraint(obj1, '%s_%s_%s_ribbon_moveGrp' % (prefix, side, element))
mc.setAttr('%s_%s_%s_upperCtrl_topGrp.visibility' % (prefix, side, element), 0)
con1 = '%s_%s_%s_lowerCtrl_topGrp' % (prefix, side, element)

obj1 = 'Char_lf_loArm_jnt'
obj2 = 'Char_lf_wrist_jnt'
prefix = 'gen'
side = 'lf'
element = 'loArm'
choiceAxis = '+x'

myApp.ribbonInput(obj1, obj2, prefix, side, element, choiceAxis)
mc.scaleConstraint(obj1, '%s_%s_%s_ribbon_moveGrp' % (prefix, side, element))
mc.setAttr('%s_%s_%s_lowerCtrl_topGrp.visibility' % (prefix, side, element), 0)
con2 = '%s_%s_%s_upperCtrl_topGrp' % (prefix, side, element)

locGrp = 'lf_elbowRibbonCtrl_zGrp'
loc = 'lf_elbowRibbon_ctrl'
mc.delete(mc.pointConstraint(obj1, locGrp))
mc.parentConstraint(obj1, locGrp, mo = True)


mc.parentConstraint(loc, con1, mo = True)
mc.parentConstraint(loc, con2, mo = True)

# ==============================================================================================


obj1 = 'Char_rt_loArm_jnt'
obj2 = 'Char_rt_wrist_jnt'
prefix = 'gen'
side = 'rt'
element = 'loArm'
choiceAxis = '-x'

myApp.ribbonInput(obj1, obj2, prefix, side, element, choiceAxis)
mc.scaleConstraint(obj1, '%s_%s_%s_ribbon_moveGrp' % (prefix, side, element))
mc.setAttr('%s_%s_%s_lowerCtrl_topGrp.visibility' % (prefix, side, element), 0)
con2 = '%s_%s_%s_upperCtrl_topGrp' % (prefix, side, element)


obj1 = 'Char_rt_upArm_jnt'
obj2 = 'Char_rt_loArm_jnt'
prefix = 'gen'
side = 'rt'
element = 'upArm'
choiceAxis = '-x'

myApp.ribbonInput(obj1, obj2, prefix, side, element, choiceAxis)
mc.scaleConstraint(obj1, '%s_%s_%s_ribbon_moveGrp' % (prefix, side, element))
mc.setAttr('%s_%s_%s_upperCtrl_topGrp.visibility' % (prefix, side, element), 0)
con1 = '%s_%s_%s_lowerCtrl_topGrp' % (prefix, side, element)

locGrp = 'rt_elbowRibbonCtrl_zGrp'
loc = 'rt_elbowRibbon_ctrl'
mc.delete(mc.pointConstraint(obj2, locGrp))
mc.parentConstraint(obj2, locGrp, mo = True)

mc.parentConstraint(loc, con1, mo = True)
mc.parentConstraint(loc, con2, mo = True)

# ==============================================================================================

obj1 = 'Char_lf_upLeg_jnt'
obj2 = 'Char_lf_loLeg_jnt'
prefix = 'gen'
side = 'lf'
element = 'upLeg'
choiceAxis = '-y'

myApp.ribbonInput(obj1, obj2, prefix, side, element, choiceAxis)
mc.scaleConstraint(obj1, '%s_%s_%s_ribbon_moveGrp' % (prefix, side, element))
mc.setAttr('%s_%s_%s_upperCtrl_topGrp.visibility' % (prefix, side, element), 0)

obj1 = 'Char_rt_upLeg_jnt'
obj2 = 'Char_rt_loLeg_jnt'
prefix = 'gen'
side = 'rt'
element = 'upLeg'
choiceAxis = '-y'

myApp.ribbonInput(obj1, obj2, prefix, side, element, choiceAxis)
mc.scaleConstraint(obj1, '%s_%s_%s_ribbon_moveGrp' % (prefix, side, element))
mc.setAttr('%s_%s_%s_upperCtrl_topGrp.visibility' % (prefix, side, element), 0)

obj1 = 'Char_lf_loLeg_jnt'
obj2 = 'Char_lf_ankle_jnt'
prefix = 'gen'
side = 'lf'
element = 'loLeg'
choiceAxis = '-y'

myApp.ribbonInput(obj1, obj2, prefix, side, element, choiceAxis)
mc.scaleConstraint(obj1, '%s_%s_%s_ribbon_moveGrp' % (prefix, side, element))
mc.setAttr('%s_%s_%s_lowerCtrl_topGrp.visibility' % (prefix, side, element), 0)

obj1 = 'Char_rt_loLeg_jnt'
obj2 = 'Char_rt_ankle_jnt'
prefix = 'gen'
side = 'rt'
element = 'loLeg'
choiceAxis = '-y'

myApp.ribbonInput(obj1, obj2, prefix, side, element, choiceAxis)
mc.scaleConstraint(obj1, '%s_%s_%s_ribbon_moveGrp' % (prefix, side, element))
mc.setAttr('%s_%s_%s_lowerCtrl_topGrp.visibility' % (prefix, side, element), 0)