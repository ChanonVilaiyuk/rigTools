import maya.cmds as mc
ctrl = 'hair_ctrl.lf_hair_1'

jnts = mc.ls(sl = True)
jnt1 = 'fkJnt'
jnt2 = 'dynJnt'

jnt1Set = []
jnt2Set = []
for each in jnts : 
    jnt1Name = each.replace('_jnt', jnt1)
    jntSet1 = mc.duplicate(each, n = jnt1Name)
    
    jnt2Name = each.replace('_jnt', jnt2)
    jntSet2 = mc.duplicate(each, n = jnt2Name)
    
    constraintNode = mc.orientConstraint(jntSet1, jntSet2, each)[0]
    # follow jnt2
    # jnt1 inverse
    
    reverseNode = mc.createNode('reverse', n = '%s_rsv' % each)
    mc.connectAttr(ctrl, '%s.inputX' % reverseNode, f = True)
    mc.connectAttr(ctrl, '%s.w1' % constraintNode, f = True)
    mc.connectAttr('%s.outputX' % reverseNode, '%s.w0' % constraintNode, f = True)
    
    jnt1Set.append(jntSet1)
    jnt2Set.append(jntSet2)
    
for i in range(1, len(jnts)) : 
    mc.parent(jnts[i], jnts[i-1])
    mc.parent(jnt1Set[i], jnt1Set[i-1])
    mc.parent(jnt2Set[i], jnt2Set[i-1])