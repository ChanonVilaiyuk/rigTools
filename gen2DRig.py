import maya.cmds as mc
import maya.mel as mm

def rigJntDepth() : 
    sels = mc.ls(sl = True)

    depthGrp = 'depthJnt_grp'
    if not mc.objExists(depthGrp) : 
        depthGrp = mc.group(em = True, n = depthGrp)

    for each in sels : 
        if mc.getAttr('%s.visibility' % each) : 
            joint = mc.createNode('joint')
            
            if '_ply' in each : 
                newName = each.replace('_ply', '_jnt')
                
            else : 
                newName = '%s_jnt' % each
                
            joint = mc.rename(joint, newName)
            
            mc.delete(mc.pointConstraint(each, joint))
            mc.skinCluster(each, joint, tsb = True)
            mc.parent(joint, depthGrp)


def addDepthJntAttr(obj = 'placement_ctrlShape') : 
    sels = mc.ls(sl = True)

    for each in sels : 
        attrName = '%sZ' % each.replace('_jnt', '').replace('dp_', '')
        mc.addAttr(obj, ln = attrName, min = -10, max = 10, dv = 0)
        mc.setAttr('%s.%s' % (obj, attrName), e = True, keyable = True)

        attr = '%s.%s' % (obj, attrName)

        mdvNode = mc.createNode('multiplyDivide', n = '%s_mdv' % attrName)
        mc.setAttr('%s.input2Z' % mdvNode, 0.1)

        mc.connectAttr(attr, '%s.input1Z' % mdvNode, f = True)
        mc.connectAttr('%s.outputZ' % mdvNode, '%s.translateZ' % each, f = True)



def addXYJntAttr(obj = 'placement_ctrlShape') : 
    sels = mc.ls(sl = True)

    for each in sels : 
        attrName = each.replace('Jnt_zGrp', '').replace('dp_', '')

        mc.addAttr(obj, ln = attrName, min = -10, max = 10, dv = 0, at = 'bool')
        mc.setAttr('%s.%s' % (obj, attrName), e = True, keyable = True)
        mc.setAttr('%s.%s' % (obj, attrName), lock = True)

        mc.addAttr(obj, ln = '%sX' % attrName, min = -10, max = 10, dv = 0)
        mc.setAttr('%s.%s' % (obj, '%sX' % attrName), e = True, keyable = True)

        mc.addAttr(obj, ln = '%sY' % attrName, min = -10, max = 10, dv = 0)
        mc.setAttr('%s.%s' % (obj, '%sY' % attrName), e = True, keyable = True)

        attrX = '%s.%s' % (obj, '%sX' % attrName)
        attrY = '%s.%s' % (obj, '%sY' % attrName)

        mdvNode = mc.createNode('multiplyDivide', n = '%s_mdv' % attrName)

        mc.setAttr('%s.input2X' % mdvNode, 0.1)
        mc.connectAttr(attrX, '%s.input1X' % mdvNode, f = True)
        mc.connectAttr('%s.outputX' % mdvNode, '%s.translateX' % each, f = True)


        mc.setAttr('%s.input2Y' % mdvNode, 0.1)
        mc.connectAttr(attrY, '%s.input1Y' % mdvNode, f = True)
        mc.connectAttr('%s.outputY' % mdvNode, '%s.translateY' % each, f = True)


def rigFace() : 
    jntGrp = 'facialJnt_grp'

    if not mc.objExists(jntGrp) : 
        mc.group(em = True, n = jntGrp)

    facePolyMap = {'L_brow_ply': 'L_brow_ctrl',
                     'L_baseEye_ply': 'L_baseEye_ctrl', 
                     'L_eye_ply': 'L_eye_ctrl',
                     'R_brow_ply': 'R_brow_ctrl', 
                     'R_baseEye_ply': 'R_baseEye_ctrl', 
                     'R_eye_ply': 'R_eye_ctrl', 
                     'nose_ply': 'noseface_ctrl', 
                     'mouth_ply': 'mount_ctrl'
                     }

    for each in facePolyMap : 
        poly = each
        ctrl = facePolyMap[poly]

        if mc.objExists(poly) : 

            movePivot(ctrl, poly)

            joint = mc.createNode('joint', n = poly.replace('_ply', '_jnt'))
            mc.delete(mc.pointConstraint(poly, joint))
            mc.skinCluster(poly, joint, tsb = True)
            mc.parentConstraint(ctrl, joint)
            mc.scaleConstraint(ctrl, joint)

            mc.parent(joint, jntGrp)


def rigFace2() : 
    jntGrp = 'facialJnt_grp'

    if not mc.objExists(jntGrp) : 
        mc.group(em = True, n = jntGrp)

    facePolyMap = {'L_brow_ply': 'L_brow_ctrl',
                     'L_baseEye_ply': 'L_baseEye_ctrl', 
                     'L_eye_ply': 'L_eye_ctrl',
                     'R_brow_ply': 'R_brow_ctrl', 
                     'R_baseEye_ply': 'R_baseEye_ctrl', 
                     'R_eye_ply': 'R_eye_ctrl', 
                     'nose_ply': 'noseface_ctrl', 
                     'mouth_ply': 'mouth_ctrl', 
                     'L_eyeLine_ply': 'L_eyeLine_ctrl', 
                     'R_eyeLine_ply': 'R_eyeLine_ctrl', 
                     'L_wrinkle_ply': 'L_wrinkle_ctrl', 
                     'R_wrinkle_ply': 'R_wrinkle_ctrl'
                     }

    # facePolyMap = {'L_brow_ply': 'L_brow_ctrl',
    #                  'L_Eye_line_ply': 'L_baseEye_ctrl', 
    #                  'L_eye_ply': 'L_eye_ctrl',
    #                  'R_brow_ply': 'R_brow_ctrl', 
    #                  'R_Eye_line_ply': 'R_baseEye_ctrl', 
    #                  'R_eye_ply': 'R_eye_ctrl', 
    #                  'nose_ply': 'noseface_ctrl', 
    #                  'mouth_ply': 'mount_ctrl',
    #                  'L_wrinkle_ply': 'L_wrinkle_ctrl',
    #                  'R_wrinkle_ply': 'R_wrinkle_ctrl'
    #                  }

    for each in facePolyMap : 
        poly = each
        ctrl = facePolyMap[poly]

        if mc.objExists(poly) : 
            joint = mc.createNode('joint', n = ctrl.replace('_ctrl', '_jnt'))
            jntZgrp = mc.group(joint, n = '%sJnt_zGrp' % ctrl.replace('_ctrl', '_jnt'))
            mc.delete(mc.pointConstraint(poly, jntZgrp))
            mc.skinCluster(poly, joint, tsb = True)

            mc.pointConstraint(ctrl, joint, mo = True)

            # mc.connectAttr('%s.translateX' % ctrl, '%s.translateX' % joint, f = True)
            # mc.connectAttr('%s.translateY' % ctrl, '%s.translateY' % joint, f = True)
            # mc.connectAttr('%s.translateZ' % ctrl, '%s.translateZ' % joint, f = True)
            mc.connectAttr('%s.rotateX' % ctrl, '%s.rotateX' % joint, f = True)
            mc.connectAttr('%s.rotateY' % ctrl, '%s.rotateY' % joint, f = True)
            mc.connectAttr('%s.rotateZ' % ctrl, '%s.rotateZ' % joint, f = True)
            mc.connectAttr('%s.scaleX' % ctrl, '%s.scaleX' % joint, f = True)
            mc.connectAttr('%s.scaleY' % ctrl, '%s.scaleY' % joint, f = True)
            mc.connectAttr('%s.scaleZ' % ctrl, '%s.scaleZ' % joint, f = True)

            mc.parent(jntZgrp, jntGrp)

        else : 
            print '%s not exists' % poly


def movePivot(obj, target) : 

    loc = mc.spaceLocator()
    mc.delete(mc.pointConstraint(target, loc[0]))

    pos = mc.xform(loc[0], q=True, ws=True, t=True)
    mc.xform(obj, piv = pos)
    mc.delete(loc)


def hideUnused() : 
    hide = ['lf_allHandCtrl_grp', 'lf_handJnt_zGrp', 'rt_allHandCtrl_grp', 'rt_handJnt_zGrp', 'lf_eye_jnt', 'rt_eye_jnt', 'lwr_jaw1_jnt', 'upr_jaw1_jnt']

    for each in hide : 
        if mc.objExists(each) : 
            mc.setAttr('%s.visibility' % each, 0)



def skinCurve() :
    mc.skinCluster('lf_upArm_jnt', 'lf_loArm_jnt', 'lf_wrist_jnt', 'L_arm_pathCrv')
    mc.skinCluster('rt_upArm_jnt', 'rt_loArm_jnt', 'rt_wrist_jnt', 'R_arm_pathCrv')
    mc.skinCluster('lf_upLeg_jnt', 'lf_loLeg_jnt', 'lf_ankle_jnt', 'L_leg_pathCrv')
    mc.skinCluster('rt_upLeg_jnt', 'rt_loLeg_jnt', 'rt_ankle_jnt', 'R_leg_pathCrv')
# def rigPlane() : 
#     'lf_upLeg_nrJnt'
#     mc.orientConstraint()
    
#     [u'L_arm_pathCrv', u'L_arm_profileCrv', u'R_arm_pathCrv', u'R_arm_profileCrv', u'L_leg_pathCrv', u'L_leg_profileCrv', u'R_leg_pathCrv', u'R_leg_profileCrv'] 

def armScale() : 
    # ctrl
    ctrls = {'lf_arm_ctrl': 'L_arm_profileCrv', 'rt_arm_ctrl': 'R_arm_profileCrv'}
    attrName = 'arm_volumn'

    for each in ctrls : 
        ctrl = each
        profileCurve = ctrls[each]

        if not mc.objExists('%s.%s' % (ctrl, attrName)) : 
            mc.addAttr(ctrl, ln = attrName, at = 'double', min = 1, dv = 10)
            mc.setAttr('%s.%s' % (ctrl, attrName), e = True, keyable = True)

        mdv = mc.createNode('multiplyDivide', n = '%s_mdv' % profileCurve)
        mc.setAttr('%s.input2Y' % mdv, 0.1)

        mc.connectAttr('%s.%s' % (ctrl, attrName), '%s.input1Y' % mdv, f = True)
        mc.connectAttr('%s.outputY' % mdv, '%s.scaleY' % profileCurve, f = True)



def armSleeve() : 
    nrs = {'lf_upArm_nrJnt': 'lf_armSleeve_jnt', 'rt_upArm_nrJnt': 'rt_armSleeve_jnt'}

    for each in nrs : 
        jnt = each
        jntName = nrs[each]
        joint = mc.createNode('joint', n = jntName)

        mc.delete(mc.parentConstraint(jnt, joint))
        mc.makeIdentity(joint, apply=True, t=1, r=1, s=1, n=0)

        mc.parent(joint, jnt)


def pelvisExtraJnt() : 
    pelvisJnt = 'cnt_pelvis_jnt'
    extraJnts = ['crotch_jnt', 'butt_jnt']

    for eachExtraJnt in extraJnts : 
        joint = mc.createNode('joint', n = eachExtraJnt)

        mc.delete(mc.parentConstraint(pelvisJnt, joint))
        mc.makeIdentity(joint, apply=True, t=1, r=1, s=1, n=0)

        mc.parent(joint, pelvisJnt)

