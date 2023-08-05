from __future__ import division
import time
import warnings
import numpy as np
from math import log
import numpy.ma as ma
from scipy.signal import convolve
from numpy.fft import rfft2,irfft2,fftshift

cimport cython
cimport numpy as np # gives-access-to-C-implementation-of-numpy 
DTYPEi = np.int32
DTYPEf = np.float64
ctypedef np.int32_t DTYPEi_t
ctypedef np.float64_t DTYPEf_t
@cython.wraparound(False) 
@cython.boundscheck(False) 

class CorrelationFunction( ):
    
    def __init__ (self, corr):
        self.data = corr
        self.shape = self.data.shape
        self.peak1, self.corr_max1 = self._find_peak(self.data)
    
    def _find_peak (self,array):
        # row/column-indices-of-the-heighest-peak
        ind = array.argmax()
        s = array.shape[1] 
        i = ind // s 
        j = ind %  s
        return (i,j),array.max()
        
    def _find_second_peak (self,width):
        # square-submatrix-the-first-correlation-peak: avoid-boundary-to-avoid-negative-indices
        tmp = self.data.view(ma.MaskedArray)
        iini = max(0, self.peak1[0]-width)
        ifin = min(self.peak1[0]+width+1, self.data.shape[0])
        jini = max(0, self.peak1[1]-width)
        jfin = min(self.peak1[1]+width+1, self.data.shape[1])
        tmp[ iini:ifin, jini:jfin ] = ma.masked
        peak, corr_max2 = self._find_peak( tmp )
        return peak, corr_max2  
            
    def subpixel_peak_position(self, method='gaussian'):
        # peak-and-its-neighbours: left->right->down->up
        try:
            c  = self.data[self.peak1[0],self.peak1[1]]
            cl = self.data[self.peak1[0]-1,self.peak1[1]]
            cr = self.data[self.peak1[0]+1,self.peak1[1]]
            cd = self.data[self.peak1[0],self.peak1[1]-1] 
            cu = self.data[self.peak1[0],self.peak1[1]+1]
        # peak-close-to-the-boundary: skip-subpixel-approximation
        except IndexError:
            return self.peak1
        # all-zero/few-NaN-skip: sub-pixel search
        tmp = np.array([c,cl,cr,cd,cu])
        if np.any(np.isnan(tmp)) or np.all (tmp == 0):
            return self.peak1
        # negative-correlation-near-the-peak: revert-to-centroid-approximation
        if np.any (tmp  < 0) and method == 'gaussian':
            method = 'centroid'
        # choose-method
        if method == 'centroid':
            subp_peak_position = (((self.peak1[0]-1)*cl+self.peak1[0]*c+(self.peak1[0]+1)*cr)/(cl+c+cr),((self.peak1[1]-1)*cd+self.peak1[1]*c+(self.peak1[1]+1)*cu)/(cd+c+cu))
        elif method == 'gaussian':
            subp_peak_position = (self.peak1[0] + ((np.log(cl)-np.log(cr) )/( 2*np.log(cl) - 4*np.log(c) + 2*np.log(cr))),self.peak1[1] + ((np.log(cd)-np.log(cu) )/( 2*np.log(cd) - 4*np.log(c) + 2*np.log(cu)))) 
        elif method == 'parabolic':
            subp_peak_position = (self.peak1[0] +  (cl-cr)/(2*cl-4*c+2*cr),self.peak1[1] +  (cd-cu)/(2*cd-4*c+2*cu)) 
        else:
            raise ValueError( "method not understood. Can be 'gaussian', 'centroid', 'parabolic'." )
        return subp_peak_position
        
    def sig2noise_ratio(self,method='peak2peak',width=2):
        # image-lacking-particles: zero -> since-no-signal
        if self.corr_max1 <  1e-3:
            return 0.0
        # first-peak-on-the-borders: zero -> since-no-signal
        if (0 in self.peak1 or self.data.shape[0] in self.peak1 or self.data.shape[1] in self.peak1):
            return 0.0
        # find-second-peak-height
        if method == 'peak2peak':
            peak2, corr_max2 = self._find_second_peak(width=width)
        # mean-of-the-correlation-map 
        elif method == 'peak2mean':
            corr_max2 = self.data.mean()
        else:
            raise ValueError('wrong sig2noise_method')
        # avoid-dividing-by-zero
        try:
            sig2noise = self.corr_max1/corr_max2
        except ValueError:
            sig2noise = np.inf    
        return sig2noise
    
def extended_search_area_piv(np.ndarray[DTYPEi_t, ndim=2] frame_a, 
                              np.ndarray[DTYPEi_t, ndim=2] frame_b,
                              int window_size,
                              int overlap=0,
                              float dt=1.0,
                              int search_area_size=0,
                              str subpixel_method='gaussian',
                              sig2noise_method=None,
                              int width=2,
                              nfftx=None,
                              nffty=None):
    # initial-parameter-ckecks
    if overlap >= window_size:
        raise ValueError('Overlap has to be smaller than the window_size')
    if search_area_size < window_size:
        raise ValueError('Search size cannot be smaller than the window_size')
    if (window_size > frame_a.shape[0]) or (window_size > frame_a.shape[1]):
        raise ValueError('window size cannot be larger than the image')
    # shape-of-the-resulting-flow-field
    cdef int n_cols, n_rows
    n_rows, n_cols = get_field_shape((frame_a.shape[0], frame_a.shape[1]), window_size, overlap)
    # define arrays
    cdef np.ndarray[DTYPEf_t, ndim=2] u = np.zeros([n_rows, n_cols], dtype=DTYPEf)
    cdef np.ndarray[DTYPEf_t, ndim=2] v = np.zeros([n_rows, n_cols], dtype=DTYPEf)
    cdef np.ndarray[DTYPEf_t, ndim=2] sig2noise = np.zeros([n_rows, n_cols], dtype=DTYPEf)
    cdef np.ndarray[DTYPEi_t, ndim=2] window_a = np.zeros([window_size, window_size], dtype=DTYPEi)
    cdef np.ndarray[DTYPEf_t, ndim=2] corr = np.zeros([search_area_size, search_area_size], dtype=DTYPEf)
    cdef np.ndarray[DTYPEi_t, ndim=2] search_area = np.zeros([search_area_size, search_area_size], dtype=DTYPEi)
    # cython-data-types
    cdef int i, j, k, l, I, J
    cdef float i_peak, j_peak
    # loop-over-the-interrogation-windows: starting-at-the-top-left-corner
    I = 0
    for i in range(0, frame_a.shape[0]-window_size+1, window_size-overlap):
        J = 0
        for j in range(0, frame_a.shape[1]-window_size+1, window_size-overlap):
            # interrogation-window-matrix-from: frame 1
            for k in range(window_size):
                for l in range( window_size ):
                    window_a[k,l] = frame_a[i+k, j+l]
            # search-area-on: frame b
            for k in range(search_area_size):
                for l in range(search_area_size):
                    # zero-padding-outside-boundary
                    if i+window_size/2-search_area_size//2+k < 0 or i+window_size//2-search_area_size//2+k >= frame_b.shape[0]:
                        search_area[k,l] = 0
                    elif j+window_size//2-search_area_size//2+l < 0 or j+window_size//2-search_area_size//2+l >= frame_b.shape[1]:
                        search_area[k,l] = 0
                    else:
                        search_area[k,l] = frame_b[ i+window_size//2-search_area_size//2+k,
                            j+window_size//2-search_area_size//2+l ]
            # compute-correlation-map 
            if any(window_a.flatten()):
                corr = correlate_windows(search_area, window_a, nfftx=nfftx, nffty=nffty)
                c = CorrelationFunction(corr)
                # subpixel-approximation-of-the-peak-center
                i_peak, j_peak = c.subpixel_peak_position( subpixel_method )
                # velocities
                v[I,J] = -((i_peak - corr.shape[0]/2) - (search_area_size-window_size)/2) / dt
                u[I,J] =  ((j_peak - corr.shape[0]/2) - (search_area_size-window_size)/2) / dt
                # signal-to-noise-ratio
                if sig2noise_method:
                    sig2noise[I,J] = c.sig2noise_ratio(sig2noise_method, width)
            else:
                v[I,J] = 0.0
                u[I,J] = 0.0
                # signal-to-noise-ratio
                if sig2noise_method:
                    sig2noise[I,J] = np.inf
            # next-vector
            J = J + 1
        # next-vector
        I = I + 1
    # apply-signal-to-noise-filter
    if sig2noise_method:
        return u, v, sig2noise
    else:
        return u, v

def get_field_shape (image_size, window_size, overlap):
    return ((image_size[0]-window_size)//(window_size-overlap)+1,(image_size[1] - window_size)//(window_size-overlap)+1)

def get_coordinates(image_size, window_size, overlap):
    # shape-of-the-flow-field
    field_shape = get_field_shape(image_size, window_size, overlap)
    # grid-coordinates-of-the-interrogation-window-centers
    x = np.arange(field_shape[1])*(window_size-overlap) + window_size/2.0
    y = np.arange(field_shape[0])*(window_size-overlap) + window_size/2.0
    return np.meshgrid(x,y[::-1])

def correlate_windows(window_a, window_b, corr_method = 'fft', nfftx = None, nffty = None):
    if corr_method == 'fft':
        if nfftx is None:
            nfftx = 2*window_a.shape[0]
        if nffty is None:
            nffty = 2*window_a.shape[1]
        return fftshift(irfft2(rfft2(normalize_intensity(window_a),s=(nfftx,nffty))*np.conj(rfft2(normalize_intensity(window_b),s=(nfftx,nffty)))).real, axes=(0,1))
    elif corr_method == 'direct':
        return convolve(normalize_intensity(window_a), normalize_intensity(window_b[::-1,::-1]), 'full')
    else:
        raise ValueError('method is not implemented')

def normalize_intensity(window):
    return window-window.mean()

def replace_nans(np.ndarray[DTYPEf_t, ndim=2] array, int max_iter, float tol, int kernel_size=2, str method='disk'):    
    cdef float n
    cdef int i, j, I, J, it, k, l
    cdef np.ndarray[DTYPEi_t, ndim=1] iter_seeds = np.zeros(max_iter, dtype=DTYPEi)
    cdef np.ndarray[DTYPEi_t, ndim=1] inans = np.empty([array.shape[0]*array.shape[1]], dtype=DTYPEi)
    cdef np.ndarray[DTYPEi_t, ndim=1] jnans = np.empty([array.shape[0]*array.shape[1]], dtype=DTYPEi)
    cdef np.ndarray[DTYPEf_t, ndim=2] kernel = np.empty((2*kernel_size+1, 2*kernel_size+1), dtype=DTYPEf) 
    # indices-with-NaN
    inans, jnans = [x.astype(DTYPEi) for x in np.nonzero(np.isnan(array))]
    n_nans = len(inans)
    cdef np.ndarray[DTYPEf_t, ndim=1] replaced_new = np.zeros( n_nans, dtype=DTYPEf)
    cdef np.ndarray[DTYPEf_t, ndim=1] replaced_old = np.zeros( n_nans, dtype=DTYPEf)
    if method == 'localmean':
        for i in range(2*kernel_size+1):
            for j in range(2*kernel_size+1):
                kernel[i,j] = 1.0
    elif method == 'disk':
        for i in range(2*kernel_size+1):
            for j in range(2*kernel_size+1):
                if ((kernel_size-i)**2 + (kernel_size-j)**2)**0.5 <= kernel_size:
                    kernel[i,j] = 1.0
                else:
                    kernel[i,j] = 0.0
    elif method == 'distance': 
        for i in range(2*kernel_size+1):
            for j in range(2*kernel_size+1):
                if ((kernel_size-i)**2 + (kernel_size-j)**2)**0.5 <= kernel_size:
                    kernel[i,j] = kernel[i,j] = -1*(((kernel_size-i)**2 + (kernel_size-j)**2)**0.5 - ((kernel_size)**2 + (kernel_size)**2)**0.5)
                else:
                    kernel[i,j] = 0.0
    else:
        raise ValueError( 'method not valid. Should be one of `localmean`, `disk` or `distance`.')
    # loop-over-max-iteration-number
    for it in range(max_iter):
        # loop-over-nans
        for k in range(n_nans):
            i = inans[k]
            j = jnans[k]
            # initialize -> 0
            replaced_new[k] = 0.0
            n = 0.0
            # loop-over-the-kernel
            for I in range(2*kernel_size+1):
                for J in range(2*kernel_size+1):
                    # within-the-boundary
                    if i+I-kernel_size < array.shape[0] and i+I-kernel_size >= 0:
                        if j+J-kernel_size < array.shape[1] and j+J-kernel_size >= 0:
                            # neighbour-element-not NaN
                            if not np.isnan(array[i+I-kernel_size, j+J-kernel_size]):
                                # only-non-zero-kerenels
                                if kernel[I, J] != 0:
                                    # convolve-with-kernel
                                    replaced_new[k] = replaced_new[k] + array[i+I-kernel_size, j+J-kernel_size]*kernel[I, J]
                                    n = n + kernel[I,J]
            # divide-by-effective-number-of-added-elements
            if n > 0:
                replaced_new[k] = replaced_new[k] / n
            else:
                replaced_new[k] = np.nan
        # replacement-by-new-values
        for k in range(n_nans):
            array[inans[k],jnans[k]] = replaced_new[k]
        # cut-off
        if np.mean((replaced_new-replaced_old)**2) < tol:
            break
        else:
            for l in range(n_nans):
                replaced_old[l] = replaced_new[l]
    return array
