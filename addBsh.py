lfBrow = ['browUD', 'browIO', 'browTurn', 'browAngry', 'browSad']
lfBrowInfo = {
'browUD' : ['brow_lf_up_bsh', 'brow_lf_down_bsh'],
'browIO': ['brow_lf_in_bsh', 'brow_lf_out_bsh'],
'browTurn': ['brow_lf_turnF_bsh', 'brow_lf_turnL_bsh'],
'browAngry' : ['brow_lf_angry_bsh'],
'browSad' : ['brow_lf_sad_bsh']
}

rtBrow = ['browUD','browIO','browTurn','browAngry','browSad']
rtBrowInfo = {
'browUD': ['brow_rt_up_bsh', 'brow_rt_down_bsh'], 
'browIO': ['brow_rt_in_bsh', 'brow_rt_out_bsh'], 
'browTurn': ['brow_rt_turnF_bsh', 'brow_rt_turnL_bsh'], 
'browAngry': ['brow_rt_angry_bsh'], 
'browSad': ['brow_rt_sad_bsh']
}


lfEye = ['upLid','loLid','wink']
lfEyeInfo = {
'upLid' : ['eye_lf_upLidDn_bsh'],
'loLid' : ['eye_lf_loLidUp_bsh'],
'wink' : ['eye_lf_closeWink_bsh']
}

rtEye = ['upLid','loLid','wink']
rtEyeInfo = {
'upLid' : ['eye_rt_upLidDn_bsh'],
'loLid' : ['eye_rt_loLidUp_bsh'],
'wink' : ['eye_rt_closeWink_bsh']
}

mouth = ['a', 'e', 'o', 'u', 'mm', 'smile', 'smileOpen', 'sad', 'sadOpen', 'mUD', 'mIO', 'mTurn']
mouthInfo = {
'a': ['mouth_A_bsh'],
'e': ['mouth_E_bsh'],
'o': ['mouth_O_bsh'],
'u': ['mouth_U_bsh'],
'mm': ['mouth_M_bsh'],
'smile': ['mouth_smile_bsh'],
'smileOpen': ['mouth_smileOpen_bsh'],
'sad': ['mouth_sad_bsh'],
'sadOpen': ['mouth_sadOpen_bsh'],
'mUD': ['mouth_up_bsh', 'mouth_down_bsh'],
'mIO': ['mouth_in_bsh', 'mouth_out_bsh'],
'mTurn': ['mouth_turnF_bsh', 'mouth_turnL_bsh']
}

ctrls = {'mouth_ctrl': [mouth, mouthInfo], 'lf_brow_ctrl': [lfBrow, lfBrowInfo], 'rt_brow_ctrl': [rtBrow, rtBrowInfo], 'lf_eyeBl_ctrl': [lfEye, lfEyeInfo], 'rt_eyeBl_ctrl': [rtEye, rtEyeInfo]}
bshNode = 'bsh:blendShape1'

for ctrl in ctrls : 
	targetInfo = ctrls[ctrl][0]

	for each in targetInfo : 
		attrName = each
		min = 0
		max = 10
		dv = 0
		bshTarget = ctrls[ctrl][1][each]
		
		if len(bshTarget) > 1 : 
			min = -10

		mc.addAttr(ctrl, ln = attrName, at = 'double', min = min, max = max, dv = dv)
		mc.setAttr('%s.%s' % (ctrl, attrName), e = True, keyable = True)
		
		for i in range(len(bshTarget)) : 
			target = bshTarget[i]
			mdv = mc.createNode('multiplyDivide', n = target.replace('bsh', 'mdv'))
			mc.setAttr('%s.input2X' % mdv, 0.1)
			clmp = mc.createNode('clamp', n = target.replace('bsh', 'clmp'))
			mc.setAttr('%s.minR' % clmp, 0)
			mc.setAttr('%s.maxR' % clmp, 10)
			mc.connectAttr('%s.%s' % (ctrl, attrName), '%s.inputR' % clmp, f = True)
			mc.connectAttr('%s.outputR' % clmp, '%s.input1X' % mdv, f = True)
			mc.connectAttr('%s.outputX' % mdv, '%s.%s' % (bshNode, target), f = True)           
				
			if i == 1 : 
				mc.setAttr('%s.input2X' % mdv, -0.1)
				mc.setAttr('%s.minR' % clmp, -10)
				mc.setAttr('%s.maxR' % clmp, 0)
			
