import maya.cmds as mc

def writeWeight(srcObj, filePath) : 

    # sel = mc.ls(sl = True)
    # srcObj = sel[0]
    # targetObj = sel[1]

    infList = mc.skinCluster(srcObj, q = True, inf = True)
    skinInfo = dict()
    allInfo = {'infList': infList, 'skinInfo': skinInfo}

    nodes = mc.listHistory()
    skinCluster = str()

    for each in nodes : 
        if mc.objectType(each, isType = 'skinCluster') : 
            skinCluster = each

    if skinCluster : 

        for i in range(mc.polyEvaluate(srcObj, v = True)) : 
            vtx = '%s.vtx[%s]' % (srcObj, i)
            value = mc.skinPercent(skinCluster, vtx, q = True, value = True)
            skinValue = []
            for ii in range(len(value)) : 
                if value[ii] > 0.0 : 
                    data = (infList[ii], value[ii])
                    skinValue.append(data)
                    
            skinInfo[vtx] = skinValue
            

        allInfo = {'srcObj': srcObj, 'infList': infList, 'skinInfo': skinInfo}
        data = str(allInfo)

        result = writeFile(filePath, data)

        return result


def readWeight(targetObj, filePath) :    

    data = readFile(filePath)
    allInfo = eval(data)

    if allInfo : 
        srcObj = allInfo['srcObj']
        infList = allInfo['infList']
        skinInfo = allInfo['skinInfo']

        result = mc.skinCluster(infList, targetObj, inf = True)
        targetSkinCluster = result[0]
        
        for each in skinInfo : 
            skinValue = skinInfo[each]
            vtx = each.replace(srcObj, targetObj)
            mc.skinPercent(targetSkinCluster, vtx, transformValue = skinValue)


def writeFile(file, data) : 
    f = open(file, 'w')
    f.write(data)
    f.close()


def readFile(file) : 
    f = open(file, 'r')
    data = f.read()
    return data