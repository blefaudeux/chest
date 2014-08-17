# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:18:07 2013

@author: benjamin lefaudeux
"""

import numpy as np
import pylab

pylab.rcParams.update({'font.size': 14})

# Generate gaussian curve
def generateGaussian(mean, std, x_range):
  y = np.zeros((np.size(x_range)))

  i = 0
  for x in x_range:
    y[i] = gaussian(mean, std, x)
    i += 1

  return y

# Simple gaussian function
def gaussian(mean, std, x):
#  return 1/(std*np.sqrt(2*np.pi))*np.exp(-1/2.* np.power((x-mean)/(std),2.))
  return np.exp(-1/2.* np.power((x-mean)/std,2.))

def generateRandomSamples(mean, std, n_samples):
  results = std * np.random.randn(n_samples) + mean
  return results

# Generate sigma points from gaussian parameters
def generateSigmaPoints( mean, cov):
  kappa = 2. # kappa = 3-dim
  sigma_points = np.zeros((3,3))
  std = np.sqrt(cov)

  sigma_points[0,0] = mean                                      # position
  sigma_points[0,1] = gaussian(mean, std, sigma_points[0,0])     # value on initial gaussian
  sigma_points[0,2] = kappa / (2 + kappa)                       # weight

  sigma_points[1,0] = mean - np.sqrt((2+kappa)*cov)
  sigma_points[1,1] = gaussian(mean, std, sigma_points[1,0])
  sigma_points[1,2] = 1 /(2*(2 + kappa))

  sigma_points[2,0] = mean + np.sqrt((2+kappa)*cov)
  sigma_points[2,1] = gaussian(mean, std, sigma_points[2,0])
  sigma_points[2,2] = 1 /(2*(2 + kappa))

  return sigma_points

def transform(x):
#  y = np.sqrt(np.abs(x))
#  y = np.power(x, 0.33)
  y = 0.05 * np.exp(x)

#  y = np.arctan(x)
  return y

def transformDeriv(x):
#  y = -1/(2*np.sqrt(np.abs(x)))
#  y = -1/(3*np.power(x, 0.66))
  y = 0.05 * np.exp(x)
#  y = 1
  return y

def transformSigmaPoints(sigma_points):
  sigma_points_transform = np.array(sigma_points)

  for i in range(np.size(sigma_points,0)):
    sigma_points_transform[i, 0] = transform(sigma_points[i,0])

  return sigma_points_transform

def transformEKF(mean, std):
  mean_t  = transform(mean)
  cov_t   = transformDeriv(mean) * std * std * transformDeriv(mean)
  return mean_t, np.sqrt(cov_t)

def getGaussianFromSigma(sigma_points):
  # Get weighted mean
  mean = np.average(sigma_points[:,0], 0, sigma_points[:,2])

  # Get weighted covariance
  cov = 0.0
  for point in sigma_points:
    cov += point[2]*np.power(point[0]-mean, 2)

  return mean, np.sqrt(cov)

# Generate the rendering
def plotGaussianAndSignaPoints(x_range, gaussian, sigma_points, means):
  # Get inputs
  gaussian_i    = gaussian[0]
  gaussian_t    = gaussian[1]
  gaussian_mc   = gaussian[2]
  gaussian_ekf  = gaussian[3]

  sigma_points_i = sigma_points[0]
  sigma_points_t = sigma_points[1]

  mean_ekf, mean_sigma, mean_mc = means

  fig = pylab.figure("Gaussian and sigma points")
  plot = fig.gca()

  # get the offset to plot in reverse
  rev_offset = np.min(x_range)

  # plot the gaussians
  plot.plot(x_range, gaussian_i, 'b-')
  plot.plot(gaussian_t, x_range + rev_offset,'g-.', label='Trans. Inodore')
  plot.plot(gaussian_mc[0],gaussian_mc[1][:-1] + rev_offset, 'g', label='Monte Carlo')
  plot.plot(gaussian_ekf,x_range + rev_offset,'g.', label=u'Linéarisation')

  # plot the sigma points
  plot.plot(sigma_points_i[:,0], sigma_points_i[:,1], 'bo')
  plot.plot(sigma_points_t[:,1] + np.min(x_range), sigma_points_t[:,0] + rev_offset, 'go')

  # plot the transformation
#  plot.plot(x_range, x_range + rev_offset, 'k-', linewidth = 0.5)
  plot.plot(x_range, transform(x_range) + rev_offset, 'k--', label='Fonction de transfert')

  # plot the mean values
  max_line = 2
  pylab.hlines(mean_ekf,0, max_line, colors = 'r', linestyles='dotted')
  pylab.hlines(mean_sigma,0, max_line, colors = 'r', linestyles='dashdot')
  pylab.hlines(mean_mc,0, max_line, colors = 'r', linestyles='solid')


  # set plot parameters
  pylab.xlim([np.min(x_range),np.max(x_range)])
  pylab.ylim([0,8])

  pylab.legend(loc = 'upper right')
  plot.set_aspect('equal')
  pylab.title(u'Différentes méthodes de propagation')
  pylab.grid(True, 'both', 'both')
  fig.show()

# Script to run all this stuff
def run():
  # define parameters
  peak = 1
  mean  = 3.5
  std   = 0.7
#  max_range = mean + 5 * std
#  min_range = np.abs(mean - 5 * std)
  range = np.arange(0, 7 + 0.1, 0.1)
  mc_samples = 1e7
  mc_bins = 3000

  #generate data
  gaussian = generateGaussian(mean, std, range)
  sigma_points = generateSigmaPoints(mean, std*std)
  sigma_points_transform = transformSigmaPoints(sigma_points)
  mc = generateRandomSamples(mean, std, mc_samples)
  mc_t = transform(mc)
  mc_t_h = np.histogram(mc_t, mc_bins, normed=True)
  mc_t_h[0][:] = mc_t_h[0] / np.max(mc_t_h[0])

  # get the gaussian from the sigma points
  mean_t, std_t     = getGaussianFromSigma(sigma_points_transform)
  gaussian_t        = generateGaussian(mean_t, std_t, range)
  mean_ekf, std_ekf = transformEKF(mean, std)
  mean_mc           = np.mean(mc_t)
  std_mc            = np.std(mc_t)
  gaussian_ekf      = generateGaussian(mean_ekf, std_ekf, range)


  print "Moments from linearized transform : \n{:.2f} mean, {:.2f} std\n".format(mean_ekf, std_ekf)
  print "Moments from sigma points : \n{:.2f} mean, {:.2f} std\n".format(mean_t, std_t)
  print "Moments from MC :  \n{:.2f} mean, {:.2f} std\n".format(mean_mc, std_mc)

  # plot the stuff
  plotGaussianAndSignaPoints(range,
                             [peak*gaussian, gaussian_t, mc_t_h, gaussian_ekf],
                             [peak*sigma_points, peak*sigma_points_transform], [mean_ekf, mean_t, mean_mc])

  return 1

# Execute !
run()

