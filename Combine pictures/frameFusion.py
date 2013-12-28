# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 15:17:59 2013

@author: benjamin lefaudeux

Class to combine different pictures on top of one another. 
"""

import cv2
import numpy as np


class frameFusion:
  n_fused_frames  = 0
  pict_size_x     = 0
  pict_size_y     = 0
  gamma           = 1.0 # The gamma curve parameter.. lower value lightens the picture
  
  n_max_corners   = 1000
  corners_q_level = 4    
  tracked_corners = False
    
  frame_acc       = np.float32(pict_size_x * pict_size_y)
  frame_acc_disp  = np.float32(pict_size_x * pict_size_y)
  frame_eq        = np.float32(pict_size_x * pict_size_y)
  frame_prev      = np.float32(pict_size_x * pict_size_y)
  corners         = np.float32(0)
  corners_next    = np.float32(0)
  
  # The constructor, on top of an initial frame  
  def __init__(self, frame_first, gamma = 1.0, motion_compensation = False):
    # Define settings
    self.n_fused_frames = 1
    self.gamma          = gamma    
    self.n_max_corners  = 400
    self.corners_q_level= 4    
    self.motion_comp    = motion_compensation
    
    # Allocate buffers
    self.frame_acc      = np.float32(frame_first)
    self.frame_acc_disp = np.float32(frame_first)
    self.frame_eq       = np.float32(frame_first)
    self.frame_prev     = frame_first    
    
    # Do the first accumulation
    cv2.equalizeHist(frame_first, self.frame_acc)
    cv2.normalize(self.frame_acc, self.frame_acc_disp, 0., 1., cv2.NORM_MINMAX) # just for the display stuf

  # Display lines representing tracks  
  # TODO: Make it "private" ?
  def drawVec(self, img, corners, corners_next):
    try:
      corn_xy = corners.reshape((-1, 2))
      corn_xy_next = corners_next.reshape((-1, 2))
      
      i = 0
      for x, y in corn_xy:
        cv2.line(img,(int(x),int(y)), (int(corn_xy_next[i,0]), int(corn_xy_next[i,1])), [0,0,255])         
        i = i + 1
        
    except ValueError:
      pass            
    
  # Function to add a new picture to the current pile
  def pileUp(self, new_frame):    
    cv2.equalizeHist(new_frame, self.frame_eq) # Kill black level before the accumulation
    
    # FIXME: No motion compensation here... TODO    
    
    if (self.motion_comp):
      self.compensateInterFrameMotion(new_frame)
    
    cv2.accumulate(new_frame, self.frame_acc)  #  Just add pixel values
    cv2.normalize(np.power(self.frame_acc, self.gamma), self.frame_acc_disp, 0., 1., cv2.NORM_MINMAX)    
    
    self.n_fused_frames = self.n_fused_frames + 1
    self.frame_prev     = new_frame    
    
    return self.n_fused_frames
    
  def compensateInterFrameMotion(self, new_frame):    
    # Measure and compensate for inter-frame motion:
    # - get points on both frames
    # -- we use Shi & Tomasi here, to be adapted ?
#    self.corners = cv2.goodFeaturesToTrack(self.frame_prev, self.n_max_corners, self.corners_q_level, 1.0)  
    self.corners = cv2.goodFeaturesToTrack(self.frame_prev, 50, .01, 50)
   
    # - track points
    [self.corners_next, status, err] = cv2.calcOpticalFlowPyrLK(self.frame_prev, new_frame, self.corners)  
  
    # - determine if a motion compensation is necessary  
    # TODO 
    # (RANSAC + Vote ?)
  
    # - compute the transformation from the tracked pattern
    # -- estimate the rigid transform
    transform = cv2.estimateRigidTransform(self.corners, self.corners_next, False)
      
    # -- see if this transform explains most of the displacements (thresholded..)  
    # TODO
  
    # - bring the second picture in the current referential
    pass
    
  def show(self):
    keep_going = False

    # Show the current combined picture
    print "Showing frame {}".format(self.n_fused_frames)
    
    cv2.namedWindow("frameFusion")
    cv2.imshow("frameFusion", self.frame_acc_disp)  
    cv2.resizeWindow('frameFusion', 800, 600)
    cv2.waitKey(5)

    # Show the initial picture
    cv2.namedWindow('Raw frame')        
    # - Show tracked features
    if self.motion_comp:
      self.drawVec(self.frame_prev,self.corners, self.corners_next)    

    cv2.imshow('Raw frame', self.frame_prev)
    cv2.resizeWindow('Raw frame', 800, 600)
    cv2.waitKey(5)
    
    while(1):
      # Escape quits    
      k = cv2.waitKey(33)
      if (k==27):
          keep_going = False
          cv2.destroyWindow('frameFusion')
          cv2.destroyWindow('Raw frame')
          break
          
      # Space continues
      elif (k==32):
        keep_going = True
        break
        
    return keep_going    
    
  