# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 10:03:08 2012

@author: merlin
"""

import pylab
import numpy as np

# ----------------------
# Define useful classes
# ----------------------

class Pos:
    def __init__(self, posx, posy):
        self.x = float(posx)
        self.y = float(posy)
        
    def normalize(self) :
        dist = np.sqrt(self.x**2 + self.y**2)
        self.x = self.x/dist;
        self.y = self.y/dist;

# Light temperature
class LightTemp :
    r = 1.
    g = 1.
    b = 1.
    # Define constructor
    def __init__(self, red, green, blue):
        self.b = blue
        self.g = green
        self.r = red

# Light source
class Light :
    # Define constructor
    def __init__(self, pos_x, pos_y, power, temp):
        self.position = Pos(pos_x, pos_y)
        self.power = power
        self.temperature = LightTemp(temp[0], temp[1], temp[2])
    
class Mirror : 
    # Define constructor:
    def __init__(self, start_x, start_y, stop_x, stop_y) :    
        self.pos_start = Pos(start_x, start_y)
        self.pos_stop  = Pos(stop_x, stop_y)
        
    # Mirror reference number (to recognize mirrored lights effects)
    reference = 0
    temperature = [1., 1., 1.] # tainted mirror
    
class MirrorLight(Light):
    # Define constructor:
    # A mirror-light is defined by a combination of a light and 
    # .. a mirror. Important because of window effect
    ref_mirror = 0

class Room :
    # Define constructor
    def __init__ (self, length, width) :
        self.luminance = np.zeros((length, width, 3))
        self.lights = [] # we will store the successive lights in there
        self.mirrors = []# we will store the successive mirrors in there
        self.mirroredLights = []
        self.size_x = length
        self.size_y = width
        self.light_map_updated = 0
        
    def resetLuminance(self) :
        self.luminance = np.zeros((self.size_x, self.size_y, 3))   
        print "Light map has been erased"

    # Compute illumination for every light in the room        
    def computeLighting(self) :
        for i in range(len(self.lights)) :
            light_curr = self.lights[i]
            
            for x in range(self.size_x):
                for y in range(self.size_y):
                    # Compute illumination value
                    cast_light = self.lightPoint(x,y, light_curr)
                    
                    # Increment light map
                    self.luminance[x,y,0] = self.luminance[x,y,0] + cast_light[0]
                    self.luminance[x,y,1] = self.luminance[x,y,1] + cast_light[1]
                    self.luminance[x,y,2] = self.luminance[x,y,2] + cast_light[2]
    
    # Compute illumination for the last light in the light_list       
    def computeLastLighting(self) :
        index = len(self.lights)-1
        
        for x in range(self.size_x):
            for y in range(self.size_y):
                # Compute illumination value
                cast_light = self.lightPoint(x,y, self.lights[index])
                
                # Increment light map
                for colour in range(3) :
                    self.luminance[x,y,colour] = self.luminance[x,y,colour] + cast_light[colour]
                
    def computeMirroredLighting(self) :
        for i in range(len(self.mirroredLights)) :
            light_curr = self.mirroredLights[i]

            print "Computing mirrored light {}".format(i)           
            
            for x in range(self.size_x):
                for y in range(self.size_y):
                    # Compute illumination value
                    cast_light = self.lightMirrorPoint(x,y, light_curr)
                    
                    # Increment light map
                    for colour in range(3) :
                        self.luminance[x,y,colour] = self.luminance[x,y,colour] + cast_light[colour]
            

    # Compute visible light at some point
    def lightPoint(self, x,y, light) :
        dist = np.sqrt(pow(float(x)-light.position.x, 2) + pow(float(y)-light.position.y, 2))
        dist = max(dist, 1.0) # threshold distance close to the lamp    
        
        # test if it is on the right side of every mirror :
        mirror_side = 1
        for i_m in range(len(self.mirrors)) :
            mirror = self.mirrors[i_m]
            norm_vec = Pos(mirror.pos_stop.y - mirror.pos_start.y, mirror.pos_start.x - mirror.pos_stop.x)        
            norm_vec.normalize()
    
            point2mirror = Pos(mirror.pos_start.x - x, mirror.pos_start.y - y)                
            
            side = point2mirror.x*norm_vec.x + point2mirror.y*norm_vec.y
            if (side > 0) : 
                mirror_side = 0
                i_m = len(self.mirrors)

        coloured_light = np.zeros(3)
        
        if (mirror_side >0 ) :                
            visible_light = np.divide(light.power, dist**2) 
            coloured_light = np.array((light.temperature.r, light.temperature.g, light.temperature.b))
            coloured_light = coloured_light * visible_light
        
        # Check that it is within the window of visibility : (no obstruction by a mirror)           
        elif (mirror_side == 0) :
            light2point = Pos(x - light.position.x, y - light.position.y)
            light2mirrA = Pos(mirror.pos_start.x - light.position.x, mirror.pos_start.y - light.position.y)
            light2mirrB = Pos(mirror.pos_stop.x - light.position.x,  mirror.pos_stop.y - light.position.y)
            
            sign = light2mirrA.y*light2point.x - light2mirrA.x*light2point.y
            sign = sign*(light2mirrB.y*light2point.x - light2mirrB.x*light2point.y)
            
            if (sign > 0):
                mirror_side = 0
                visible_light = np.divide(light.power, dist**2)
                coloured_light = np.array((light.temperature.r, light.temperature.g, light.temperature.b))
                coloured_light = coloured_light*visible_light
                    
        return coloured_light
        
        # TODO : test with every mirror, not just one !
        
    # Compute visible light at some point from a mirrored source
    def lightMirrorPoint(self, x,y, light) :        
        dist = np.sqrt(pow(float(x)-light.position.x, 2) + pow(float(y)-light.position.y, 2))
        dist = max(dist, 1.0) # threshold distance close to the lamp    
        visible_light = np.divide(light.power, dist**2) 
        coloured_light = np.array((light.temperature.r, light.temperature.g, light.temperature.b))
        coloured_light = coloured_light*visible_light # 3x1 computation

        mirror = self.mirrors[light.ref_mirror]
        # Taint the reflected colour
        for colour in range(3) :
            coloured_light[colour] = coloured_light[colour]*mirror.temperature[colour]
        
        # test if it is on the right side of the mirror :        
        norm_vec = Pos(mirror.pos_stop.y - mirror.pos_start.y, mirror.pos_start.x - mirror.pos_stop.x)        
        norm_vec.normalize()

        point2mirror = Pos(mirror.pos_start.x - x, mirror.pos_start.y - y)                
        
        # Only cast light if you're on the right side of the mirror
        mirror_side = point2mirror.x*norm_vec.x + point2mirror.y*norm_vec.y
        if (mirror_side < 0) : 
            mirror_side = 1
        else :
            mirror_side = 0
            
        # Check that it is within the window of visibility :            
        if (mirror_side == 1) :
            light2point = Pos(x - light.position.x, y - light.position.y)
            light2mirrA = Pos(mirror.pos_start.x - light.position.x, mirror.pos_start.y - light.position.y)
            light2mirrB = Pos(mirror.pos_stop.x - light.position.x,  mirror.pos_stop.y - light.position.y)
            
            sign = light2mirrA.y*light2point.x - light2mirrA.x*light2point.y
            sign = sign*(light2mirrB.y*light2point.x - light2mirrB.x*light2point.y)
            
            if (sign > 0):
                mirror_side = 0
                
        # TODO ! window based occlusion prior to checking side

                
        return mirror_side*coloured_light
        
    # Add a light in the room            
    def addLight(self, newLight) : 
        self.lights.append(newLight)
        print "New light added to the room"
        if len(self.lights) > 1 :
            print "{} lights in the room".format(len(self.lights))
        else :
            print "{} light in the room".format(len(self.lights))
            
        # Compute the new lighting values
        #self.computeLastLighting()
        #print "Lighting computed"
        
    # Add a mirror in the room
    def addMirror(self, newMirror) :
        # Append the new mirror to the list
        newMirror.reference = len(self.mirrors)
        self.mirrors.append(newMirror)
        
        # Update light sources : add virtual light sources behind mirrors
        for i in range(len(self.lights)) :
            self.mirrorLightSource(self.lights[i], newMirror)
        
        # Draw the mirror on the screen (lame method right now..)
        self.drawMirror(newMirror)
        
        # Compute lighting induced by the mirror
        self.resetLuminance()
        print "New mirror taken into account"
        
    def mirrorLightSource(self, light, mirror):
        ## Quick'n'dirty..
        # Compute mirror normal vector
        norm_vec = Pos(mirror.pos_stop.y - mirror.pos_start.y, mirror.pos_start.x - mirror.pos_stop.x)        
        norm_vec.normalize()

        light2mirror = Pos(mirror.pos_start.x - light.position.x, mirror.pos_start.y - light.position.y)                
        dist2mirror = light2mirror.x*norm_vec.x + light2mirror.y*norm_vec.y
        light_temp = [light.temperature.r, light.temperature.g, light.temperature.b]
        newLight = MirrorLight(light.position.x + 2*dist2mirror*norm_vec.x, light.position.y + 2*dist2mirror*norm_vec.y, light.power, light_temp)        

        newLight.ref_mirror = mirror.reference
        self.mirroredLights.append(newLight)
        
        # TODO  ! window effect through the mirror   
        # TODO  ! Bresenham ray-tracing algorithm
        
    def drawMirror(self, mirror) :
        # Get positions in "standard" order
        if( mirror.pos_start.x >  mirror.pos_stop.x) :
            start_x = mirror.pos_stop.x
            stop_x  = mirror.pos_start.x
            start_y = mirror.pos_stop.y
            stop_y  = mirror.pos_start.y
        else :
            start_x = mirror.pos_start.x
            stop_x  = mirror.pos_stop.x
            start_y = mirror.pos_start.y
            stop_y  = mirror.pos_stop.y
            
        # Exclude vertical case :
        if start_y == stop_y:
            x_current = start_x
            
            while x_current <= stop_x :
                self.luminance[x_current, stop_y,0] = 2000 # stupid draw to correct.. 
                x_current = x_current + 1
        
        else :
            slope = (stop_x - start_x)/float(stop_y - start_y)
            x_current = start_x
            y_current = start_y
            while x_current <= stop_x :
                self.luminance[x_current, y_current,0] = 2000 # stupid draw to correct.. 
                x_current = x_current + 1
                y_current = y_current + 1/slope 

    # Show the light in the room        
    def plotLight(self) :
        # Update luminance map
        self.computeLighting()
        self.computeMirroredLighting()        
        
        # Take the log
        for x in range(self.size_x) :
            for y in range(self.size_y) :
                for colour in range(3) :
                    self.luminance[x,y,colour] = max(self.luminance[x,y,colour], 1.0)
    
        self.luminance = np.log(self.luminance)        
        
        # Normalize   
        max_lum = 0.;                 
        for x in range(self.size_x):
            for y in range(self.size_y):
                max_lum = max(max_lum,self.luminance[x,y,0], self.luminance[x,y,1], self.luminance[x,y,2] )
        
        self.luminance = np.divide(self.luminance, max_lum)        
        
        # Show                
        pylab.imshow(self.luminance, interpolation='bilinear')
        pylab.show()

# ----------------------        
# Test script : 
# ----------------------
test_room = Room(200,200)
#test_room.addLight(Light(150., 100., 10000, [0.1, 1., 1.])) # ~light blue
test_room.addLight(Light(160., 15., 7000, [1., 0.1, 1.]))  # ~magenta
test_room.addLight(Light(130., 5., 7000, [1., 1., 1.]))  # ~white
test_room.addLight(Light(35., 90., 3000, [0., 0., 1.]))  # ~white
test_room.addMirror(Mirror(160, 0, 130, 0)) # White mirror

#mirror = Mirror(180, 20, 160, 0)
#mirror.temperature = [0.3, 0.7, 0]
#test_room.addMirror(mirror) # tainted mirror
test_room.plotLight()
