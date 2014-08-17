import PythonKML as pykml
import os
mode = pykml.altitudeMode()
if os.path.exists("test.kml"):
    os.remove("test.kml")
kmlFile = pykml.kml("test.kml")
ls = pykml.LineString()
ls.Coordinates.append((0,0,00))
ls.Coordinates._coords = []
ls.Coordinates.append((0,0,100))
ls.Coordinates.append((5,5,50))
ls.Tessellate = True
ls.Extrude = True
ls.AltitudeMode = mode.clampToGround
pm = pykml.Placemark()
pm.setGeometry(ls)
pm.addToFolder("test")
pm.description = "Example of a line string"
la = pykml.LookAt()
ls.AltitudeMode = mode.absolute
ls.AltitudeMode = mode.clampToGround
la.AltitudeMode = mode.absolute
la.latitude = 2.5
la.longitude = 2.5
la.altitude = 50
la.tilt = 4
la.range = 50
la.heading = 45
pm.setView(la)
ls.Coordinates.append((10,10,100))
kmlFile.placemarks.append(pm)
pt = pykml.Point()
pt.latitude = 52
pt.longitude = 1.3
pt.altitude = 100.456
pt.AltitudeMode = mode.absolute
pm = pykml.Placemark()
pm.description = "Example of a point"
pm.setGeometry(pt)
kmlFile.placemarks.append(pm)
kmlFile.write()
















