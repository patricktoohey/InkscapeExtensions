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
import inkex, os
from lxml import etree

class RestoreView(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('--project', action = 'store', type = 'string', dest = 'project', default='Default')		
        self.OptionParser.add_option('--name', action = 'store', type = 'string', dest = 'name', default='Default')		

    def effect(self):
        home = os.getenv("HOME") + "\\Views\\" + self.options.project
        view = home + '\\' + self.options.name + '.xslt'
        
        if os.path.exists(view):
            templates = etree.parse(view)
            transform = etree.XSLT(templates)
            self.document = transform(self.document)

if __name__ == '__main__':
    e = RestoreView()
    e.affect()