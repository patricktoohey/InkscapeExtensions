<?xml version="1.0" encoding="utf-8"?>
<!--
Copyright (c) 2013 Patrick Toohey

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
-->
<xsl:stylesheet version="1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:svg="http://www.w3.org/2000/svg"
  xmlns:msxsl="urn:schemas-microsoft-com:xslt" 
  xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" exclude-result-prefixes="msxsl svg">
  <xsl:output method="text" indent="yes"/>
  <xsl:template match="svg:svg">&lt;?xml version="1.0" encoding="utf-8"?>
&lt;xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:svg="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl">
  &lt;xsl:output method="xml" indent="yes"/>
  &lt;xsl:template match="@* | node()">
    &lt;xsl:copy>
      &lt;xsl:apply-templates select="@* | node()"/>
    &lt;/xsl:copy>
  &lt;/xsl:template>
    <xsl:apply-templates />
&lt;/xsl:stylesheet>
  </xsl:template>

  <xsl:template match="@* | node()">
    <xsl:apply-templates select="@* | node()"/>
  </xsl:template>

  <xsl:template match="@inkscape:label">
    &lt;xsl:template match="svg:g[@inkscape:label='<xsl:value-of select="." />']/@style">
      &lt;xsl:attribute name="style"><xsl:value-of select="../@style" />&lt;/xsl:attribute>
    &lt;/xsl:template>
  </xsl:template>
</xsl:stylesheet>
