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
import inkex, os, subprocess, shutil
from lxml import etree

class NewView(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('--project', action = 'store', type = 'string', dest = 'project', default='Default')		
        self.OptionParser.add_option('--name', action = 'store', type = 'string', dest = 'name', default='Default')		
        self.OptionParser.add_option('--screenshot', action = 'store', type = 'inkbool', dest = 'screenshot', default=False)

    def effect(self):
        home = os.getenv("HOME") + "\\Views\\" + self.options.project
        
        if not os.path.exists(home):
            os.mkdir(home)
        
        template = etree.parse('transformbuilder.xslt')
        transform = etree.XSLT(template)
        outputXml = transform(self.document)
        outputFile = home + "\\" + self.options.name
        outputXslt = outputFile + ".xslt"
        with open(outputXslt, 'w') as export:
            export.write(str(outputXml))

        if (self.options.screenshot) :
            outputTemp = outputFile + ".tmp"
            shutil.copy(self.svg_file, outputTemp)
            outputPng = outputFile + ".png"
            proc = subprocess.Popen(['inkscape', '-e', outputPng, outputTemp])
            proc.wait()
            os.remove(outputTemp)

if __name__ == '__main__':
    e = NewView()
    e.affect()
