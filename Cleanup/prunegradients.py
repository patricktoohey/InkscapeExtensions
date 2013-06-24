#!/usr/bin/env python 
'''
Copyright (C) 2013 Patrick Toohey

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''
import inkex, os, subprocess, shutil, re
from lxml import etree

def pruneFile(svgFile):
    document = etree.parse(svgFile)
    prune(document)

def pruneToFile(sourceFile, output):
    document = etree.parse(sourceFile)
    prune(document)
    document.write(output)

def prune(document):
    pathGradients = '/svg:svg/svg:defs/svg:linearGradient'
    pathGradientByParentId = '/svg:svg/svg:defs/svg:linearGradient[@xlink:href]'
    pathRectWithStyle = "//*[contains(@style, 'fill:url(#%s)')]"    
    gradients = document.xpath(pathGradients, namespaces=inkex.NSS)
    childGradients = document.xpath(pathGradientByParentId, namespaces=inkex.NSS)
    #print "Found %d linear gradient definitions" % len(gradients)
        
    layerMap = dict()
    
    for lg in gradients:
        attrib = lg.attrib
        layerName = attrib["id"]
        
        stops = lg.xpath("svg:stop", namespaces=inkex.NSS)
        numStops = len(stops)

        if (numStops > 0):
            if numStops not in layerMap:
                layerMap[numStops] = []
                #print "init %s stop family" % numStops         
            layerMap[numStops].append(lg)

    for i in layerMap.keys():
        #print "---------------------------------------------"
        #print "process %s stop family" % i
        matrix = buildLayerMatrix(layerMap[i])
        for pair in matrix:
            if (matchedPair(pair)):
                print ''
                attribA = pair[0].attrib
                attribB = pair[1].attrib
                
                #print attribA["id"], "and", attribB["id"], "are equal"

                childA = findChildGradient(childGradients, attribA)
                childB = findChildGradient(childGradients, attribB)

                if (childA is None):
                    #print "childA is null"
                    continue;
                if (childB is None):
                    #print "childB is null"
                    continue;

                #print "replace", childB, "with", childA
                attribChildA = childA.attrib
                attribChildB = childB.attrib
        
                attribChildB["{http://www.w3.org/1999/xlink}href"] = attribChildA["{http://www.w3.org/1999/xlink}href"]

                #print ''

def matchedPair(pair):    
    stopsA = pair[0].xpath("svg:stop", namespaces=inkex.NSS)
    stopsB = pair[1].xpath("svg:stop", namespaces=inkex.NSS)

    return stopsEqual(stopsA, stopsB)        

def findChildGradient(childGradients, parent):
    for child in childGradients:
        attribChild = child.attrib
        comparator = "#%s" % parent["id"]                    
        if (attribChild["{http://www.w3.org/1999/xlink}href"] == comparator):
            return child
    return None
       
def findChildGradientId(childGradients, parent):
    for child in childGradients:
        attribChild = child.attrib
        comparator = "#%s" % parent["id"]                    
        if (attribChild["{http://www.w3.org/1999/xlink}href"] == comparator):
            return attribChild["id"]
    return ""

def stopsEqual(stopsA, stopsB):
    for i in range(len(stopsA)):
        stopAttribA = stopsA[i].attrib
        stopAttribB = stopsB[i].attrib
        if stopAttribA["style"] != stopAttribB["style"]:
            return False;
        if stopAttribA["offset"] != stopAttribB["offset"]:
            return False;
                
    return True

def buildLayerMatrix(layers):
    layers.sort()
    layerMatrix=[]
    for context in layers:
        for layer in layers:
            if layer != context:
                appendExclusive(layerMatrix, context, layer)

    return layerMatrix

def appendExclusive(list, elementFirst, elementSecond):
    for element in list:
        if (element[0] == elementSecond) and (element[1] == elementFirst):
            return;

    list.append([elementFirst, elementSecond])

class PruneGradients(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)

    def effect(self):
        prune(self.document)    

#pruneToFile("Prototype.svg", "PrototypeOptimized.svg")
e = PruneGradients()
e.affect()