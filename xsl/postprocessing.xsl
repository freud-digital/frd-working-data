<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="#all"
    version="2.0">
    
    <xsl:template match="node()|@*">
        <xsl:copy>
            <xsl:apply-templates select="node()|@*"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="tei:fw"/>
    
    <xsl:template match="tei:pb"/>
    
    <xsl:template match="tei:lb[@break='no']"/>
    
    <xsl:template match="tei:lb[not(@break)]"/>
    
    <xsl:template match="tei:lb[@break='paragraph']">
        <xsl:if test="following-sibling::*">
            <xsl:text> </xsl:text>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="tei:span[@class='inlinequote']">
        <quote xmlns="http://www.tei-c.org/ns/1.0" type="inlinequote"><xsl:apply-templates/></quote>
    </xsl:template>
    
</xsl:stylesheet>