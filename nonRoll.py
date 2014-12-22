import maya.cmds as mc
import maya.mel as mm

# create non-roll joint for selected joint

def run() : 
	sels = mc.ls(sl = True)

	if len(sels) == 2 : 
		startJnt = sels[0]
		endJnt = sels[1]

		# create joint

		jnt1 = mc.createNode('joint')
		jnt2 = mc.createNode('joint')
		jnt1 = mc.rename(jnt1, startJnt.replace('_jnt', '_nrJnt'))
		jnt2 = mc.rename(jnt2, endJnt.replace('_jnt', '_nrJnt'))

		mc.delete(mc.parentConstraint(startJnt, jnt1))
		mc.delete(mc.parentConstraint(endJnt, jnt2))

		mc.makeIdentity(jnt1, apply=True, t = 1, r = 1, s = 1, n = 0)
		mc.makeIdentity(jnt2, apply=True, t = 1, r = 1, s = 1, n = 0)

		mc.parent(jnt2, jnt1)

		# create IK

		ik = mc.ikHandle(n = endJnt.replace('_jnt', '_nrIk'), sj = jnt1, ee = jnt2, sol = 'ikRPsolver')
		ikGrp = mc.group(em = True, n = ik[0].replace('_nrIk', '_nrIkGrp'))
		mc.parent(ik[0], ikGrp)

		mc.setAttr('%s.poleVectorZ' % ik[0], 0)
		mc.setAttr('%s.poleVectorX' % ik[0], 0)
		mc.setAttr('%s.poleVectorY' % ik[0], 0)

		# set nonRoll to startJnt and endJnt
		mc.pointConstraint(startJnt, jnt1)
		mc.pointConstraint(endJnt, ik[0])

		# put jnt in a group
		nrJntGrp = mc.group(em = True, n = startJnt.replace('_jnt', '_nrGrp'))
		mc.parent(jnt1, nrJntGrp)

		# ik group

		ikAllGrp = 'nonRollIk_grp'
		if not mc.objExists(ikAllGrp) : 
			ikAllGrp = mc.group(em = True, n = ikAllGrp)

		mc.parent(ikGrp, ikAllGrp)

		return jnt1, jnt2, ik, nrJntGrp, ikAllGrp


def runWithRig() : 
	# clear name
	allObjs = mc.ls()

	for each in allObjs : 
		if 'Char_' in each : 
			try : 
				newName = each.replace('Char_', '')
				mc.rename(each, newName)

			except : 
				pass


	allCtrlJntGrp = 'allJnt_grp'
	allIkGrp = 'allIK_grp'

	leftLeg = ['cnt_pelvis_jnt', 'lf_upLeg_jnt', 'lf_loLeg_jnt']
	rightLeg = ['cnt_pelvis_jnt', 'rt_upLeg_jnt', 'rt_loLeg_jnt']
	leftArm = ['lf_clavicle1_jnt', 'lf_upArm_jnt', 'lf_loArm_jnt']
	rightArm = ['rt_clavicle1_jnt', 'rt_upArm_jnt', 'rt_loArm_jnt']

	setupNonRoll = [leftLeg, rightLeg, leftArm, rightArm]

	for each in setupNonRoll : 
		mc.select(each[1], each[2])
		jnt1, jnt2, ik, nrJntGrp, ikAllGrp = run()
		mc.orientConstraint(each[0], jnt1)

		mc.parent(nrJntGrp, allCtrlJntGrp)
	
	mc.parent(ikAllGrp, allIkGrp)

	print 'Add nonroll'


def rigExtrudePlane() : 
	mc.select(cl = True)
	lf_leg = ['lf_upLeg_nrJnt', 'L_leg_profileCrv']
	rt_leg = ['rt_upLeg_nrJnt', 'R_leg_profileCrv']
	lf_arm = ['lf_upArm_nrJnt', 'L_arm_profileCrv']
	rt_arm = ['rt_upArm_nrJnt', 'R_arm_profileCrv']
	set1 = [lf_leg, rt_leg, lf_arm, rt_arm]

	for each in set1 : 
		# constraint nonRoll to profile curve
		mc.orientConstraint(each[0], each[1], mo = True)
		print each[0], each[1]

	mc.select(cl = True)

	naming1 = ['L_arm_pathCrv', 'L_arm_profileCrv', 'R_arm_pathCrv', 'R_arm_profileCrv']
	naming2 = ['L_leg_pathCrv', 'L_leg_profileCrv', 'R_leg_pathCrv', 'R_leg_profileCrv']
	mc.select(naming1, naming2)
	mm.eval('tazGrp;')
	mc.select(cl = True)

	grp = ['L_armProfileCrv_zGrp', 'R_armProfileCrv_zGrp', 'L_legProfileCrv_zGrp', 'R_legProfileCrv_zGrp']

	for each in grp : 
		mc.scaleConstraint('placement_ctrl', each)

	# mc.select(cl = True)
	# # bind skin
	# mc.skinCluster('lf_upArm_jnt', 'lf_loArm_jnt', 'lf_wrist_jnt', 'L_arm_pathCrv', tsb = True)
	# mc.skinCluster('lf_upArm_jnt', 'lf_loArm_jnt', 'lf_wrist_jnt', 'L_arm_pathCrv', tsb = True)
	# mc.skinCluster('rt_upLeg_jnt', 'rt_loLeg_jnt', 'rt_ankle_jnt', 'R_leg_pathCrv', tsb = True)
	# mc.skinCluster('rt_upArm_jnt', 'rt_loArm_jnt', 'rt_wrist_jnt', 'Larm_pathCrv', tsb = True)

			
	# print 'Done'