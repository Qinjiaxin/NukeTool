#-*-coding:utf-8 -*-
# !/usr/bin/env python
# Author: AlexLuze
# IDE: PyCharm
# CreateTime: 2018/12/6
#************************
import nuke
import re
import os

def firstWrite():
    rootFilePath = nuke.Root().name()
    upRootPath = os.path.abspath(os.path.join(rootFilePath, ".."))  # 'E:\\GF\\comp\\EP02\\shot050'
    splitPath = upRootPath.split('\\')  # ['E:', 'GF', 'comp', 'EP02', 'shot050']
    path = os.path.splitdrive(upRootPath)  # ('E:', '\\GF\\comp\\EP02\\shot050')
    rootPath = "D:" + path[1]
    rightUpRootPath = rootPath.replace('\\', '/')  # 'D:/GF/comp/EP02/shot050'
    movFileName = splitPath[-2] + '_' + splitPath[-1] + '.mov'
    movSavePath = rightUpRootPath + '/' + movFileName
    number = 0
    for node in nuke.allNodes():
        if node.Class() == 'OLMSmoother':
            if number == 0:
                upPath = 'chAll'
                fileName = 'chAll.%04d.png'
                fileUpPath = os.path.join(rootPath, upPath)
                rightUpPath = fileUpPath.replace('\\', '/')  # 'E:/GF/comp/EP02/shot050/chAll'
                if os.path.exists(rightUpPath) == False:
                    os.makedirs(rightUpPath)
                filePath = fileUpPath + "/" + fileName
                rightFilePath = filePath.replace('\\', '/')  # 'E:/GF/comp/EP02/shot050/chAll/chAll.%04d.png'
                print "rightFilePath:", rightFilePath
                print "rightUpPath:", rightUpPath
                print 'node:', node.name()
                parentNode = node.input(0)
                print "parentNode:", parentNode.name()
                writeNode = nuke.nodes.Write(inputs=[parentNode])
                writeNode['file'].setValue(rightFilePath)
                writeNode['file_type'].setValue('png')
                nuke.execute(writeNode)
                readNode = importPngSeqs(rightUpPath)
                node['disable'].setValue(0)
                node.setInput(0, readNode)
            
            if number != 0:
                upPath = 'chAll' + str(number)
                fileName = 'chAll' + str(number) + '.%04d.png'
                fileUpPath = os.path.join(rootPath, upPath)
                rightUpPath = fileUpPath.replace('\\', '/')  # 'E:/GF/comp/EP02/shot050/chAll1'
                if os.path.exists(rightUpPath) == False:
                    os.makedirs(rightUpPath)
                filePath = fileUpPath + "/" + fileName
                rightFilePath = filePath.replace('\\', '/')  # 'E:/GF/comp/EP02/shot050/chAll1/chAll1.%04d.png'
                
                print "rightFilePath1:", rightFilePath
                print "rightUpPath1:", rightUpPath
                
                print 'node1:', node.name()
                parentNode = node.input(0)
                print "parentNode1:", parentNode.name()
                writeNode = nuke.nodes.Write(inputs=[parentNode])
                writeNode['file'].setValue(rightFilePath)
                writeNode['file_type'].setValue('png')
                nuke.execute(writeNode)
                readNode = importPngSeqs(rightUpPath)
                node['disable'].setValue(0)
                node.setInput(0, readNode)

            number += 1
            lastWriteNode = nuke.toNode('Write1')
            print "movSavePath:", movSavePath
            lastWriteNode['file'].setValue(movSavePath)
            lastWriteNode['file_type'].setValue('mov')
            nuke.execute(lastWriteNode)


# 获取序列帧并创建Read节点读取文件夹
def importPngSeqs(imagesPath):
    imagesTypes = "png"
    rule = r'(.*?)(\d+)(\.(?:%s))' % imagesTypes
    pattern = re.compile(rule)
    nukeReadSeqs = []
    imagesBaseName = []
    for root, dirs, files in os.walk(imagesPath):
        imagesSeq = [x for x in files if x.split('.')[-1] in imagesTypes]
        if imagesSeq != []:
            imagesSeq.sort()
            for f in imagesSeq:
                print pattern.findall(f)
                if pattern.findall(f) == []:
                    # nuke.createNode("Read",inpanel=False)["file"].setValue(root+'/'+f)
                    nukeReadSeqs.append([root + '/' + f, 1, 1])
                elif pattern.findall(f)[0][0] not in imagesBaseName:
                    firstFrame = int(pattern.findall(f)[0][1])
                    imagesBaseName.append(pattern.findall(f)[0][0])
                    nukeReadSeqs.append([root + '/' + pattern.findall(f)[0][0] + '#' * len(pattern.findall(f)[0][1]) +
                                         pattern.findall(f)[0][2], firstFrame, firstFrame])
                else:
                    nukeReadSeqs[-1][2] += 1
    for readSeq in nukeReadSeqs:
        n = nuke.createNode("Read", inpanel=False)
        n["file"].setValue(readSeq[0])
        n["first"].setValue(readSeq[1])
        n["last"].setValue(readSeq[2])
    nuke.delete(nuke.thisNode())
    return n
























