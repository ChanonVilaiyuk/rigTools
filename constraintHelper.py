import maya.cmds as mc
from functools import partial

class run() : 
	def __init__(self) : 
		self.win = 'ConstraintHelperWin'


	def ui(self) : 
		if mc.window(self.win, exists = True) : 
			mc.deleteUI(self.win)
		mc.window('ConstraintHelperWin', t = 'Constraint Finder')
		mc.columnLayout(adj = 1, rs = 4)

		mc.frameLayout(borderStyle = 'etchedIn', l = 'Constraint List')
		mc.rowColumnLayout(nc = 3, cw = ([1, 150], [2, 150], [3, 150]), cs = ([2, 4], [3, 4]))

		mc.text(l = 'Object Lists')
		mc.text(l = 'Constraint Nodes')
		mc.text(l = 'Target Lists')

		mc.textScrollList('objTSL', numberOfRows = 12, sc = partial(self.listConstraintNodes))
		mc.textScrollList('constraintListTSL', numberOfRows = 12, sc = partial(self.listTargets))
		mc.textScrollList('targetListTSL', numberOfRows = 12)

		mc.setParent('..')
		mc.setParent('..')

		mc.columnLayout(adj = 1, rs = 2)

		mc.button(l = 'Add to List', h = 30, c = partial(self.loadConstraintObject))
		mc.button(l = 'Break Constraint', h = 30, c = partial(self.breakConstraint))
		mc.button(l = 'Restore Constraint', h = 30, c = partial(self.restoreConstraint))
		mc.button(l = 'Remove from List', h = 30, c = partial(self.clearData))

		mc.setParent('..')

		mc.showWindow()
		mc.window('ConstraintHelperWin', e = True, wh = [464, 361])

		self.initFunction()


	def initFunction(self) : 
		self.listUI()

	def loadConstraintObject(self, *args) : 
		info = dict()

		objs = mc.ls(sl = True)

		for each in objs : 

			# load all nodes
			nodes = mc.listRelatives(each)

			validNodes = dict()
			for eachNode in nodes : 

				# find node type
				nodeType = mc.objectType(eachNode)

				# if constraint node
				if 'Constraint' in nodeType : 	

					# find target
					cmd = 'mc.%s(eachNode, q = True, tl = True)' % nodeType
					targets = eval(cmd)

					tmpDict = {'targets': targets, 'nodeType': nodeType}

					validNodes[eachNode] = tmpDict

			info[each] = validNodes

		self.appendData(info)
		self.listUI()


	def appendData(self, data) : 
		value = mc.optionVar(q = 'TAConstraintLists')

		if value == 0 : 
			mc.optionVar(sv=('TAConstraintLists', '{}'))
			value = mc.optionVar(q = 'TAConstraintLists')

		currentData = eval(value)

		for each in data.keys() : 
			currentData[each] = data[each]

		writeData = str(currentData)

		mc.optionVar(sv=('TAConstraintLists', writeData))


	def clearData(self, *args) : 
		mc.optionVar(sv=('TAConstraintLists', '{}'))

		self.listUI()


	def listUI(self, *args) : 
		data = mc.optionVar(q = 'TAConstraintLists')
		self.info = eval(data) 

		mc.textScrollList('objTSL', e = True, ra = True)
		mc.textScrollList('constraintListTSL', e = True, ra = True)
		mc.textScrollList('targetListTSL', e = True, ra = True)

		for each in sorted(self.info.keys()) : 
			mc.textScrollList('objTSL', e = True, append = each)


	def listConstraintNodes(self, *args) : 
		selection = mc.textScrollList('objTSL', q = True, si = True)[0]
		extraText = 'X'

		mc.textScrollList('constraintListTSL', e = True, ra = True)
		mc.textScrollList('targetListTSL', e = True, ra = True)

		if selection in self.info.keys() : 

			listNodes = self.info[selection]

			for eachNode in listNodes : 
				if mc.objExists(eachNode) : 
					extraText = 'O'

				mc.textScrollList('constraintListTSL', e = True, append = '%s-%s' % (extraText, eachNode))


	def listTargets(self, *args) : 
		selObject = mc.textScrollList('objTSL', q = True, si = True)[0]
		selNode = mc.textScrollList('constraintListTSL', q = True, si = True)[0].split('-')[-1]

		mc.textScrollList('targetListTSL', e = True, ra = True)

		node = self.info[selObject]
		targets = node[selNode]['targets']

		for each in targets : 
			mc.textScrollList('targetListTSL', e = True, append = each)

	def breakConstraint(self, *args) : 
		selNode = mc.textScrollList('constraintListTSL', q = True, si = True)[0].split('-')[-1]

		mc.delete(selNode)
		self.listUI()

	def restoreConstraint(self, *args) : 
		selNode = mc.textScrollList('constraintListTSL', q = True, si = True)[0].split('-')[-1]
		selObj = mc.textScrollList('objTSL', q = True, si = True)[0]
		targets = mc.textScrollList('targetListTSL', q = True, ai = True)
		targetString = '"%s"' % ('","').join(targets)

		node = self.info[selObj]
		nodeType = node[selNode]['nodeType']

		cmd = 'mc.%s(%s, "%s", mo = True, n = "%s")' % (nodeType, targetString, selObj, selNode)
		print cmd

		if not mc.objExists(selNode) : 
			node = eval(cmd)

			self.listUI()

			return node