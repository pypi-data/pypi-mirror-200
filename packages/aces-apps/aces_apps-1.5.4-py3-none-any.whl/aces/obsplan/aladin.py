'''
Tools to support the Aladin  GUI.


'''

__author__ = 'Keith Bannister <keith.bannister@csiro.au>'


class AladinFootprint(object):
    '''A hopeless hack at the Aladin footprint editor
    http://aladin.u-strasbg.fr/footprint_editor/#
    '''
    
    def __init__(self, footprint_name, telescope_name, instrument_name, instrument_description, origin):
        self._circles = []
        self._polygons = []
        self.footprint_name = footprint_name
        self.telescope_name = telescope_name
        self.instrument_name = instrument_name
        self.instrument_description = instrument_description
        self.origin = origin
        
    def add_circle(self, name, xpos, ypos, radius):
        """Add a circle with the given name, at the given offset positions and
        radius in arcsec
        """
        self._circles.append((name, xpos, ypos, radius))

    def add_polygon(self, name, xylist):
        '''Add a polygon with a given name. xylist should be a list of 2-tuples containing 
        (x, y) coordinates
        '''
        self._polygons.append((name, xylist))

    def add_square(self, name, width, height):
        w2 = width/2.
        h2 = height/2.
        self.add_polygon(name, ((w2, h2), (w2, -h2), (-w2, -h2), (-w2, h2)))
        
    def writeto(self, fileout):
        fout = open(fileout, 'w')
        fout.write(str(self))
        fout.close()
            
    def __str__(self):
        s = '''
        <?xml version="1.0" encoding="UTF-8"?>
<VOTABLE xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1" xmlns="http://www.ivoa.net/xml/VOTable/v1.1" xsi:schemaLocation="http://www.ivoa.net/xml/VOTable/v1.1 http://www.ivoa.net/xml/VOTable/v1.1">

<RESOURCE ID="{footprint_name}" utype="dal:footprint.geom">
    <PARAM datatype="char" arraysize="*" ID="TelescopeName" value="{telescope_name}" />
    <PARAM datatype="char" arraysize="*" ID="InstrumentName" value="{instrument_name}" />
    <PARAM datatype="char" arraysize="*" ID="InstrumentDescription" value="{instrument_description}" />
    <PARAM datatype="char" arraysize="*" ID="Origin" value="{origin}" />

    <PARAM datatype="char" arraysize="*" utype="stc:AstroCoordSystem.CoordFrame.CARTESIAN" name="reference frame" value="*"/>
    <PARAM name="projection" utype="stc:AstroCoordSystem.CoordFrame.Cart2DRefFrame.projection" datatype="char" arraysize="*" value="TAN"/>
    <PARAM name="Rollable" value="true"/>
        
        '''.format(**self.__dict__)

        for name, xylist in self._polygons:
            tbl = ''
            for x, y in xylist:
                tbl += '<TR><TD>{x}</TD><TD>{y}</TD></TR>'.format(x=x,y=y)
                
            sp = '''
            <RESOURCE ID="handles" name="handles">
            <TABLE utype="dal:footprint.geom.segment">
            <PARAM datatype="char" name="Shape" arraysize="*" value="Polygon" utype="dal:footprint.geom.segment.shape" />
            <FIELD unit="arcsec" datatype="double" name="xPtPosition" utype="stc:AstroCoordArea.Polygon.Vertex.Position.C1" />
            <FIELD unit="arcsec" datatype="double" name="yPtPosition" utype="stc:AstroCoordArea.Polygon.Vertex.Position.C2" />
            <DATA>
            <TABLEDATA>
            {tbl}
            </TABLEDATA>
            </DATA>
            </TABLE>
            </RESOURCE>
            '''.format(tbl=tbl)
            s += sp

        for name, xpos, ypos, radius in self._circles:
            cs = '''
            <RESOURCE ID="{name}" name="{name}">
    <TABLE utype="dal:footprint.geom.segment">
        <PARAM datatype="char" name="Shape" arraysize="*" value="Circle" utype="dal:footprint.geom.segment.shape" />
        <PARAM datatype="double" unit="arcsec" name="cxPtPosition" utype="stc:AstroCoordArea.Circle.Center.C1" value="{xpos}" />
        <PARAM datatype="double" unit="arcsec" name="cyPtPosition" utype="stc:AstroCoordArea.Circle.Center.C2" value="{ypos}" />
        <PARAM datatype="double" unit="arcsec" name="radius" utype="stc:AstroCoordArea.Circle.radius" value="{radius}" />
    </TABLE>
    </RESOURCE>
            '''.format(**locals())
            s += cs

        s += '''</RESOURCE>
        </VOTABLE>
        '''
    
        return s

