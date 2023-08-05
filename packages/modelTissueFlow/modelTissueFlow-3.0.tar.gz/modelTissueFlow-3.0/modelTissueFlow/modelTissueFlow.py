import numpy
import itertools
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D 
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from modelTissueFlow.modules import PIV,inOutTools
from mpl_toolkits.axes_grid1 import make_axes_locatable

# color-list
colorsList = inOutTools.colors 
colorMaps = inOutTools.colorMaps

#======================================================================================================#
#                                           class: Animal1D                                            #
#======================================================================================================#
class Frame1D:
    
    #####################
    # initialize-animal #
    #####################
    def __init__(self,*args,**kwarg):  
        
        return
    
    ###############################
    # reference-frame-information #
    ###############################
    def reference_frame_information(self,dirPath,ref_frame,parametersFileName,epithelium_orientation,posterior_pole_location):
        parameters = inOutTools.read_parameter_file(parametersFileName) 
        ref_frame_raw_markers,_,_,frameDimension = self.extract_different_markers(ref_frame,int(parameters['reMarker_Number']),parameters['apical_marker_position_off_set'],parameters['basal_marker_position_off_set'],epithelium_orientation)   
        centre,embryo_principle_axes,ellipse_markers,_ = inOutTools.coordinate_frame_with_respect_to_polygon(ref_frame_raw_markers)
        frameDim_x,frameDim_y = frameDimension
        axis_scaleFactor = numpy.sum(frameDimension)
        embryo_principle_axes_major,embryo_principle_axes_minor = embryo_principle_axes
        image_frame_markers = numpy.array([[0,0],[frameDim_x,0],[frameDim_x,frameDim_y],[0,frameDim_y]])
        image_frame_line_segments = inOutTools.line_segments_along_polygon(image_frame_markers)
        x_ref_axis = None
        y_ref_axis = None
        reference_axis = None
        X_1,X_0 = embryo_principle_axes_major
        embryo_reference_axis_dir = inOutTools.normalize(X_1-X_0)
        for sign in [1,-1]:
            P0 = X_0 + sign*axis_scaleFactor*embryo_reference_axis_dir
            P = inOutTools.intersection_point_on_polygon_from_a_point(image_frame_line_segments,X_0,P0)
            X,Y = P-X_0
            embryo_orientation = inOutTools.point_at_which_quandrant(numpy.array([X,-Y])+1e-3)
            if embryo_orientation == posterior_pole_location:
                reference_axis = [P,X_0]
                c_x,c_y = X_0
                x_ref_axis = numpy.array([[frameDim_x,c_y],[0,c_y]])
                y_ref_axis = numpy.array([[c_x,frameDim_y],[c_x,0]])   
        if reference_axis is None: 
            inOutTools.error(True,inOutTools.get_linenumber(),'WARNING: readOutModule -> failed to detect the posterior pole !!!')
        # embryo-pole-markers: anterior/posterior   
        ref_frame_raw_markers,_ = inOutTools.reset_starting_point_of_polygon(ref_frame_raw_markers,reference_axis)
        ref_frame_raw_markers,_ = inOutTools.uniform_distribution_along_polygon(ref_frame_raw_markers,len(ref_frame_raw_markers),closed=True)
        ref_frame_raw_markers = numpy.roll(ref_frame_raw_markers,25,axis=0)
        curv = inOutTools.curvature_along_polygon(ref_frame_raw_markers,closed=True)
        curv = -1.0*curv if not inOutTools.Polygon(ref_frame_raw_markers).exterior.is_ccw else curv
        s,s_max = inOutTools.arc_length_along_polygon(ref_frame_raw_markers)
        anterior_ref_marker = ref_frame_raw_markers[0]   
        self.x_ref_axis = x_ref_axis
        self.y_ref_axis = y_ref_axis
        self.ellipse_fit_centre = centre
        self.frameDimension_ref = frameDimension
        self.ellipse_markers = ellipse_markers
        self.animal_reference_axis = reference_axis
        self.anterior_ref_marker = anterior_ref_marker
        self.animal_markers_ref = ref_frame_raw_markers
        self.epithelium_orientation = epithelium_orientation
        return 
    
    #################
    # analyze-frame #
    #################
    def analyze_FRAME(self,frameIndex,frame_MARKERS,frame_MYO,frame_MEM_PAIR,parametersFileName):
        print('frame(analyzing):',frameIndex)
        parameters = inOutTools.read_parameter_file(parametersFileName)
        # float-parameters
        time_between_frames = parameters['time_between_frames']
        # integer-parameters
        overlap = int(parameters['overlap'])
        reMarker_Number = int(parameters['reMarker_Number'])
        search_area_size = int(parameters['search_area_size'])
        layer_widths = [int(ele) for ele in parameters['layer_widths']]
        piv_interpol_window_size = int(parameters['piv_interpol_window_size'])
        bulk_piv_refMarker_Number = int(parameters['bulk_piv_refMarker_Number'])
        # float-parameters
        piv_cutOff = parameters['piv_cutOff']
        piv_interpol_depth = parameters['piv_interpol_depth']
        basal_marker_position_off_set = parameters['basal_marker_position_off_set']
        apical_marker_position_off_set = parameters['apical_marker_position_off_set']
        # bool-parameters
        myoMask = parameters['myoMask']
        bulk_PIV = parameters['bulk_PIV']
        midline_PIV = parameters['midline_PIV']
        background_subtraction = parameters['background_subtraction']
        equal_midline_to_apical_basal_distance = parameters['equal_midline_to_apical_basal_distance']
        # markers:apical/basal/midline 
        apical_markers_raw,basal_markers_raw,img_masks,frameDimension = self.extract_different_markers(frame_MARKERS,reMarker_Number,apical_marker_position_off_set,basal_marker_position_off_set,self.epithelium_orientation)
        apical_markers_ref,_ = inOutTools.reset_starting_point_of_polygon(apical_markers_raw,self.animal_reference_axis)
        # extract-RGB-values/PIV-referencing-of-image-frames 
        mem_frame,myo_frame,mem_frame_masked,myo_frame_masked,RGB_scale_myo_pair,piv_frame_pair = self.process_frames_and_markers(frame_MEM_PAIR,frame_MYO,frame_MARKERS,img_masks,background_subtraction)
        y_dim,x_dim = myo_frame.shape[:2]
        # spatial-orientation-of-animal 
        s,mid_markers,apical_markers,basal_markers = inOutTools.midline_polygon_from_a_pair_of_ploygons(apical_markers_raw,basal_markers_raw,start_point_intersetion_axis=self.animal_reference_axis,equal_apical_basal_distance=equal_midline_to_apical_basal_distance)
        # apical/basal-markers-and-masks 
        apical_markers,basal_markers,apical_polygon_Mask,basal_polygon_Mask,semi_apical_polygon_Mask,semi_basal_polygon_Mask = self.apical_basal_markers_and_masks_with_respect_to_midline(mid_markers,apical_markers_raw,basal_markers_raw,apical_markers,basal_markers,frameDimension,layer_widths)
        # process-piv 
        piv_tangent = None 
        piv_normal = None 
        # piv-raw 
        x,y,u,v,_ = self.extract_flow_field(inOutTools.copy_DATA(piv_frame_pair[0]),inOutTools.copy_DATA(piv_frame_pair[1]),piv_interpol_window_size,overlap,time_between_frames,search_area_size,'peak2peak',piv_cutOff)
        # piv-interpolation-markers
        normal_dir_outer,normDist_outer = inOutTools.nearest_distance_and_direction_to_one_polygon_from_another_polygon(mid_markers,apical_markers,direction='outer')
        normal_dir_inner,normDist_inner = inOutTools.nearest_distance_and_direction_to_one_polygon_from_another_polygon(mid_markers,basal_markers,direction='inner')
        sub_apical_markers = numpy.array([midPoint - piv_interpol_depth*normDist*norm for midPoint,norm,normDist in zip(mid_markers,normal_dir_outer,normDist_outer)])  
        sub_basal_markers = numpy.array([midPoint + piv_interpol_depth*normDist*norm for midPoint,norm,normDist in zip(mid_markers,normal_dir_inner,normDist_inner)])
        # piv-interpolation-at-mid-markers
        if midline_PIV: 
            piv_tangent,piv_normal,_ = inOutTools.split_vector_field_in_tangent_normal_components_along_polygon(x,y,u,v,[sub_apical_markers,mid_markers,sub_basal_markers],piv_interpol_window_size)
        # piv-interpolation-at-apical-markers
        else: 
            piv_tangent,piv_normal,_ = inOutTools.split_vector_field_in_tangent_normal_components_along_polygon(x,y,u,v,[sub_apical_markers],piv_interpol_window_size) 
        # piv-interpolation-at-bulk-markers 
        bulk_piv = numpy.copy(mid_markers)
        bulk_markers = numpy.zeros_like(mid_markers)
        if bulk_PIV:
            frame_center = 0.5*numpy.array(frameDimension)
            bulk_markers = inOutTools.points_within_pair_of_polygons(inOutTools.uniform_points_within_rectangle(frame_center,frame_center*0.9,bulk_piv_refMarker_Number)[::-1],polygon_out=apical_markers,polygon_in=basal_markers) 
            bulk_piv,_ = inOutTools.interpolate_vector_field_around_markers([bulk_markers],piv_interpol_window_size,x,y,u,v)
            bulk_piv = numpy.reshape(bulk_piv,(-1,2))
        # process-myosin-intensity 
        apical_myo_pixel_distributed,basal_myo_pixel_distributed = self.extract_MYOSIN_intensity_and_colorMap(apical_polygon_Mask,basal_polygon_Mask,semi_apical_polygon_Mask,semi_basal_polygon_Mask,frameDimension,RGB_scale_myo_pair,myoMask,apical_polygon_Mask,basal_polygon_Mask)
        # process-active-moment-incredients: apical-myosin,basal-myosin,cell-height 
        e_h,apical_myo,basal_myo = self.extract_activeMoment_ingredients(apical_myo_pixel_distributed,basal_myo_pixel_distributed,mid_markers,apical_markers,basal_markers) 
        # process-curvature 
        curv = inOutTools.curvature_along_polygon(mid_markers,closed=True)
        # update-animal-individual-frame-information 
        self.s = s
        self.e_h = e_h
        self.curv = curv
        self.ID = frameIndex
        self.mem_frame = mem_frame
        self.myo_frame = myo_frame
        self.basal_myo = basal_myo 
        self.apical_myo = apical_myo
        self.piv_normal = piv_normal
        self.frameIndex = frameIndex
        self.mid_markers = mid_markers
        self.bulk_markers = bulk_markers
        self.basal_markers = basal_markers
        self.frameDimension = [x_dim,y_dim]
        self.apical_markers = apical_markers
        self.mem_frame_masked = mem_frame_masked
        self.myo_frame_masked = myo_frame_masked
        self.basal_markers_raw = basal_markers_raw
        self.apical_markers_raw = apical_markers_raw
        self.basal_polygon_Mask = basal_polygon_Mask
        self.apical_polygon_Mask = apical_polygon_Mask
        self.basal_myo_pixel_distributed = basal_myo_pixel_distributed
        self.apical_myo_pixel_distributed = apical_myo_pixel_distributed
        # piv-bulk
        self.bulk_piv = bulk_piv
        self.bulk_pvec_mag = numpy.array([numpy.linalg.norm(v) for v in bulk_piv])
        self.bulk_piv_dir = numpy.array([inOutTools.normalize(v) for v in bulk_piv])
        # piv-tangent
        self.piv_tangent = piv_tangent
        self.pvec_tan_mag = numpy.absolute(piv_tangent)
        self.piv_tangent_dir = numpy.array(inOutTools.tangent_normals_along_polygon(mid_markers,closed=False)[0])
        
        return 
        
    ###################################
    # orient-anterior-posterior-frame #
    ###################################
    def orient_AnteriorPosterior_FRAME(self,crop_margin): 
        ellipse_markers = self.ellipse_markers
        animal_markers_ref = self.animal_markers_ref 
        apical_polygon_Mask,basal_polygon_Mask,mid_markers,bulk_markers,bulk_piv,apical_markers,apical_markers_raw,basal_markers,basal_markers_raw,myo_frame  = [self.apical_polygon_Mask,self.basal_polygon_Mask,self.mid_markers,self.bulk_markers,self.bulk_piv,self.apical_markers,self.apical_markers_raw,self.basal_markers,self.basal_markers_raw,self.myo_frame]
        # split-piv-to-end-points
        bulk_piv_dir_List  = numpy.reshape(bulk_piv,(-1,2))
        bulk_markers = numpy.reshape(bulk_markers,(-1,2))
        bulk_piv  = numpy.add(bulk_piv_dir_List,bulk_markers) 
        # ref-image/rotation-angle
        img_ref = inOutTools.copy_DATA(myo_frame )
        rotation_angle_List = inOutTools.angle_between(numpy.array(mid_markers[0]-numpy.mean(ellipse_markers,axis=0)),numpy.array([-1,0]))
        # rotate-image
        ellipse_markers,animal_markers_ref = [numpy.array(inOutTools.rotatePointsOnImage(myo_frame ,markers,rotation_angle=rotation_angle_List)) for markers in [ellipse_markers,animal_markers_ref]] 
        apical_polygon_Mask,basal_polygon_Mask = [numpy.array([numpy.array(inOutTools.rotatePointsOnImage(myo_frame ,mask,rotation_angle=rotation_angle_List),int) for mask in myo_maskType_List]) for myo_maskType_List in [apical_polygon_Mask,basal_polygon_Mask]]
        mid_markers,bulk_markers,bulk_piv,apical_markers,apical_markers_raw,basal_markers,basal_markers_raw = [numpy.array(inOutTools.rotatePointsOnImage(myo_frame ,markers_List,rotation_angle=rotation_angle_List)) for markers_List in [mid_markers,bulk_markers,bulk_piv,apical_markers,apical_markers_raw,basal_markers,basal_markers_raw]]
        myo_frame  = numpy.array(inOutTools.rotateImage(myo_frame ,rotation_angle=rotation_angle_List))
        # flip-image
        img_ref = inOutTools.copy_DATA(myo_frame )
        mid_markers_ref = inOutTools.copy_DATA(mid_markers)
        flipMode = 'H' if not inOutTools.Polygon(mid_markers_ref).exterior.is_ccw else None
        ellipse_markers,animal_markers_ref = [numpy.array(inOutTools.flipPointsOnImage(img_ref,markers,flipMode=flipMode)) for markers in [ellipse_markers,animal_markers_ref]] 
        apical_polygon_Mask,basal_polygon_Mask = [numpy.array([numpy.array(inOutTools.flipPointsOnImage(img_ref,mask,flipMode=flipMode),int) for mask in myo_maskType_List]) for myo_maskType_List in [apical_polygon_Mask,basal_polygon_Mask]]
        mid_markers,bulk_markers,bulk_piv,apical_markers,apical_markers_raw,basal_markers,basal_markers_raw = [numpy.array(inOutTools.flipPointsOnImage(img_ref,markers_List,flipMode=flipMode)) for markers_List in [mid_markers,bulk_markers,bulk_piv,apical_markers,apical_markers_raw,basal_markers,basal_markers_raw]]
        myo_frame  = numpy.array(inOutTools.flipImage(myo_frame ,flipMode=flipMode))
        # crop-image
        img_ref = inOutTools.copy_DATA(myo_frame )
        height,width,_ = img_ref.shape
        mid_markers_ref = inOutTools.copy_DATA(mid_markers)
        P_markers_ref = numpy.array(inOutTools.copy_DATA(mid_markers_ref[0]),int)
        D_markers_ref = numpy.array(inOutTools.copy_DATA(mid_markers_ref[25]),int)
        A_markers_ref = numpy.array(inOutTools.copy_DATA(mid_markers_ref[50]),int)
        V_markers_ref = numpy.array(inOutTools.copy_DATA(mid_markers_ref[75]),int)
        crop_xL,crop_xR = [P_markers_ref[0]-crop_margin,-(width-A_markers_ref[0]-crop_margin)]
        crop_yT,crop_yB = [D_markers_ref[1]-crop_margin,-(height-V_markers_ref[1]-crop_margin)]
        ellipse_markers,animal_markers_ref = [numpy.array(markers) - numpy.array([crop_xL,crop_yT]) for markers in [ellipse_markers,animal_markers_ref]]
        apical_polygon_Mask,basal_polygon_Mask = [numpy.array([numpy.array(mask)-numpy.array([crop_xL,crop_yT]) for mask in myo_maskType_List]) for myo_maskType_List in [apical_polygon_Mask,basal_polygon_Mask]] 
        mid_markers,bulk_markers,bulk_piv,apical_markers,apical_markers_raw,basal_markers,basal_markers_raw  = [numpy.array(numpy.array(markers_List) - numpy.array([crop_xL,crop_yT])) for markers_List in [mid_markers,bulk_markers,bulk_piv,apical_markers,apical_markers_raw,basal_markers,basal_markers_raw]]
        myo_frame  = numpy.array(myo_frame [crop_yT:crop_yB,crop_xL:crop_xR])
        y_dim,x_dim = myo_frame .shape[:2]
        # construct-piv-from-end-points
        bulk_piv = numpy.subtract(bulk_piv,bulk_markers)
        self.ellipse_markers,self.animal_markers_ref = [ellipse_markers,animal_markers_ref]
        self.piv_tangent_dir = numpy.reshape([t_dir*vec for t_dir,vec in zip(inOutTools.tangent_normals_along_polygon(mid_markers,closed=False)[0],self.piv_tangent)],(-1,2))
        self.apical_polygon_Mask,self.basal_polygon_Mask,self.mid_markers,self.bulk_markers,self.bulk_piv,self.apical_markers,self.apical_markers_raw,self.basal_markers,self.basal_markers_raw,self.myo_frame = [apical_polygon_Mask,basal_polygon_Mask,mid_markers,bulk_markers,bulk_piv,apical_markers,apical_markers_raw,basal_markers,basal_markers_raw,myo_frame ]
        self.frameDimension = [x_dim,y_dim]
 
        return
    
    ###################
    # visualize-frame #
    ###################
    def view_FRAME(self,outputPath,parametersFileName,pixel_to_micron_conversion_factor,figFormat,limits=[]):
        FRAME = inOutTools.copy_DATA(self)
        print('frame(visualizing):',FRAME.ID)
        # load-parameters
        parameters = inOutTools.read_parameter_file(parametersFileName)
        piv_tan_mag_lim,bulk_piv_mag_lim,all_myo_colorMap_lim,basal_myo_colorMap_lim,apical_myo_colorMap_lim = limits if limits else [[] for _ in range(5)]
        ####################
        # loop-over-frames #
        ####################
        # orient-animal 
        if parameters['orient_anterior_posterior']:
            FRAME.orient_AnteriorPosterior_FRAME(int(parameters['crop_margin']))
        # extract-myo-color-map  
        apical_myo_colorMap,basal_myo_colorMap,all_myo_colorMap = FRAME.extract_intensityColorMap(FRAME.apical_myo_pixel_distributed,FRAME.basal_myo_pixel_distributed,FRAME.apical_polygon_Mask,FRAME.basal_polygon_Mask,FRAME.frameDimension)
        # epithelium: full/posterior ? 
        truncate_data = [FRAME.mid_markers,FRAME.bulk_markers,FRAME.apical_markers,FRAME.apical_markers_raw,FRAME.basal_markers,FRAME.basal_markers_raw,FRAME.myo_frame,FRAME.piv_tangent,FRAME.piv_tangent_dir,FRAME.pvec_tan_mag,FRAME.bulk_piv_dir,FRAME.bulk_pvec_mag,FRAME.apical_polygon_Mask,FRAME.basal_polygon_Mask,apical_myo_colorMap,basal_myo_colorMap,all_myo_colorMap]
        mid_markers,bulk_markers,apical_markers,apical_markers_raw,basal_markers,basal_markers_raw,myo_frame,piv_tan_sig,piv_tan_dir,pvec_tan_mag,bulk_piv_dir,bulk_pvec_mag,apical_myo_Mask,basal_myo_Mask,apical_myo_colorMap,basal_myo_colorMap,all_myo_colorMap = [inOutTools.truncate_Data_Range(item,FRAME.posterior_domain) if parameters['view_posterior_domain'] else item for item in truncate_data] 
        # unit-conversion
        piv_tan_sig,pvec_tan_mag,bulk_pvec_mag = [numpy.array(ele)*pixel_to_micron_conversion_factor for ele in [piv_tan_sig,pvec_tan_mag,bulk_pvec_mag]]
        apical_myo_colorMap,basal_myo_colorMap,all_myo_colorMap = [numpy.array(ele)/pixel_to_micron_conversion_factor for ele in [apical_myo_colorMap,basal_myo_colorMap,all_myo_colorMap]]
        # myo-frame 
        myo_frame = inOutTools.adjustBrightnessImage(numpy.copy(myo_frame),brightNessParam=int(parameters['brightNess']))       
        # ellipse-reference
        ellipse_center = numpy.mean(FRAME.ellipse_markers,axis=0)
        ####################
        # reference-frames #
        ####################
        if parameters['view_reference_frames']:
            FIG, (AB_ax,Edge_ax) = plt.subplots(2, 1, figsize = (5,4))
            # map-markers/ellipse-on-frame 
            for axis in [AB_ax,Edge_ax]:
                axis.imshow(myo_frame[:,:,0], interpolation = 'nearest', cmap = 'gray_r', origin = 'upper') if parameters['invert_RGB'] else axis.imshow(myo_frame, interpolation = 'nearest', cmap = 'gray', origin = 'upper')
            ellipse_ref_line = inOutTools.open_to_closed_polygon(FRAME.ellipse_markers)
            AB_ax.plot(ellipse_ref_line[:,0],ellipse_ref_line[:,1], c = 'b', lw = 0.5) 
            # map-lateral-edge-position-on-frame 
            apical_line = inOutTools.open_to_closed_polygon(apical_markers_raw)
            basal_line = inOutTools.open_to_closed_polygon(basal_markers_raw)
            Edge_ax.plot(apical_line[:,0],apical_line[:,1], c = 'r', ls = '--', lw = 0.5)
            Edge_ax.plot(basal_line[:,0],basal_line[:,1], c = 'b', ls = '--', lw = 0.5)
            for marker_type_counter,(m,a,b) in enumerate(zip(mid_markers[:],apical_markers[:],basal_markers[:])):
                Edge_ax.scatter(a[0],a[1], c = colorsList[marker_type_counter], marker = 'o', s = 0.1)
                Edge_ax.scatter(m[0],m[1], c = colorsList[marker_type_counter], marker = 'o', s = 0.1)
                Edge_ax.scatter(b[0],b[1], c = colorsList[marker_type_counter], marker = 'o', s = 0.1)
                Edge_ax.add_line(Line2D([a[0],m[0]],[a[1],m[1]], c = colorsList[marker_type_counter], lw = 0.5))
                Edge_ax.add_line(Line2D([m[0],b[0]],[m[1],b[1]], c = colorsList[marker_type_counter], lw = 0.5))
            # reference-origin/orientation
            mid_markers_orientation_patch = mid_markers[0:5]
            for axis_counter,axis in enumerate([AB_ax,Edge_ax]):    
                axis.plot([mid_markers[0][0],ellipse_center[0]],[mid_markers[0][1],ellipse_center[1]], c = 'r', ls = '-', lw = 0.5) 
                axis.plot(mid_markers_orientation_patch[:,0],mid_markers_orientation_patch[:,1], c = 'c', ls = '--', lw = 0.5) 
            AB_ax.axis('off')
            Edge_ax.axis('off') 
            figName = outputPath + '/Fig_readOut_' + str(FRAME.frameIndex) + '.' + figFormat
            inOutTools.deleteFile(figName)
            FIG.savefig(figName,format = figFormat, figsize=(10, 3), dpi = 500, bbox_inches='tight', pad_inches=0.01)
            plt.close(FIG)       
        #########################
        # myo-masks/mid-markers #
        #########################
        if parameters['view_myo_masks']:   
            FIG,mask_ax = plt.subplots(1,1,figsize = (8,4))
            mask_ax.imshow(myo_frame[:,:,0], interpolation = 'nearest', cmap = 'gray_r', origin = 'upper') if parameters['invert_RGB'] else mask_ax.imshow(myo_frame, interpolation = 'nearest', cmap = 'gray', origin = 'upper')
            # myo-masks: apical/basal 
            for maskType in [apical_myo_Mask,basal_myo_Mask]:
                mask_ax.add_collection(PatchCollection([Polygon(polygon,True) for polygon in maskType] , facecolors = 'w', edgecolors = 'k',linewidths= 0.5)) 
            # mid-markers-and-lateral-edges 
            for indx,(a,m,b) in enumerate(zip(apical_markers,mid_markers,basal_markers)):
                # mid-markers 
                m_x,m_y = m
                mask_ax.scatter(m_x,m_y, c = 'g', marker = 'o',s = 2.0, zorder = 2)
                # lateral-edges 
                a_x,a_y = a
                b_x,b_y = b
                mask_ax.add_line(Line2D([a_x,m_x,b_x],[a_y,m_y,b_y], c = 'w', lw = 0.5,zorder=1))
            mask_ax.axis('off')
            figName = outputPath + '/FIG_midline_ref_' + str(FRAME.frameIndex) + '.' +  figFormat
            inOutTools.deleteFile(figName)
            FIG.savefig(figName,format = figFormat, figsize=(10, 3),dpi=500, bbox_inches='tight', pad_inches=0.01)
            plt.close(FIG)       
        #############################
        # piv/myo-map-oriented-color #
        ##############################
        if parameters['view_piv_oriented_color']:
            FIG,img_piv_tan_myo_axis = plt.subplots(1,1,figsize = (8,4)) 
            # piv-tangent-map 
            img_piv_tan_myo_axis.imshow(myo_frame[:,:,0], interpolation = 'nearest', cmap = 'gray_r', origin = 'upper') if parameters['invert_RGB'] else img_piv_tan_myo_axis.imshow(myo_frame, interpolation = 'nearest', cmap = 'gray', origin = 'upper')
            piv_color = ['y' if piv <= 0 else 'r' for piv in piv_tan_sig]
            if not numpy.all((pvec_tan_mag == 0)): 
                img_piv_tan_myo_axis.quiver(mid_markers[:,0],mid_markers[:,1], piv_tan_dir[:,0], piv_tan_dir[:,1],color = piv_color,angles ='xy',scale = parameters['piv_scale_factor'], width = 0.003,zorder=2) # cmap : inOutTools.transparent_cmap(plt.get_cmap('rainbow'))
            img_piv_tan_myo_axis.axis('off')
            # save-figure 
            figName = outputPath + '/FIG_piv_oriented_' + str(FRAME.frameIndex) + '.' + figFormat
            inOutTools.deleteFile(figName)
            FIG.savefig(figName,figsize=(10, 3), format = figFormat, dpi = 500, bbox_inches='tight', pad_inches=0.01)
            plt.close(FIG)       
        ################
        # bulk-piv-map #
        ################
        if parameters['view_bulk_piv']:
            FIG,img_piv_tan_myo_axis = plt.subplots(1,1,figsize = (8,4))
            # piv-tangent-map 
            img_piv_tan_myo_axis.imshow(myo_frame[:,:,0], interpolation = 'nearest', cmap = 'gray_r', origin = 'upper') if parameters['invert_RGB'] else img_piv_tan_myo_axis.imshow(myo_frame, interpolation = 'nearest', cmap = 'gray', origin = 'upper')
            divider = make_axes_locatable(img_piv_tan_myo_axis)
            if not numpy.all((bulk_pvec_mag == 0)): 
                cax_piv_tan = divider.append_axes("left", size="5%", pad=0.05)
                img = img_piv_tan_myo_axis.quiver(bulk_markers[:,0],bulk_markers[:,1],bulk_piv_dir[:,0],bulk_piv_dir[:,1],bulk_pvec_mag,angles ='xy',cmap = 'nipy_spectral',scale = 0.5*parameters['piv_scale_factor'], width = 0.003,zorder=2) # cmap : inOutTools.transparent_cmap(plt.get_cmap('rainbow'))
                if bulk_piv_mag_lim:img.set_clim(bulk_piv_mag_lim[0],bulk_piv_mag_lim[-1])  
                FIG.colorbar(img, ax = img_piv_tan_myo_axis, cax = cax_piv_tan)
                cax_piv_tan.yaxis.set_ticks_position("left")
            #cax_piv_tan.tick_params(labelsize=20) 
            img_piv_tan_myo_axis.tick_params(axis='both', which='major', labelsize=18)
            img_piv_tan_myo_axis.axis('off')
            # save-figure 
            figName = outputPath + '/FIG_bulk_piv_' + str(FRAME.frameIndex) + '.' + figFormat
            inOutTools.deleteFile(figName)
            FIG.savefig(figName,figsize=(10, 3), format = figFormat, dpi = 500, bbox_inches='tight', pad_inches=0.01)
            plt.close(FIG)      
        ########################
        # piv/myo-map-together #
        ########################
        if parameters['view_piv_myo_together']:
            FIG,img_piv_tan_myo_axis = plt.subplots(1,1,figsize = (8,4))
            # piv-tangent-map 
            img_piv_tan_myo_axis.imshow(myo_frame[:,:,0], interpolation = 'nearest', cmap = 'gray_r', origin = 'upper') if parameters['invert_RGB'] else img_piv_tan_myo_axis.imshow(myo_frame, interpolation = 'nearest', cmap = 'gray', origin = 'upper')
            #inOutTools.create_vector_heatMap(fig=FIG,ax=img_piv_tan_myo_axis,vectorMag=pvec_tan_mag,vectorBase=mid_markers,vectorDir=piv_tan_dir,vectorSign=piv_tan_sig,angles='xy',scaleFactor=parameters['piv_scale_factor'],colorMap='nipy_spectral',widthFactor=0.003,vector_mag_lim=piv_tan_mag_lim,labelSize=10)
            img_piv_tan_myo_axis.tick_params(axis='both', which='major', labelsize=18)
            img_piv_tan_myo_axis.axis('off')
            # apical/basal-myosin-map 
            inOutTools.create_scalar_heatMap(fig=FIG,ax=img_piv_tan_myo_axis,scalarMag=all_myo_colorMap,colorMap=inOutTools.transparent_cmap(plt.get_cmap('rainbow')),scalar_mag_lim=all_myo_colorMap_lim,labelSize=20)
            img_piv_tan_myo_axis.tick_params(axis='both', which='major', labelsize=18)
            img_piv_tan_myo_axis.axis('off')
            # save-figure 
            figName = outputPath + '/FIG_piv_myo_tog_' + str(FRAME.frameIndex) + '.' + figFormat
            inOutTools.deleteFile(figName)
            FIG.savefig(figName,figsize=(10, 3), format = figFormat, dpi = 500, bbox_inches='tight', pad_inches=0.01)
            plt.close(FIG)       
        ###############################
        # piv/myo-map-seperate-panels #
        ###############################
        if parameters['view_piv_myo_separately']:
            FIG,(imgPIVtan_ax,img_apical_myo_ax,img_basal_myo_ax) = plt.subplots(3,1,figsize = (8,12))
            # piv-tangent-map 
            imgPIVtan_ax.imshow(myo_frame[:,:,0], interpolation = 'nearest', cmap = 'gray_r', origin = 'upper') if parameters['invert_RGB'] else imgPIVtan_ax.imshow(myo_frame, interpolation = 'nearest', cmap = 'gray', origin = 'upper')
            divider_tan = make_axes_locatable(imgPIVtan_ax)
            if not numpy.all((pvec_tan_mag == 0)): 
                cax_piv_tan = divider_tan.append_axes("right", size="5%", pad=0.05)
                img = imgPIVtan_ax.quiver(mid_markers[:,0], mid_markers[:,1], piv_tan_dir[:,0], piv_tan_dir[:,1],pvec_tan_mag,angles ='xy',cmap = 'nipy_spectral',scale = parameters['piv_scale_factor'], width = 0.003,zorder=2)
                if piv_tan_mag_lim:img.set_clim(piv_tan_mag_lim[0],piv_tan_mag_lim[-1]) 
                FIG.colorbar(img, ax = imgPIVtan_ax, cax = cax_piv_tan)
                cax_piv_tan.yaxis.set_ticks_position("right")
            imgPIVtan_ax.axis('off')
            # apical/basal-myosin-map 
            for axis_counter,(axis,intensity_colorMap,colorMap_lim) in enumerate(zip([img_apical_myo_ax,img_basal_myo_ax],[apical_myo_colorMap,basal_myo_colorMap],[apical_myo_colorMap_lim,basal_myo_colorMap_lim])):
                axis.imshow(myo_frame[:,:,0], interpolation = 'nearest', cmap = 'gray_r', origin = 'upper') if parameters['invert_RGB'] else axis.imshow(myo_frame, interpolation = 'nearest', cmap = 'gray', origin = 'upper')
                divider = make_axes_locatable(axis)
                if not numpy.all((intensity_colorMap == 0)):
                    cax_myo = divider.append_axes("right", size="5%", pad=0.05)
                    img = axis.imshow(intensity_colorMap,cmap = inOutTools.transparent_cmap(plt.get_cmap('rainbow')),interpolation = 'none',origin = 'upper',zorder=2)
                    if colorMap_lim:img.set_clim(colorMap_lim[0],colorMap_lim[-1]) 
                    FIG.colorbar(img, ax = axis, cax = cax_myo)
                    cax_myo.yaxis.set_ticks_position("right")
            img_apical_myo_ax.axis('off')
            img_basal_myo_ax.axis('off')
            # reference-mark-tracking 
            if parameters['view_reference_mark_tracking']: 
                for axis_counter,axis in enumerate([imgPIVtan_ax,img_apical_myo_ax,img_basal_myo_ax]):
                    for ref_mark_counter,(ref_indx,x_dis,y_dis,ref_col) in enumerate(zip([0,len(mid_markers)//4,len(mid_markers)//2,3*len(mid_markers)//4],[-50,0,50,0],[0,-50,0,50],['r','m','b','orange'])):
                        axis.scatter(mid_markers[:,0][ref_indx],mid_markers[:,1][ref_indx], marker = 'o', s = 50.0,facecolors = ref_col,edgecolors = 'k',zorder = 5) 
                        x = [mid_markers[:,0][ref_indx],ellipse_center[0]]
                        y = [mid_markers[:,1][ref_indx],ellipse_center[1]]
                        axis.plot(x,y, c = ref_col, ls = '--', lw = 1.0)
            # save-figure 
            figName = outputPath + '/FIG_piv_myo_sep_' + str(FRAME.frameIndex) + '.' + figFormat
            inOutTools.deleteFile(figName)
            FIG.savefig(figName,format = figFormat, figsize=(10, 3),dpi=500, bbox_inches='tight', pad_inches=0.01)
            plt.close(FIG)
    
    ###################################
    # piv-field-form-a-pair-of-frames #
    ###################################
    @classmethod
    def extract_flow_field(cls,frame_0,frame_1,ws,ol,fr,area,sig_to_noise,piv_cutOff):
        # extract-piv-accross-a-pair-of-movie-frames 
        u, v, sig2noise = PIV.extended_search_area_piv(frame_0.astype(numpy.int32), 
                                                           frame_1.astype(numpy.int32), 
                                                           window_size = ws, 
                                                           overlap = ol, 
                                                           dt = fr, 
                                                           search_area_size = area, 
                                                           sig2noise_method = sig_to_noise
                                                           )
        x, y = PIV.get_coordinates(image_size = frame_0.shape, window_size = ws, overlap = ol)
        sig2noise[sig2noise == numpy.inf] = 1e6
        threshold_after_PIV = 1.0*numpy.min(sig2noise[numpy.nonzero(sig2noise)])
        piv_x_limit = (numpy.min(u),numpy.max(u))
        piv_y_limit = (numpy.min(v),numpy.max(v))
        u, v, piv_mask = inOutTools.global_val_filter_on_velocity_field(u, v, piv_x_limit, piv_y_limit)
        u, v, piv_mask = inOutTools.sig2noise_filter_on_velocity_field(u, v, sig2noise, threshold = threshold_after_PIV)
        u, v = inOutTools.replace_outliers_from_vector_fields(PIV.replace_nans, u, v, method = 'localmean', max_iter = 10, kernel_size = 3)
        x, y, u, v = inOutTools.uniform_scaling_of_vectors(x, y, u, v, scaling_factor = 1.0)
        # discard-piv-above-set-cutoff 
        piv_mat_x,piv_mat_y = x.shape
        if piv_cutOff > 0.0: # remove-noisy-piv-cut-off-based
            uv_Dirs = [list(a) for a in zip(list(u.flatten()),list(v.flatten()))] 
            uv_norms = [numpy.linalg.norm(pvec) for pvec in uv_Dirs]
            uv_cutOff = numpy.mean(uv_norms) + piv_cutOff*numpy.std(uv_norms)
            for i in range(piv_mat_x):
                for j in range(piv_mat_y):
                    if numpy.linalg.norm([u[i][j],v[i][j]]) > uv_cutOff: 
                        u[i][j] = 0.0
                        v[i][j] = 0.0 
        return x,y,u,v,piv_mask
    
    #######################
    # intensity-color-map #
    #######################
    @classmethod
    def extract_intensityColorMap(cls,apical_myo_pixel_distributed,basal_myo_pixel_distributed,apical_polygon_Mask,basal_polygon_Mask,frameDimension):
        # no-myosin-color-map 
        intensity_colorMap_null = numpy.zeros(frameDimension[::-1])
        # construct-requested-myosin-color-map 
        intensity_colorMap_seperate_channel_List = [intensity_colorMap_null]
        all_myo_colorMap = inOutTools.copy_DATA(intensity_colorMap_null)
        for myoSelectFlag,(intensityType,polygonType) in enumerate(zip([apical_myo_pixel_distributed,basal_myo_pixel_distributed],[apical_polygon_Mask,basal_polygon_Mask])):
            intensity_colorMap_seperate_channel = inOutTools.copy_DATA(intensity_colorMap_null) # x-y-dimensions-are-inverted-for-image-representation
            # construct-the-color-map: fill-with-intensity
            for polygon_counter,(intensity,polygon) in enumerate(zip(intensityType,polygonType)):
                # create-empty(dummy)-colorMap
                empty_colorMap = numpy.zeros_like(intensity_colorMap_seperate_channel)
                # fill-the-dummy-colorMap
                inOutTools.cv2.fillPoly(empty_colorMap,[polygon],255) 
                # get-location-of-intensity-in-the-colorMap
                where_signal = numpy.where(empty_colorMap == 255)
                # fill-the-actual-colorMap
                intensity_colorMap_seperate_channel[where_signal] = intensity
                all_myo_colorMap[where_signal] = intensity
            intensity_colorMap_seperate_channel_List.append(intensity_colorMap_seperate_channel)
        no_intensity_colorMap_List,apical_myo_colorMap,basal_myo_colorMap = intensity_colorMap_seperate_channel_List
        return apical_myo_colorMap,basal_myo_colorMap,all_myo_colorMap
    
    #################################
    # myosin-intensity-and-colorMap #
    #################################
    @classmethod
    def extract_MYOSIN_intensity_and_colorMap(cls,apical_polygon_Mask,basal_polygon_Mask,semi_apical_polygon_Mask,semi_basal_polygon_Mask,frameDimension,RGB_scale_myo_pair,myoMask,apical_polygon_Mask_width_height,basal_polygon_Mask_width_height):
        frameDimension = frameDimension[::-1] # NOTE: x-y-dimensions-are-inverted
        # raw-myosin-intensity: averaged-over-pair-of-frames 
        RGB_scale_myo,RGB_scale_myo_next = RGB_scale_myo_pair
        raw_myo_intensity = 0.5*(RGB_scale_myo+RGB_scale_myo_next)
        # compute-myosin-intensity-and-colorMap 
        intensity_values_List = []
        for indx,PolygonLayer in enumerate([[apical_polygon_Mask,basal_polygon_Mask],[semi_apical_polygon_Mask,semi_basal_polygon_Mask]]):
            # take-a-pair-of-polygon-mask-or-semi-polygon-mask: apical,basal 
            intensity_values_per_layer = []
            intensity_colorMap = numpy.zeros(frameDimension)
            for PolygonType in PolygonLayer:
                # extract-intensity(primarily)-also-fill-for-colorMap 
                intensity_values = []
                for polygon in PolygonType:
                    # create-empty(dummy)-colorMap
                    mask = numpy.zeros(frameDimension)
                    # fill-the-dummy-colorMap
                    inOutTools.cv2.fillPoly(mask,[polygon],255) 
                    # get-location-of-intensity-in-the-colorMap
                    where = numpy.where(mask == 255)
                    R_G_B_indv_pixels = raw_myo_intensity[where[0], where[1]]
                    RGB_indv_pixels = [sum(myo) for myo in R_G_B_indv_pixels]   
                    # fill-the-actual-intensity-colorMap
                    intensity_colorMap[where] = RGB_indv_pixels
                    # store-the-intensity-per-polygon 
                    intensity_values.append(RGB_indv_pixels)
                # store-the-intensity-per-individual-layer 
                intensity_values_per_layer.append(intensity_values)
            # store-the-intensity-per-layer-type 
            intensity_values_List.append(intensity_values_per_layer)
        # myosin-intensity: per-length-and-per-pixel 
        apical_intensity_per_length,basal_intensity_per_length = cls.extract_MYOSIN_intensity(intensity_values_List,myoMask,apical_polygon_Mask_width_height,basal_polygon_Mask_width_height)      
        # true/mask-intensity-colorMap 
        return(apical_intensity_per_length,basal_intensity_per_length)
    
    #############################################
    # markers-and-masks-with-respect-to-midline #
    #############################################
    @classmethod
    def apical_basal_markers_and_masks_with_respect_to_midline(cls,mid_markers,apical_markers_raw,basal_markers_raw,apical_markers,basal_markers,imageDimension,layer_widths):
        # transtale-markers-to-respective-raw-reference-marker-lines: apical/basal 
        apical_markers = [inOutTools.nearest_point_on_contour_from_external_point(apical_markers_raw,marker) for marker in apical_markers]
        basal_markers = [inOutTools.nearest_point_on_contour_from_external_point(basal_markers_raw,marker) for marker in basal_markers]
        layer_offSet_List = []
        for layer in [numpy.roll(mid_markers,1,axis=0),numpy.roll(apical_markers,1,axis=0),numpy.roll(basal_markers,1,axis=0)]:
            numNode = len(layer)
            layer_offSet = [0.5*(numpy.array(layer[(node_indx+1)%(numNode)]) + numpy.array(layer[(node_indx)%(numNode)])) for node_indx in range(numNode)]
            layer_offSet_List.append(numpy.array(layer_offSet))
        mid_markers_offSet,_,_ = layer_offSet_List
        # set-myo-mask-width 
        layer_width_apical,layer_width_basal = layer_widths
        sub_layer_width_apical,sub_layer_width_basal = [ele/2.0 for ele in layer_widths]
        layer_width_apical = [-layer_width_apical,-(layer_width_apical+sub_layer_width_apical)] # apical,semi-apical
        layer_width_basal = [-layer_width_basal,-(layer_width_basal+sub_layer_width_basal)] # basal-semi-basal
        layer_widths = [layer_width_apical,layer_width_basal]
        # create-masks-and-markers: apical/basal 
        polygon_Mask,apical_markers,basal_markers = cls.create_apical_basal_polygon_masks(mid_markers_offSet,apical_markers_raw,basal_markers_raw,layer_widths)
        # refine-masks-and-markers: apical/basal 
        polygon_Mask,apical_markers,basal_markers = cls.refine_polygon_masks_at_target_posterior_region(mid_markers,polygon_Mask,[apical_markers_raw,basal_markers_raw],layer_widths)
        # check-ordeing-of-polygon-masks 
        intersecting_edges = []
        for indx0,(a0,b0) in enumerate(zip(apical_markers,basal_markers)):
            for indx1,(a1,b1) in enumerate(zip(apical_markers[indx0+1:],basal_markers[indx0+1:])):
                flag,v,_ = inOutTools.intersection_of_two_LineSegments(a0,b0,a1,b1)
                if flag:
                    intersecting_edges.append([indx0,indx1+indx0+1])
        inOutTools.error(intersecting_edges,inOutTools.get_linenumber(),'inOutTools -> masks are not sequentially orderd !!!')
        # extract-masks-and-markers: apical/basal 
        apical_polygon_Mask,basal_polygon_Mask,semi_apical_polygon_Mask,semi_basal_polygon_Mask = polygon_Mask
        apical_polygon_Mask = numpy.array(apical_polygon_Mask)
        basal_polygon_Mask = numpy.array(basal_polygon_Mask)
        semi_apical_polygon_Mask = numpy.array(semi_apical_polygon_Mask)
        semi_basal_polygon_Mask = numpy.array(semi_basal_polygon_Mask)
        return(apical_markers,basal_markers,apical_polygon_Mask,basal_polygon_Mask,semi_apical_polygon_Mask,semi_basal_polygon_Mask) 
    
    #########################
    # create-apolygon_masks #
    #########################
    @classmethod
    def create_apical_basal_polygon_masks(cls,mid_markers,apical_markers_raw,basal_markers_raw,layer_widths):
        layer_width_apical,layer_width_basal = layer_widths
        # create-polygon-edges: determined-by-layer-widths 
        basal_Mask_refEdge = []
        apical_Mask_refEdge = []
        semi_basal_Mask_refEdge = []
        semi_apical_Mask_refEdge = []
        normDist_outer,normal_dir_outer = inOutTools.nearest_distance_and_direction_to_one_polygon_from_another_polygon(mid_markers,apical_markers_raw,direction='outer')
        normDist_inner,normal_dir_inner = inOutTools.nearest_distance_and_direction_to_one_polygon_from_another_polygon(mid_markers,basal_markers_raw,direction='inner')
        for midPoint,norm_out,norm_in,normDist_out,normDist_in in zip(mid_markers,normal_dir_outer,normal_dir_inner,normDist_outer,normDist_inner): 
            norm_step_List_outer = [normDist_out,normDist_out + layer_width_apical[0],normDist_out + layer_width_apical[1]]  
            normalPoints = [midPoint - norm_step*norm_out for norm_step in norm_step_List_outer]   
            norm_step_List_inner = [normDist_in,normDist_in + layer_width_basal[0],normDist_in + layer_width_basal[1]] 
            normalPoints.extend([midPoint + norm_step*norm_in for norm_step in norm_step_List_inner[::-1]])
            # apical/semi-apical
            apical_Mask_refEdge.append(numpy.array([normalPoints[0],normalPoints[1]])) 
            semi_apical_Mask_refEdge.append(numpy.array([normalPoints[1],normalPoints[2]]))
            # basal/semi-basal
            basal_Mask_refEdge.append(numpy.array([normalPoints[-1],normalPoints[-2]])) 
            semi_basal_Mask_refEdge.append(numpy.array([normalPoints[-2],normalPoints[-3]])) 
        # construct-polygons: using-the-respective-polygon-edges 
        polygon_Mask_List = []
        for maskType in [apical_Mask_refEdge,basal_Mask_refEdge,semi_apical_Mask_refEdge,semi_basal_Mask_refEdge]:
            polygon_vertices = []
            numNode = len(maskType)
            for node_indx in range(numNode):
                e1 = maskType[(node_indx+1)%(numNode)]
                e2 = maskType[(node_indx)%(numNode)]
                polygon = numpy.array(numpy.concatenate((e1,e2[::-1])),numpy.int32)# ordered-polygon
                polygon_vertices.append(polygon)
            polygon_Mask_List.append(polygon_vertices) 
        apical_polygon_Mask,basal_polygon_Mask,_,_ = polygon_Mask_List
        apical_markers = numpy.array([numpy.array(inOutTools.Polygon(polygon).centroid.coords).flatten() for polygon in apical_polygon_Mask])
        basal_markers = numpy.array([numpy.array(inOutTools.Polygon(polygon).centroid.coords).flatten() for polygon in basal_polygon_Mask])
        return polygon_Mask_List,apical_markers,basal_markers
    
    ########################
    # refine-polygon-masks #
    ########################
    @classmethod
    def refine_polygon_masks_at_target_posterior_region(cls,mid_markers,polygon_Mask,apical_basal_markers_ref,layer_widths): 
        mask_refined_List = []
        polygon_centres_List = []
        semi_mask_refined_List = []
        layer_width_apical,layer_width_basal = layer_widths
        apical_Mask,basal_Mask,semi_apical_Mask,semi_basal_Mask = polygon_Mask
        for indx,(mask_semiMask_Type,ld) in enumerate(zip([[inOutTools.copy_DATA(apical_Mask),inOutTools.copy_DATA(semi_apical_Mask)],[inOutTools.copy_DATA(basal_Mask),inOutTools.copy_DATA(semi_basal_Mask)]],[layer_width_apical,layer_width_basal])):
            # refine-polygon-masks-having-width > 10-times-the-width-of-smallest-polygon 
            maskType,semi_maskType = mask_semiMask_Type
            mask_Width_Height,_ = inOutTools.extract_width_and_hegith_of_polygons(maskType)
            division_polygon_num = numpy.array(mask_Width_Height[:,0]/(10*min(mask_Width_Height[:,0])),int)
            polygon_centres = numpy.array([numpy.array(inOutTools.Polygon(polygon).centroid.coords).flatten() for polygon in maskType])
            for refine_indx,refine_polygon_iteration in enumerate(division_polygon_num):
                # increase-polygon-node-number-by-inserting-an-edge: mid-edge 
                c1 = numpy.array(inOutTools.nearest_point_on_contour_from_external_point(apical_basal_markers_ref[indx],polygon_centres[refine_indx]))
                normal_dir = inOutTools.normalize(c1-mid_markers[refine_indx])
                c1 = numpy.array(c1)
                c2 = numpy.array(c1 + ld[0]*normal_dir,int)
                c3 = numpy.array(c1 + ld[1]*normal_dir,int)
                maskType[refine_indx] = numpy.insert(maskType[refine_indx],[0,2],[c1,c2],axis=0)
                semi_maskType[refine_indx] = numpy.insert(semi_maskType[refine_indx],[0,2],[c2,c3],axis=0)
                # refined-polygon-centre: mid-point-of-the-two-newly-inserted-markers-on-the-polygon-mask
                polygon_centres[refine_indx] = 0.5*(c1 + c2)   
                # increase-polygon-node-number-by-inserting-a-pair-of-edges: left/rigth-to-the-mid-edge 
                for N_max in range(refine_polygon_iteration):
                    markers_Mask_add_List = []
                    markers_semi_Mask_add_List = []
                    for refine_indx_next in range(2**(N_max+1)):
                        # mid-point-of-outer-edge    
                        p1 = numpy.array(0.5*numpy.array(maskType[refine_indx][refine_indx_next-1]+maskType[refine_indx][refine_indx_next]),int) 
                        # mid-point-of-intermediate-edge
                        p2 = numpy.array(0.5*numpy.array(maskType[refine_indx][-(refine_indx_next+2)]+maskType[refine_indx][-(refine_indx_next+3)]),int) 
                        distance = numpy.linalg.norm(p2-p1)
                        # mid-point-of-inner-edge
                        p3 = numpy.array(0.5*numpy.array(semi_maskType[refine_indx][-(refine_indx_next+2)]+semi_maskType[refine_indx][-(refine_indx_next+3)]),int) 
                        semi_distance = numpy.linalg.norm(p3-p2)
                        # translate-mask/semi-mask-to-fit-with-the-raw-apical/basal-contour 
                        p1 = numpy.array(inOutTools.nearest_point_on_contour_from_external_point(apical_basal_markers_ref[indx],p1),int)
                        p2 = numpy.array(p1+distance*inOutTools.normalize(p2-p1),int)
                        p3 = numpy.array(p2+semi_distance*inOutTools.normalize(p3-p2),int)
                        # polygon-masks
                        markers_Mask_add_List.append(p1)
                        markers_Mask_add_List.append(p2)
                        # semi-polygon-masks
                        markers_semi_Mask_add_List.append(p2) 
                        markers_semi_Mask_add_List.append(p3)
                    # insert-newly-created-markers-into-the-corresponding-polygon-masks/semi-polygon-masks
                    insert_indx_list = []
                    for insert_indx in range(2**(N_max+1)):
                        insert_indx_list.extend([insert_indx,2**(N_max+2)-insert_indx])
                    maskType[refine_indx] = numpy.insert(maskType[refine_indx],insert_indx_list,markers_Mask_add_List,axis=0)
                    semi_maskType[refine_indx] = numpy.insert(semi_maskType[refine_indx],insert_indx_list,markers_semi_Mask_add_List,axis=0)
            mask_refined_List.append(maskType)
            semi_mask_refined_List.append(semi_maskType)
            polygon_centres_List.append(polygon_centres) 
        # extract-refines-polygon-masks: apical/basal 
        apical_polygon_Mask,basal_polygon_Mask = mask_refined_List
        semi_apical_mask_List,semi_basal_mask_List = semi_mask_refined_List 
        apical_markers,basal_markers = polygon_centres_List
        return [apical_polygon_Mask,basal_polygon_Mask,semi_apical_mask_List,semi_basal_mask_List],apical_markers,basal_markers
    
    ####################
    # myosin-intensity #
    ####################
    @classmethod
    def extract_MYOSIN_intensity(cls,intensity_set,apply_MyoMask,apical_polygon_Mask,basal_polygon_Mask):     
        # function: 1 
        def average_MYOSIN_intensity_per_pixel_within_polygon_mask(true,mask):
            # average-of-true-intensity 
            true_avg_apical = sum(true[0])/len(true[0])
            true_avg_basal = sum(true[1])/len(true[1])
            # average-of-mask-intensity 
            mask_avg_apical = sum(mask[0])/len(mask[0])
            mask_avg_basal = sum(mask[1])/len(mask[1])
            return([true_avg_apical,true_avg_basal],[mask_avg_apical,mask_avg_basal])
        # apical/basal-mask-width 
        apical_polygon_Mask_width_height,apical_poly_mid_markers_List = inOutTools.extract_width_and_hegith_of_polygons(apical_polygon_Mask)
        basal_polygon_Mask_width_height,basal_poly_mid_markers_List = inOutTools.extract_width_and_hegith_of_polygons(basal_polygon_Mask)
        apical_layer_width = apical_polygon_Mask_width_height[:,0]
        basal_layer_width = basal_polygon_Mask_width_height[:,0]
        # integrated-intensity-at-different-types-masks/sub-mask: apical/sub-apical,basal/sub-basal 
        apical_basal_integrated_intensity_raw = numpy.array(intensity_set[0]).T
        apical_basal_mask_integrated_intensity_raw = numpy.array(intensity_set[1]).T
        # seperate-apical/basal-intensity 
        apical_basal_intensity_per_length = []
        for indx,(true,mask) in enumerate(zip(apical_basal_integrated_intensity_raw,apical_basal_mask_integrated_intensity_raw)):
            true_avg,mask_avg = average_MYOSIN_intensity_per_pixel_within_polygon_mask(true,mask)
            # masked-intensity: actual-intensity - sub-intensity 
            true_apical = numpy.array(true[0])
            true_basal = numpy.array(true[1])
            if apply_MyoMask: 
                true_apical = numpy.array(true_apical - mask_avg[0])
                true_basal = numpy.array(true_basal - mask_avg[1])
                true_apical[true_apical < 0] = 0 # replace-negative-apical-intensity-by-zero 
                true_basal[true_basal < 0] = 0 # replace-negative-basal-intensity-by-zero
            # per-length-average 
            apical_basal_intensity_per_length.append([sum(true_apical)/apical_layer_width[indx],sum(true_basal)/basal_layer_width[indx]]) 
        # list-to-array-conversion 
        apical_basal_intensity_per_length = numpy.array(apical_basal_intensity_per_length) 
        apical_intensity_per_length,basal_intensity_per_length = [apical_basal_intensity_per_length[:,0],apical_basal_intensity_per_length[:,1]]
        return(apical_intensity_per_length,basal_intensity_per_length)

    ##############################
    # process-frames-and-markers #
    ##############################
    @classmethod
    def process_frames_and_markers(cls,mem_frame_pair,myo_frame_pair,marker_frame,img_masks,apply_masks):
        # generate-piv-frame-pairs-from-membrane-frames 
        piv_frame_pair = []
        for mem_frame in mem_frame_pair:
            mem_img = inOutTools.readImage(mem_frame,'color') 
            GRAY_scale_mem = inOutTools.cv2.cvtColor(mem_img.copy(),inOutTools.cv2.COLOR_BGR2GRAY) # convert-to-gray-scale 
            piv_frame_pair.append(GRAY_scale_mem.copy())
        # myo-RGB-values 
        RGB_scale_myo_pair = []
        for myo_frame in myo_frame_pair:
            myo_img = inOutTools.readImage(myo_frame,'color')
            RGB_scale_myo = inOutTools.cv2.merge(inOutTools.cv2.split(myo_img)) 
            RGB_scale_myo_pair.append(RGB_scale_myo)
        # membrane/myo-frames 
        mem_img = inOutTools.readImage(mem_frame_pair[0],'color') 
        myo_img = inOutTools.readImage(myo_frame_pair[0],'color') 
        # masked-frames 
        mem_masked_img = mem_img.copy()
        myo_masked_img = myo_img.copy()
        if apply_masks:
            background_mask,yolk_mask = img_masks 
            yolk_mask = 255 - yolk_mask
            # mem-mask
            mem_masked_img[background_mask.astype(numpy.bool)] = 255 
            mem_masked_img[yolk_mask.astype(numpy.bool)] = 255
            # myo-mask
            myo_masked_img[background_mask.astype(numpy.bool)] = 255 
            myo_masked_img[yolk_mask.astype(numpy.bool)] = 255
        return(mem_img,myo_img,mem_masked_img,myo_masked_img,RGB_scale_myo_pair,piv_frame_pair)

    #############################
    # active-moment-ingredients #
    #############################
    @classmethod 
    def extract_activeMoment_ingredients(cls,apical_intensity,basal_intensity,mid_markers,apical_markers,basal_markers):
        # active-moment-ingredients: apical-myosion,basal-myosin,cell-height 
        e_h_List = []
        basal_myo_List = []
        apical_myo_List = []
        apical_basal_point_pairs = numpy.array([[a,b] for a,b in zip(apical_markers,basal_markers)])
        for marker_pair,mid_mark,apical_myo,basla_myo in zip(apical_basal_point_pairs,mid_markers,apical_intensity,basal_intensity):
            # myosin: apical/basal 
            apical_myo_List.append(apical_myo)
            basal_myo_List.append(basla_myo)
            # cell-height 
            e_h_List.append(2.0*numpy.average([numpy.linalg.norm(marks-mid_mark) for marks in marker_pair]))
        return(numpy.array(e_h_List),numpy.array(apical_myo_List),numpy.array(basal_myo_List))

    #######################
    # markers-from-frames #
    #######################
    @classmethod 
    def extract_different_markers(cls,marker_frame,reMarker_Number,apical_off_set,basal_off_set,epithelium_orientation):
        # load-frame-image 
        img = inOutTools.readImage(marker_frame,'color') # remove-transparency 
        ref_frame = inOutTools.cv2.cvtColor(img.copy(),inOutTools.cv2.COLOR_BGR2GRAY) # convert-to-gray-scale
        # reference-image-dimension 
        y_dim,x_dim = ref_frame.shape[:2]
        imageDimension = [x_dim,y_dim]
        # detect-contours: apical/basal 
        blured_Frame = inOutTools.cv2.GaussianBlur(ref_frame,(5,5),0.0)
        ret,thresh = inOutTools.cv2.threshold(blured_Frame.copy(),0,255,0)  # second-argument: free-threshold-value, third-argument: max-threshold-value
        contours, hierarchy = inOutTools.cv2.findContours(thresh, inOutTools.cv2.RETR_TREE, inOutTools.cv2.CHAIN_APPROX_SIMPLE)      
        # conversion: contour-to-apical/basal-markers 
        apical_markers = None
        basal_markers = None
        if(len(contours) > 0):
            # sort-contours-by-areas
            contourArea = [inOutTools.cv2.contourArea(c) for c in contours]
            contour_indicesr_by_large_area = numpy.argsort(contourArea)
            contour_indicesr_by_large_area = contour_indicesr_by_large_area[::-1]
            # first-two-large-contours-are-used-for-apical/basal-markers  
            apical_basal_contours = [contours[indx] for indx in contour_indicesr_by_large_area[:2]]
            apical_markers,basal_markers = [inOutTools.polygon_from_image_contour(apical_basal_contours[indx].T,reMarker_Number*(indx+1)) for indx in range(len(apical_basal_contours))]
        else:
            inOutTools.error(True,inOutTools.get_linenumber(),'No apical/basal contour detected !')
        # ordered-markers: apical/basal   
        apical_markers = numpy.flip(apical_markers, axis = 0) if epithelium_orientation=='D-ccw' else apical_markers
        basal_markers  = numpy.flip(basal_markers, axis = 0) if epithelium_orientation=='D-ccw' else basal_markers
        # shifting-apical/basal-markers-from-edges-to-bulk-of-epithelium 
        _,normals = inOutTools.tangent_normals_along_polygon(apical_markers,closed=True)
        apical_markers = apical_markers - apical_off_set*normals # inward
        _,normals = inOutTools.tangent_normals_along_polygon(basal_markers,closed=True)
        basal_markers = basal_markers + basal_off_set*normals # outward
        # uniform-distribution-of-markers:apical/basal 
        apical_markers,_ = inOutTools.uniform_distribution_along_polygon(apical_markers,len(apical_markers),closed=True)
        basal_markers,_ = inOutTools.uniform_distribution_along_polygon(basal_markers,len(basal_markers),closed=True)
        # effective-embryo: yolk + epithelium (masks-for-removing-background) 
        img_masks = [None,None]
        for indx,markers in enumerate([apical_markers,basal_markers]):
            contours = numpy.array([markers],int) 
            img = inOutTools.readImage(marker_frame,'color') # remove-transparency
            ref_img = inOutTools.cv2.cvtColor(img.copy(),inOutTools.cv2.COLOR_BGR2GRAY) # convert-to-gray-scale 
            imageFieldBlacked = numpy.ones_like(ref_img.copy())*255
            img_masks[indx] = inOutTools.cv2.drawContours(imageFieldBlacked,contours,0,0,inOutTools.cv2.FILLED)
            
        return(apical_markers,basal_markers,img_masks,imageDimension)
    
#======================================================================================================#
#                                           class: Animal1D                                            #
#======================================================================================================#
class Animal1D:
    
    #####################
    # initialize-animal #
    #####################
    def __init__(self,*args,**kwarg):  

        return

    #############################
    # update-time-series-animal #
    #############################
    def processFrames_ANIMAL(self,frameSequences_Map,frameIndex_Map,parametersFileName): 
        posterior_pole_location,epithelium_orientation,self.initial_frame,segmented_frames_first,segmented_frames_last,self.transition_cutOff_val = inOutTools.list_flatten_2D(frameIndex_Map)
        parameters = inOutTools.read_parameter_file(parametersFileName)
        self.window_avg_SIZE = int(parameters['window_avg_SIZE'])
        self.temporal_allignment = parameters['temporal_allignment']
        self.posterior_domain = numpy.array(parameters['posterior_domain'],int)
        self.spatial_shift_by_node_index = parameters['spatial_shift_by_node_index']
        ##################  
        # analyze-frames #
        ##################
        s_List = []
        frames_List = []
        myo_frame_List = []
        frameIndex_List = []
        mid_markers_List = []
        animal_frames_data = []
        u_dis_tangent_List = [] 
        apical_markers_List = []  
        u_dis_tangent = numpy.zeros(int(parameters['reMarker_Number'])-1)                                                                                                                                                 
        for frame_indx in range(segmented_frames_first,segmented_frames_last+1):
            # frame
            FRAME = Frame1D()
            FRAME.reference_frame_information(self.animalPath,frameSequences_Map['MARKERS'][segmented_frames_first],parametersFileName,epithelium_orientation,posterior_pole_location)
            FRAME.analyze_FRAME(frame_indx,frameSequences_Map['MARKERS'][frame_indx],frameSequences_Map['MYO'][frame_indx],frameSequences_Map['MEM'][frame_indx],parametersFileName)
            frames_List.append(FRAME)
            # displacement
            s_List.append(FRAME.s)
            piv_tangent_interpolator = inOutTools.interpolate_Measurables_OnArcLength(FRAME.s,FRAME.piv_tangent) 
            u_dis_tangent = u_dis_tangent + parameters['time_between_frames']*numpy.array(piv_tangent_interpolator(s_List[0]+u_dis_tangent))  
            u_dis_tangent_List.append(u_dis_tangent)
            # other
            myo_frame_List.append(FRAME.myo_frame)
            frameIndex_List.append(FRAME.frameIndex)
            mid_markers_List.append(FRAME.mid_markers)
            apical_markers_List.append(FRAME.apical_markers)
            animal_frames_data.append([FRAME.s,FRAME.e_h,FRAME.curv,FRAME.apical_myo,FRAME.basal_myo,FRAME.piv_tangent,FRAME.piv_normal]) 
        s_List,e_h_List,curv_List,apical_myo_List,basal_myo_List,piv_tan_List,piv_norm_List = numpy.swapaxes(animal_frames_data,0,1) 
        # truncate-data 
        pos_piv_tan_List = inOutTools.truncate_Data_Range(piv_tan_List,self.posterior_domain) 
        pos_apical_myo_List = inOutTools.truncate_Data_Range(apical_myo_List,self.posterior_domain)
        pos_mid_markers_List = inOutTools.truncate_Data_Range(mid_markers_List,self.posterior_domain)
        ####################### 
        # average-over-frames #
        #######################
        pos_piv_tan_sp_avg_List = []
        full_piv_tan_sp_avg_List = []
        pos_apical_myo_sp_avg_List = []
        full_apical_myo_sp_avg_List = []
        for time_indx,(mid_markers,apical_markers,piv_tan,apical_myo,pos_mid_markers,pos_piv_tan,pos_apical_myo) in enumerate(zip(mid_markers_List,apical_markers_List,inOutTools.sliding_window_average_data(piv_tan_List,self.window_avg_SIZE),inOutTools.sliding_window_average_data(apical_myo_List,self.window_avg_SIZE),pos_mid_markers_List,pos_piv_tan_List,pos_apical_myo_List)):
            s,s_max = inOutTools.arc_length_along_polygon(mid_markers)
            # spatially-averaged-piv 
            area_under_piv_tan = inOutTools.area_under_curve(s/s_max,numpy.array(inOutTools.sliding_window_average_data(piv_tan,self.window_avg_SIZE)),closed=False)
            full_piv_tan_sp_avg_List.append(area_under_piv_tan) 
            # total-apical-myo
            area_under_apical_myo = sum(apical_myo)
            full_apical_myo_sp_avg_List.append(area_under_apical_myo)
            # posterior-epithelium 
            pos_s,pos_s_max = inOutTools.arc_length_along_polygon(pos_mid_markers)
            # spatially-averaged-piv
            area_under_piv_tan = inOutTools.area_under_curve(pos_s/pos_s_max,numpy.array(inOutTools.sliding_window_average_data(pos_piv_tan,self.window_avg_SIZE)),closed=False)
            pos_piv_tan_sp_avg_List.append(area_under_piv_tan) 
            # total-apical-myo
            area_under_apical_myo = sum(pos_apical_myo)
            pos_apical_myo_sp_avg_List.append(area_under_apical_myo)
        # window-average 
        self.FRAMES = frames_List
        self.frameIndices = frameIndex_List
        self.pos_piv_avg = numpy.array(inOutTools.sliding_window_average_data(pos_piv_tan_sp_avg_List,self.window_avg_SIZE))
        self.pos_apical_myo_avg = numpy.array(inOutTools.sliding_window_average_data(pos_apical_myo_sp_avg_List,self.window_avg_SIZE))
        self.full_piv_avg = numpy.array(inOutTools.sliding_window_average_data(full_piv_tan_sp_avg_List,self.window_avg_SIZE))
        self.full_apical_myo_avg = numpy.array(inOutTools.sliding_window_average_data(full_apical_myo_sp_avg_List,self.window_avg_SIZE))
        #################################  
        # temporal-allignment-of-frames #
        #################################
        coeff = None
        piv_fitting_range = None
        sym_asym_transition_frame = None
        piv_transition_cutOff_val = self.transition_cutOff_val if self.temporal_allignment else -1.0*self.transition_cutOff_val
        if piv_transition_cutOff_val > 0.0:
            cutOff_indices, = numpy.where(self.full_piv_avg > piv_transition_cutOff_val)
            piv_cutOff_index = 0
            if cutOff_indices.size > 0:
                piv_cutOff_index = cutOff_indices[0] 
            # piv-avg-above-cut-off
            piv_valid_for_fitting_range = len(self.frameIndices)-piv_cutOff_index 
            # sym-to-asym-frame-index 
            if piv_valid_for_fitting_range > 5:
                piv_fitting_range = piv_cutOff_index + 5
                frame_indx_patch = self.frameIndices[piv_cutOff_index:piv_fitting_range]
                piv_tan_sp_avg_patch = self.full_piv_avg[piv_cutOff_index:piv_fitting_range]
                coeff = numpy.polyfit(frame_indx_patch,piv_tan_sp_avg_patch,1) # line-fitting
                # sym-to-asym-transition-frame-indx
                sym_asym_transition_frame = int(round(-1.0*coeff[1]/coeff[0]))
                frameIndexDic = {item:indx for indx,item in enumerate(self.frameIndices)}
                sym_asym_transition_frame_reverseMap = frameIndexDic[sym_asym_transition_frame]
                if self.full_piv_avg[sym_asym_transition_frame_reverseMap] < 0:
                    full_piv_tan_sp_avg_List_negative_indices, = numpy.where(self.full_piv_avg[sym_asym_transition_frame_reverseMap:]< 0)
                    sym_asym_transition_frame = self.frameIndices[sym_asym_transition_frame_reverseMap+max(full_piv_tan_sp_avg_List_negative_indices)+1]  
                sym_asym_transition_frame = int(sym_asym_transition_frame)
            else:
                print('Allignmnet failed !!!, number of frames after transition is <', 5)
                inOutTools.terminate()
        else:
            print('no allignmnet requested !!!')
            sym_asym_transition_frame = self.frameIndices[0]
        self.transition_frame_indx = sym_asym_transition_frame
        self.transition_detection_information = [piv_transition_cutOff_val,piv_fitting_range,coeff] 
        if self.transition_frame_indx is None: 
            print('--> transition can not be detected: !!! add more frames OR reduce transition cut-off !!!') 
        ##############
        # ouput-data #
        ##############
        self.transition_reference_indx = self.transition_frame_indx-self.frameIndices[0]
        # shift-reference-origin
        e_h_List,curv_List,basal_myo_List,apical_myo_List,piv_norm_List,mid_markers_List,piv_tan_List,u_dis_tangent_List = [[numpy.roll(item,self.spatial_shift_by_node_index,axis=0) for item in items] for items in [e_h_List,curv_List,basal_myo_List,apical_myo_List,piv_norm_List,mid_markers_List,piv_tan_List,u_dis_tangent_List]]
        # close-epithelium
        mid_markers_List,piv_tan_List,piv_norm_List,u_dis_tangent_List,curv_List,e_h_List,apical_myo_List,basal_myo_List = [[numpy.append(item,[item[0]],axis=0) for item in items] for items in [mid_markers_List,piv_tan_List,piv_norm_List,u_dis_tangent_List,curv_List,e_h_List,apical_myo_List,basal_myo_List]]
        # recalculate-arc-length
        s_List = [numpy.insert(numpy.cumsum(numpy.sqrt(numpy.sum(numpy.diff(markers,axis = 0)**2,axis = 1))),0,1e-6) for markers in mid_markers_List]
        # mid-markers: after/before-transition
        self.mid_markers_after_transition = mid_markers_List[self.transition_reference_indx:]
        self.mid_markers_before_transition = mid_markers_List[:self.transition_reference_indx+1]
        # image-frames: after/before-transition
        self.myo_frames_after_transition = myo_frame_List[self.transition_reference_indx:]
        self.myo_frames_before_transition = myo_frame_List[:self.transition_reference_indx+1]
        # record-output-data
        self.s_frames,self.piv_tan_frames,self.piv_norm_frames,self.u_dis_tangent_frames,self.curv_frames,self.e_h_frames,self.apical_myo_frames,self.basal_myo_frames = [inOutTools.sliding_window_average_data(item,self.window_avg_SIZE) for item in [s_List,piv_tan_List,piv_norm_List,u_dis_tangent_List,curv_List,e_h_List,apical_myo_List,basal_myo_List]]
        
        return

    ##################
    # analyze-animal #
    ##################
    def analyze_ANIMAL(self,ID,frameSequences_Map,frameIndex_Map,parametersFileName,animalPath):
        print('animal(analyzing):',ID)
        self.ID = ID
        self.animalPath = animalPath
        self.processFrames_ANIMAL(frameSequences_Map,frameIndex_Map,parametersFileName)
        
        return  
    
    #################
    # visualization #
    #################
    def view_ANIMAL(self,parametersFileName,pixel_to_micron_conversion_factor,figFormat):
        print('animal(visualizing):',self.ID)
        # delete-existing-images
        inOutTools.delete_files_with_specific_extension(self.animalPath,'.' + figFormat)
        ###############
        # frames-view #
        ###############
        # limits
        piv_tan_mag_List = []
        bulk_piv_mag_List = []
        all_myo_colorMap_List = []
        basal_myo_colorMap_List = []
        apical_myo_colorMap_List = []
        for FRAME in self.FRAMES:     
            parameters = inOutTools.read_parameter_file(parametersFileName) 
            apical_myo_colorMap,basal_myo_colorMap,all_myo_colorMap = FRAME.extract_intensityColorMap(FRAME.apical_myo_pixel_distributed,FRAME.basal_myo_pixel_distributed,FRAME.apical_polygon_Mask,FRAME.basal_polygon_Mask,FRAME.frameDimension)
            truncate_data = [FRAME.pvec_tan_mag,FRAME.bulk_pvec_mag,apical_myo_colorMap,basal_myo_colorMap,all_myo_colorMap]
            pvec_tan_mag,bulk_piv_mag,apical_myo_colorMap,basal_myo_colorMap,all_myo_colorMap = [inOutTools.truncate_Data_Range(item,FRAME.posterior_domain) if parameters['view_posterior_domain'] else item for item in truncate_data] 
            piv_tan_mag_List.append(pvec_tan_mag)
            bulk_piv_mag_List.append(bulk_piv_mag)
            all_myo_colorMap_List.append(inOutTools.flatten_List(all_myo_colorMap))
            basal_myo_colorMap_List.append(inOutTools.flatten_List(basal_myo_colorMap))
            apical_myo_colorMap_List.append(inOutTools.flatten_List(apical_myo_colorMap))
        piv_tan_mag_List,bulk_piv_mag_List,all_myo_colorMap_List,basal_myo_colorMap_List,apical_myo_colorMap_List = [inOutTools.flatten_List(item) for item in [piv_tan_mag_List,bulk_piv_mag_List,all_myo_colorMap_List,basal_myo_colorMap_List,apical_myo_colorMap_List]]
        limits = [[numpy.min(item),numpy.max(item)] for item in [piv_tan_mag_List,bulk_piv_mag_List,all_myo_colorMap_List,basal_myo_colorMap_List,apical_myo_colorMap_List]]
        # view
        for FRAME in self.FRAMES:
            FRAME.view_FRAME(self.animalPath,parametersFileName,pixel_to_micron_conversion_factor,figFormat,limits)
        ########################
        # transition detection #
        ########################
        piv_transition_cutOff_val,piv_fitting_range,piv_transition_steepness_coeff = self.transition_detection_information
        piv_transition_cutOff_val,piv_transition_steepness_coeff,full_piv_avg = [ele*pixel_to_micron_conversion_factor for ele in [piv_transition_cutOff_val,piv_transition_steepness_coeff,self.full_piv_avg]]
        if piv_transition_cutOff_val > 0.0:
            FIG,piv_tangent_sp_avg_ax = plt.subplots(1,1,figsize = (2.6,1.3))
            # raw-piv-avg-data
            piv_tangent_sp_avg_ax.scatter(self.frameIndices,full_piv_avg, c = 'k', marker = 'o', s = 5,zorder=1,label = self.ID)
            # transition-references
            piv_tangent_sp_avg_ax.axvline(self.transition_frame_indx, c = 'm', ls = '-', lw = 1.0)
            fit_line = numpy.poly1d(piv_transition_steepness_coeff)
            frameIndex_List_regression = numpy.linspace(self.transition_frame_indx,self.frameIndices[-1],10) 
            piv_tangent_sp_avg_ax.plot(frameIndex_List_regression,fit_line(frameIndex_List_regression) , ls  = '--', c = 'm', lw = 1.0,zorder=2)
            # cut-off-references
            piv_tangent_sp_avg_ax.axhspan(0.0,piv_transition_cutOff_val, alpha=0.5, facecolor='r',edgecolor='none') 
            piv_tangent_sp_avg_ax.axhspan(piv_transition_cutOff_val,full_piv_avg[piv_fitting_range-1], alpha=0.5, facecolor='g',edgecolor='none')
            piv_tangent_sp_avg_ax.axhspan(full_piv_avg[piv_fitting_range-1],max(full_piv_avg),alpha=0.5, facecolor='r',edgecolor='none') 
            # highlight-transition-region
            inOutTools.customize_axis(piv_tangent_sp_avg_ax,xlim=[],ylim=[-piv_transition_cutOff_val,max(full_piv_avg)+piv_transition_cutOff_val],x_pad=0.0,leg_loc=2,leg_size=2,hline_pos=0.0,vline_pos=0.0,tick_size=5)
            # save-figure
            figName = self.animalPath  + '/FIG_transition_cutoff=' + str(piv_transition_cutOff_val) + '.' + figFormat
            inOutTools.deleteFile(figName)
            FIG.savefig(figName,format = figFormat, figsize=(10, 3), dpi = 500, bbox_inches='tight', pad_inches=0.01)
            plt.close(FIG)  
            
        return
    
    #########################
    # vertex-model-template #
    #########################
    def view_vertex(self,figFormat):
        FRAME = inOutTools.copy_DATA(self.FRAMES[0])
        FIG, vertex_ax = plt.subplots(1, 1, figsize = (5,2))
        FRAME.orient_AnteriorPosterior_FRAME(crop_margin=100) 
        # transform-image-coordiante-to-standard-coordiante    
        animal_ref_st,apical_markers_st,basal_markers_st = [markers*numpy.array([1,-1]) for markers in [FRAME.animal_markers_ref,FRAME.apical_markers,FRAME.basal_markers]]   
        animal_ref_st,apical_markers_st,basal_markers_st = [markers-numpy.mean(animal_ref_st,axis=0) for markers in [animal_ref_st,apical_markers_st,basal_markers_st]]
        animal_ref_st_line,apical_st_line,basal_st_line = [inOutTools.open_to_closed_polygon(markers) for markers in [animal_ref_st,apical_markers_st,basal_markers_st]]
        # draw-contour-and-edges 
        vertex_ax.plot(apical_st_line[:,0],apical_st_line[:,1], c = 'k', ls = '-', lw = 0.5)
        vertex_ax.plot(basal_st_line[:,0],basal_st_line[:,1], c = 'k', ls = '-', lw = 0.5)
        vertex_ax.plot(animal_ref_st_line[:,0],animal_ref_st_line[:,1], c = 'm', ls = '--', lw = 0.5) 
        for marker_type_counter,(a,b) in enumerate(zip(apical_markers_st,basal_markers_st)):
            vertex_ax.add_line(Line2D([a[0],b[0]],[a[1],b[1]], c = 'k', lw = 0.5))
        vertex_ax.axis('equal')
        vertex_ax.axis('off')
        vertex_ax.axis('off') 
        figName = self.animalPath + '/Fig_vertex_temp' + '.' + figFormat
        inOutTools.deleteFile(figName)
        FIG.savefig(figName,format = figFormat, figsize=(10, 3), dpi = 500, bbox_inches='tight', pad_inches=0.01)
        plt.close(FIG)
        # save-vertex-data
        inOutTools.save_to_file({'ref-X-coordinates':animal_ref_st[:,0],'ref-Y-coordinates':animal_ref_st[:,1],'apical-X-coordinates':apical_markers_st[:,0], 'apical-Y-coordinates':apical_markers_st[:,1],'basal-X-coordinates':basal_markers_st[:,0],'basal-Y-coordinates':basal_markers_st[:,1]},self.animalPath + '/vertex.dat')

    ########
    # save #
    ########
    def save(self,dataPath,fileName):
        inOutTools.createDirectory(dataPath)
        inOutTools.dump_data_via_pickle(dataPath+'/'+fileName+'_'+self.ID,self)
        
        return
    
#======================================================================================================#
#                                         class: Genotype1D                                            #
#======================================================================================================#
class Genotype1D:
    
    #######################
    # initialize-genotype #
    #######################
    def __init__(self,*args,**kwarg):    

        return
    
    def processAnimals_GENOTYPE(self,frameSequences_Maps,frameIndex_Maps,parametersFileName,moviePath):
        parameters = inOutTools.read_parameter_file(parametersFileName)
        self.time_between_frames = parameters['time_between_frames']
        self.spatial_shift_by_node_index = int(parameters['spatial_shift_by_node_index'])
        animal_List = [] 
        all_frames_List = []
        non_seg_frames_List = []
        all_animals_frames_data = []
        pos_piv_tan_sp_time_series = []
        full_piv_tan_sp_time_series = []
        myo_frames_after_transition = []
        myo_frames_before_transition = []
        mid_markers_after_transition = []
        mid_markers_before_transition = []
        pos_apical_myo_sp_time_series = []
        full_apical_myo_sp_time_series = []
        seg_frames_after_transition_List = []
        seg_frames_before_transition_List = []
        for animal_ID,frameIndex_Map in frameIndex_Maps.items():
            # animal
            ANIMAL = Animal1D()
            ANIMAL.analyze_ANIMAL(ID=animal_ID,frameSequences_Map=frameSequences_Maps[animal_ID],frameIndex_Map=frameIndex_Map,parametersFileName=parametersFileName,animalPath=moviePath+'/'+animal_ID)
            animal_List.append(ANIMAL)
            # other
            pos_piv_tan_sp_time_series.append(ANIMAL.pos_piv_avg)
            full_piv_tan_sp_time_series.append(ANIMAL.full_piv_avg)
            pos_apical_myo_sp_time_series.append(ANIMAL.pos_apical_myo_avg)
            full_apical_myo_sp_time_series.append(ANIMAL.full_apical_myo_avg) 
            myo_frames_after_transition.append(ANIMAL.myo_frames_after_transition)
            non_seg_frames_List.append(ANIMAL.frameIndices[0]-ANIMAL.initial_frame)
            myo_frames_before_transition.append(ANIMAL.myo_frames_before_transition)
            mid_markers_after_transition.append(ANIMAL.mid_markers_after_transition)
            mid_markers_before_transition.append(ANIMAL.mid_markers_before_transition)
            seg_frames_before_transition_List.append(ANIMAL.transition_reference_indx)
            all_frames_List.append(ANIMAL.frameIndices[0]-ANIMAL.initial_frame+len(ANIMAL.frameIndices))
            seg_frames_after_transition_List.append(ANIMAL.frameIndices[-1]- ANIMAL.transition_frame_indx)
            all_animals_frames_data.append([ANIMAL.e_h_frames,ANIMAL.curv_frames,ANIMAL.s_frames,ANIMAL.piv_tan_frames,ANIMAL.piv_norm_frames,ANIMAL.u_dis_tangent_frames,ANIMAL.basal_myo_frames,ANIMAL.apical_myo_frames])
        ##################
        # allign-animals #
        ##################
        self.transition_merge_frame_reference = max(seg_frames_before_transition_List)
        # piv-raw (masked)
        frames_offSet_back_front_List = [[nsf_frame_indx,max(all_frames_List) - max_frame_indx] for nsf_frame_indx,max_frame_indx in zip(non_seg_frames_List,all_frames_List)]
        pos_piv_raw_List,indv_emb_piv_not_alligned,pos_apical_myo_raw_List,full_apical_myo_raw_List = [inOutTools.masked_data(item,array_shift=frames_offSet_back_front_List,matrix_shift=[]) for item in [pos_piv_tan_sp_time_series,full_piv_tan_sp_time_series,pos_apical_myo_sp_time_series,full_apical_myo_sp_time_series]]
        # piv-alligned (masked) 
        frames_offSet_back_front_List = [[self.transition_merge_frame_reference-sfbt_frame_indx,max(seg_frames_after_transition_List)-sfat_frame_indx] for sfbt_frame_indx,sfat_frame_indx in zip(seg_frames_before_transition_List,seg_frames_after_transition_List)]
        pos_piv_alligned_List,indv_emb_piv_alligned_List,pos_apical_myo_alligned_List,full_apical_myo_alligned_List = [inOutTools.masked_data(item,array_shift=frames_offSet_back_front_List,matrix_shift=[]) for item in [pos_piv_tan_sp_time_series,full_piv_tan_sp_time_series,pos_apical_myo_sp_time_series,full_apical_myo_sp_time_series]]
        # frames/markers-alligned
        emb_indx_with_max_seg_frames_before_transition, = numpy.where(numpy.array(seg_frames_before_transition_List)==self.transition_merge_frame_reference)
        emb_indx_with_max_seg_frames_after_transition, = numpy.where(numpy.array(seg_frames_after_transition_List)==max(seg_frames_after_transition_List))
        # record-analysed-data 
        indv_emb_piv_not_alligned,indv_emb_piv_alligned_List,full_apical_myo_raw_List,full_apical_myo_alligned_List,pos_piv_raw_List,pos_piv_alligned_List,pos_apical_myo_raw_List,pos_apical_myo_alligned_List = [[item] if numpy.array(item).ndim == 1 else item for item in [indv_emb_piv_not_alligned,indv_emb_piv_alligned_List,full_apical_myo_raw_List,full_apical_myo_alligned_List,pos_piv_raw_List,pos_piv_alligned_List,pos_apical_myo_raw_List,pos_apical_myo_alligned_List]] 
        self.ANIMALS = animal_List
        self.pos_piv_not_alligned = pos_piv_raw_List
        self.pos_piv_alligned = pos_piv_alligned_List
        self.indv_emb_piv_alligned = indv_emb_piv_alligned_List
        self.indv_emb_piv_not_alligned = indv_emb_piv_not_alligned
        self.pos_apical_myo_not_alligned = pos_apical_myo_raw_List
        self.pos_apical_myo_alligned = pos_apical_myo_alligned_List
        self.full_apical_myo_not_alligned = full_apical_myo_raw_List
        self.full_apical_myo_alligned = full_apical_myo_alligned_List
        self.frames_offSet_back_front = frames_offSet_back_front_List
        self.transition_indiv_frame_reference = seg_frames_before_transition_List
        self.pos_avg_emb_piv_not_alligned = [numpy.ma.mean(pos_piv_raw_List,axis=0),numpy.ma.std(pos_piv_raw_List,axis=0)] 
        self.pos_avg_emb_piv_alligned = [numpy.ma.mean(pos_piv_alligned_List,axis=0),numpy.ma.std(pos_piv_alligned_List,axis=0)]
        self.full_avg_emb_piv_alligned = [numpy.ma.mean(indv_emb_piv_alligned_List,axis=0),numpy.ma.std(indv_emb_piv_alligned_List,axis=0)]
        self.full_avg_emb_piv_not_alligned = [numpy.ma.mean(indv_emb_piv_not_alligned,axis=0),numpy.ma.std(indv_emb_piv_not_alligned,axis=0)]
        self.myo_frames_alligned,self.mid_markers_alligned = [item_bf[emb_indx_with_max_seg_frames_before_transition[0]] + item_af[emb_indx_with_max_seg_frames_after_transition[0]] for item_bf,item_af in zip([myo_frames_before_transition,mid_markers_before_transition],[myo_frames_after_transition,mid_markers_after_transition])]
        ##############
        # ouput-data #
        ##############
        # all-animals-frames-data (masked)
        all_animals_frames_data = numpy.ma.array([numpy.ma.array([inOutTools.masked_data(item,array_shift=[[0,0] for _ in range(len(item))],matrix_shift=self.frames_offSet_back_front[indx]) if item.shape[0] > 1 else [inOutTools.masked_data(item,array_shift=[[0,0] for _ in range(len(item))],matrix_shift=self.frames_offSet_back_front[indx])] for item in inputData_GROUPED]) for indx,inputData_GROUPED in enumerate(numpy.ma.array(all_animals_frames_data))]) 
        all_frames_animals_data = numpy.ma.swapaxes(numpy.ma.swapaxes(all_animals_frames_data,1,2),0,1)
        # loop-over-time
        time_List = []
        myo_frames_List = []
        mid_markers_List = []
        measurables_frames_data_avg = []
        measurables_frames_data_std = []
        for frame_counter,frames_data in enumerate(all_frames_animals_data):
            measurables_List = []
            # loop-over-animals
            for emb_counter,animal_data in enumerate(frames_data): 
                e_h,curv,s,piv_tan,piv_norm,u_dis_tan,basal_myo,apical_myo = animal_data 
                total_myo = apical_myo + basal_myo      
                mom = 0.5*e_h*(apical_myo-basal_myo)
                basal_mom = 0.5*e_h*basal_myo
                apical_mom = 0.5*e_h*apical_myo
                # gradients 
                momGrad = inOutTools.gradients_of_data(s,mom,uniform_sampling=True,closed=True)
                curvGrad = inOutTools.gradients_of_data(s,curv,uniform_sampling=True,closed=True) 
                total_myoGrad = inOutTools.gradients_of_data(s,total_myo,uniform_sampling=True,closed=True)
                basal_myoGrad = inOutTools.gradients_of_data(s,basal_myo,uniform_sampling=True,closed=True)
                apical_myoGrad = inOutTools.gradients_of_data(s,apical_myo,uniform_sampling=True,closed=True) 
                measurables_List.append([s,e_h,mom,curv,piv_tan,u_dis_tan,e_h*curv,piv_norm,total_myo,basal_myo,apical_myo,mom*curvGrad,curv*momGrad,total_myoGrad,basal_myoGrad,apical_myoGrad,basal_mom*curvGrad,curv*basal_myoGrad,apical_mom*curvGrad,curv*apical_myoGrad])
            measurables_avg,measurables_std = inOutTools.calculate_masked_avg_std(numpy.ma.swapaxes(measurables_List,0,1))
            measurables_frames_data_avg.append(measurables_avg)
            measurables_frames_data_std.append(measurables_std)
            time_List.append(frame_counter*self.time_between_frames)
            myo_frames_List.append(self.myo_frames_alligned[frame_counter])
            mid_markers_List.append(self.mid_markers_alligned[frame_counter])
        ########################
        # record-analysed-data #
        ########################
        self.time_List = time_List
        self.myo_frames_List = myo_frames_List
        self.mid_markers_List = mid_markers_List   
        self.s_time_series,self.eh_time_series,self.mom_time_series,self.curv_time_series,self.piv_tan_time_series,self.u_dis_tan_time_series,self.eh_curv_time_series,self.piv_norm_time_series,self.total_myo_time_series,self.basal_myo_time_series,self.apical_myo_time_series,self.mom_curvGrad_time_series,self.curv_momGrad_time_series,self.total_myoGrad_time_series,self.basal_myoGrad_time_series,self.apical_myoGrad_time_series,self.basal_mom_curvGrad_time_series,self.curv_basal_myoGrad_time_series,self.apical_mom_curvGrad_time_series,self.curv_apical_myoGrad_time_series = numpy.ma.swapaxes(measurables_frames_data_avg,0,1)
        self.s_std_time_series,self.eh_std_time_series,self.mom_std_time_series,self.curv_std_time_series,self.piv_tan_std_time_series,self.u_dis_tan_std_time_series,self.eh_curv_std_time_series,self.piv_norm_std_time_series,self.total_myo_std_time_series,self.basal_myo_std_time_series,self.apical_myo_std_time_series,self.mom_curvGrad_std_time_series,self.curv_momGrad_std_time_series,self.total_myoGrad_std_time_series,self.basal_myoGrad_std_time_series,self.apical_myoGrad_std_time_series,self.basal_mom_curvGrad_std_time_series,self.curv_basal_myoGrad_std_time_series,self.apical_mom_curvGrad_std_time_series,self.curv_apical_myoGrad_std_time_series = numpy.ma.swapaxes(measurables_frames_data_std,0,1)
        
        return

    ####################
    # analyze-genotype #
    ####################
    def analyze_GENOTYPE(self,sysID,img_channels,seg_img_channel,frameIndex_Maps,parametersFileName,moviePath):
        print('genotype(analyzing):',sysID)
        # parameters 
        frameSequences_Maps = {}
        for animal_ID,frameIndex_Map in frameIndex_Maps.items():
            frameIndex_Map = inOutTools.list_flatten_2D(frameIndex_Map)
            frameSequences_Maps[animal_ID] = inOutTools.read_image_frame(moviePath+'/'+sysID+'/'+animal_ID,img_channels,seg_img_channel,frameIndex_Map[3:5])
        self.ID = sysID
        self.moviePath = moviePath   
        self.processAnimals_GENOTYPE(frameSequences_Maps,frameIndex_Maps,parametersFileName,moviePath+'/'+sysID)
        
        return 
    
    #################
    # visualization #
    #################
    def view_GENOTYPE(self,parametersFileName,viewAnimals,pixel_to_micron_conversion_factor,time_steps,figFormat):
        print('genotype(visualizing):',self.ID)
        path = self.moviePath +'/' + self.ID + '/' + 'plot_avg'
        inOutTools.recreateDirectory(path)
        # load-parameters
        parameters = inOutTools.read_parameter_file(parametersFileName)
        #**************#
        # temporal-piv #
        #**************#
        FIG_piv_phase_sep, FIG_piv_phase_sep_axes = plt.subplots(2,4,figsize = (10,3))
        piv_raw_ax,piv_all_ax,piv_sym_ax,piv_asym_ax = FIG_piv_phase_sep_axes[0]
        piv_raw_avg_ax,piv_alligned_avg_ax,piv_sym_avg_ax,piv_asym_avg_ax = FIG_piv_phase_sep_axes[1] 
        transition_time = self.transition_merge_frame_reference*self.time_between_frames
        #-----------------------------#
        # PIV-individual-over-animals #
        #-----------------------------#
        animalTypes = numpy.array([animal.ID for animal in self.ANIMALS])
        full_avg_emb_piv_not_alligned,full_avg_emb_piv_alligned = [[numpy.array(ele)*pixel_to_micron_conversion_factor for ele in item] for item in [self.full_avg_emb_piv_not_alligned,self.full_avg_emb_piv_alligned]]
        for emb_counter,(piv_all_raw,piv_all_alligned) in enumerate(zip(self.indv_emb_piv_not_alligned,self.indv_emb_piv_alligned)):
            # unit-conversion
            piv_all_raw,piv_all_alligned = [ele*pixel_to_micron_conversion_factor for ele in [piv_all_raw,piv_all_alligned]]
            # piv-not-alligned
            time_raw = [indx*self.time_between_frames for indx in range(len(piv_all_raw))]
            piv_raw_ax.plot(time_raw,piv_all_raw,c=colorsList[emb_counter],ls = '-', lw = 0.5, marker = 'o',ms = 2.0,label=animalTypes[emb_counter])
            piv_raw_ax.axvline(self.transition_indiv_frame_reference[emb_counter]*self.time_between_frames,c=colorsList[emb_counter],alpha = 0.3,ls='--',lw = 1.0)
            # piv-alligned 
            time_all = [indx*self.time_between_frames-transition_time for indx in range(len(piv_all_alligned))]
            piv_all_ax.plot(time_all,piv_all_alligned,c=colorsList[emb_counter],ls = '-', lw = 0.5, marker = 'o',ms = 2.0,label=animalTypes[emb_counter])
            # piv-sym
            piv_sym = piv_all_alligned[:self.transition_merge_frame_reference+1]
            time_sym = [indx*self.time_between_frames-transition_time for indx in range(len(piv_sym))]
            piv_sym_ax.plot(time_sym,piv_sym,c=colorsList[emb_counter],ls = '-', lw = 0.5, marker = 'o',ms = 2.0,label=animalTypes[emb_counter])
            # piv-asym
            piv_asym = piv_all_alligned[self.transition_merge_frame_reference:]
            time_asym = [indx*self.time_between_frames for indx in range(len(piv_asym))]
            piv_asym_ax.plot(time_asym,piv_asym,c=colorsList[emb_counter],ls = '-', lw = 0.5, marker = 'o',ms = 2.0,label=animalTypes[emb_counter])
        # sym-asym-transition-reference 
        piv_all_ax.axvline(0.0,c='k',alpha = 0.3,ls='--',lw = 1.0)
        for axis_counter,axis in enumerate([piv_raw_ax,piv_all_ax,piv_sym_ax,piv_asym_ax]): 
            inOutTools.customize_axis(axis,xlim=[],ylim=[],x_pad=0.0,leg_loc=2,leg_size=2,hline_pos=0.0,vline_pos=0.0,tick_size=20)
        #--------------------------#
        # PIV-average-over-animals #
        #--------------------------#
        # unit-conversion
        full_avg_emb_piv_not_alligned,full_avg_emb_piv_alligned,pos_avg_emb_piv_alligned,full_avg_emb_piv_alligned = [[numpy.array(ele)*pixel_to_micron_conversion_factor for ele in item] for item in [self.full_avg_emb_piv_not_alligned,self.full_avg_emb_piv_alligned,self.pos_avg_emb_piv_alligned,self.full_avg_emb_piv_alligned]]
        for emb_counter,(piv_all_raw,piv_all_alligned) in enumerate(zip([full_avg_emb_piv_not_alligned],[full_avg_emb_piv_alligned])): 
            # piv-not-alligned
            piv_avg, piv_std = piv_all_raw
            time_avg = numpy.ma.array([item*self.time_between_frames for item in range(piv_avg.size)]) 
            piv_raw_avg_ax.plot(time_avg,piv_avg,c = 'k', ls  = '-', marker = 'o', ms = 2.0, lw = 0.5,zorder=1,label='animal average') 
            piv_raw_avg_ax.fill_between(time_avg,piv_avg-piv_std,piv_avg+piv_std,facecolor='k',alpha= 0.3)
            # piv-alligned
            piv_avg, piv_std = piv_all_alligned
            time_avg = numpy.ma.array([item*self.time_between_frames for item in range(piv_avg.size)]) 
            piv_alligned_avg_ax.plot(time_avg-transition_time,piv_avg,c = 'k', ls  = '-', marker = 'o', ms = 2.0, lw = 0.5,zorder=1,label='animal average') 
            piv_alligned_avg_ax.fill_between(time_avg-transition_time,piv_avg-piv_std,piv_avg+piv_std,facecolor='k',alpha= 0.3)
            # piv-sym
            piv_avg, piv_std = [item[:self.transition_merge_frame_reference+1] for item in piv_all_alligned]
            time_avg = numpy.ma.array([item*self.time_between_frames for item in range(piv_avg.size)]) 
            piv_sym_avg_ax.plot(time_avg-transition_time,piv_avg,c = 'k', ls  = '-', marker = 'o', ms = 2.0, lw = 0.5,zorder=1,label='animal average') 
            piv_sym_avg_ax.fill_between(time_avg-transition_time,piv_avg-piv_std,piv_avg+piv_std,facecolor='k',alpha= 0.3)
            # piv-asym
            piv_avg, piv_std = [item[self.transition_merge_frame_reference:] for item in piv_all_alligned]
            time_avg = numpy.ma.array([item*self.time_between_frames for item in range(piv_avg.size)]) 
            piv_asym_avg_ax.plot(time_avg,piv_avg,c = 'k', ls  = '-', marker = 'o', ms = 2.0, lw = 0.5,zorder=1,label='animal average') 
            piv_asym_avg_ax.fill_between(time_avg,piv_avg-piv_std,piv_avg+piv_std,facecolor='k',alpha= 0.3)
        piv_alligned_avg_ax.axvline(0.0,c='k',alpha = 0.3,ls='--',lw = 1.0)    
        for axis_counter,axis in enumerate([piv_raw_avg_ax,piv_alligned_avg_ax,piv_sym_avg_ax,piv_asym_avg_ax,piv_raw_ax,piv_all_ax,piv_sym_ax,piv_asym_ax]): 
             inOutTools.customize_axis(axis,xlim=[],ylim=[],x_pad=0.0,leg_loc=2,leg_size=3,hline_pos=0.0,vline_pos=0.0,tick_size=5)
        FIG_piv_phase_sep.savefig(path +'/FIG_steps_of_allign.' + figFormat, format = figFormat, figsize=(10, 3), dpi = 500,bbox_inches ='tight',pad_inches = 0)
        plt.close(FIG_piv_phase_sep)
        #----------------------------#
        # piv-avg: full-vs-posterior #
        #----------------------------#
        FIG_piv_full_pos,full_pos_ax = plt.subplots(1,1,figsize = (2.6,1.7))
        # full
        piv_avg,piv_std  = pos_avg_emb_piv_alligned
        pos_time = numpy.ma.array([item*self.time_between_frames for item in range(piv_avg.size)])
        full_pos_ax.plot(pos_time-transition_time,piv_avg,c = 'r', ls  = '-', lw = 1,zorder=1,label='posterior-epithelium')  
        full_pos_ax.fill_between(pos_time-transition_time,piv_avg-piv_std,piv_avg+piv_std,facecolor='r',alpha= 0.3)
        # posterior
        piv_avg,piv_std  = full_avg_emb_piv_alligned
        full_time = numpy.ma.array([item*self.time_between_frames for item in range(piv_avg.size)])
        full_pos_ax.plot(full_time-transition_time,piv_avg,c = 'k', ls  = '-', lw = 1,zorder=1,label='full-epithelium') 
        full_pos_ax.fill_between(full_time-transition_time,piv_avg-piv_std,piv_avg+piv_std,facecolor='k',alpha= 0.3)
        # axis-atributes
        inOutTools.customize_axis(full_pos_ax,xlim=[],ylim=[],x_pad=0.0,leg_loc=2,leg_size=3,hline_pos=0.0,vline_pos=0.0,tick_size=5)
        FIG_piv_full_pos.savefig(path +'/FIG_piv_full_vs_pos' + '.' + figFormat,format = figFormat, figsize=(10, 3), dpi = 500,bbox_inches ='tight',pad_inches = 0.01)
        plt.close(FIG_piv_full_pos)
        #*************#
        # spatial-piv #
        #*************#
        time_List = numpy.array(self.time_List)-transition_time if not time_steps else numpy.array(time_steps)
        time_Indices = numpy.array([item*2 for item in time_List],int) + self.transition_merge_frame_reference
        s_avg_List,piv_tan_avg_List,piv_tan_std_List,u_dis_tan_avg_List,u_dis_tan_std_List = [numpy.array(item)[time_Indices] for item in [self.s_time_series,self.piv_tan_time_series,self.piv_tan_std_time_series,self.u_dis_tan_time_series,self.u_dis_tan_std_time_series]]
        # unit-conversion
        s_avg_List,piv_tan_avg_List,piv_tan_std_List,u_dis_tan_avg_List,u_dis_tan_std_List = [numpy.array([numpy.array(ele)*pixel_to_micron_conversion_factor for ele in item]) for item in [s_avg_List,piv_tan_avg_List,piv_tan_std_List,u_dis_tan_avg_List,u_dis_tan_std_List]]
        v_lim,u_lim = [[numpy.amin(piv_tan_avg_List-piv_tan_std_List),numpy.amax(piv_tan_avg_List+piv_tan_std_List)],[numpy.amin(u_dis_tan_avg_List-u_dis_tan_std_List),numpy.amax(u_dis_tan_avg_List+u_dis_tan_std_List)]]
        FIG_all_time, (ax_v,ax_u)  = plt.subplots(1,2,figsize=(5,2))
        for time_indx,(t,s,piv_avg,piv_std,u_avg,u_std) in enumerate(zip(time_List,s_avg_List,piv_tan_avg_List,piv_tan_std_List,u_dis_tan_avg_List,u_dis_tan_std_List)):
            s_ref = s-s[self.spatial_shift_by_node_index]
            ax_v.plot(s_ref,piv_avg, lw=1.0, c = colorsList[time_indx], ls='-')
            ax_u.plot(s_ref,u_avg, lw=1.0, c = colorsList[time_indx], ls='-') 
            if parameters['view_indv_times']:
                FIG, (v_ax,u_ax)  = plt.subplots(1, 2, figsize=(8,2))
                for axis_counter,(axis,axis_lim,meas_avg,meas_std) in enumerate(zip([v_ax,u_ax],[v_lim,u_lim],[piv_avg,u_avg],[piv_std,u_std])):
                    axis.plot(s_ref,meas_avg, c='k',lw=1.0, ls='-')
                    axis.fill_between(s_ref,meas_avg-meas_std,meas_avg+meas_std, facecolor='k', alpha=0.3)
                    inOutTools.customize_axis(axis,xlim=[],ylim=[],x_pad=0.0,leg_loc=2,leg_size=0.0,hline_pos=0.0,vline_pos=0.0,tick_size=5)
                FIG.savefig(path + '/Measurables_' + str(t) + '.' + figFormat, format = figFormat, figsize=(10, 3), dpi=500, bbox_inches='tight', pad_inches=0.05)
                plt.close(FIG)
        for axis in [ax_v,ax_u]:
            inOutTools.customize_axis(axis,xlim=[],ylim=[],x_pad=0.0,leg_loc=2,leg_size=0.0,hline_pos=0.0,vline_pos=0.0,tick_size=5)
        FIG_all_time.savefig(path + '/measurables_all_time' + '.' + figFormat, format = figFormat, figsize=(10, 3), dpi=500, bbox_inches='tight', pad_inches=0.05)
        plt.close(FIG_all_time) 
        #*********#
        # animals #
        #*********#
        if viewAnimals:
            for embryo_counter,EMBRYO in enumerate(self.ANIMALS):
                print('----------------------------')
                EMBRYO.view_ANIMAL(parametersFileName=parametersFileName,pixel_to_micron_conversion_factor=pixel_to_micron_conversion_factor,figFormat='png') 
        return
    
    ########
    # save #
    ########  
    def save(self,dataPath,fileName):
        inOutTools.createDirectory(dataPath)
        inOutTools.dump_data_via_pickle(dataPath+'/'+fileName+'_'+self.ID,self)
        
        return

#======================================================================================================#
#                                         class: System1D                                            #
#======================================================================================================#

class System1D:
    
    #######################
    # initialize-genotype #
    #######################
    def __init__(self,*args,**kwarg):    

        return
    
    ##################
    # analyze-system #
    ##################
    def analyze_SYSTEM(self,movieParameters):
        print('genotype(analyzing) ...')
        GENOTYPES_DICT = {}
        for gen_ID in movieParameters['Genotypes']: 
            print('--------------------------------------')
            GENOTYPE = Genotype1D()
            GENOTYPE.analyze_GENOTYPE(sysID=gen_ID,img_channels=movieParameters['img_channels'],seg_img_channel=movieParameters['seg_img_channel'],frameIndex_Maps=movieParameters['frameIndex_Map'][gen_ID],parametersFileName=movieParameters['analysisParametersFile'],moviePath=movieParameters['moviePath']) 
            GENOTYPES_DICT.update({gen_ID:GENOTYPE})
        self.GENOTYPES = GENOTYPES_DICT
        self.sysPath = movieParameters['moviePath']
    
    #################
    # visualization #
    #################
    def view_SYSTEM(self,movieParameters,viewGenotypes,viewAnimals,time_steps,pixel_to_micron_conversion_factor,figFormat):
        FIG_avg_piv, avg_piv_axes = plt.subplots(2,2,figsize = (5,3))
        avg_piv_axes_not_alligned_ax,avg_piv_axes_alligned_ax = avg_piv_axes[0] 
        pos_avg_piv_axes_not_alligned_ax,pos_avg_piv_axes_alligned_ax = avg_piv_axes[1] 
        for gen_counter,(gen_ID,GENOTYPE) in enumerate(self.GENOTYPES.items()): 
            transition_time = GENOTYPE.transition_merge_frame_reference*GENOTYPE.time_between_frames
            # unit-conversion
            full_avg_emb_piv_not_alligned,full_avg_emb_piv_alligned,pos_avg_emb_piv_not_alligned,pos_avg_emb_piv_alligned = [[numpy.array(ele)*pixel_to_micron_conversion_factor for ele in item] for item in [GENOTYPE.full_avg_emb_piv_not_alligned,GENOTYPE.full_avg_emb_piv_alligned,GENOTYPE.pos_avg_emb_piv_not_alligned,GENOTYPE.pos_avg_emb_piv_alligned]]
            ################################
            # temporal-piv:full-arc-length #
            ################################
            # piv-not-alligned
            piv_avg, piv_std = full_avg_emb_piv_not_alligned
            time_avg = numpy.ma.array([item*GENOTYPE.time_between_frames for item in range(piv_avg.size)]) 
            avg_piv_axes_not_alligned_ax.plot(time_avg,piv_avg,c = colorsList[gen_counter], ls  = '-', marker = 'o', ms = 2.0, lw = 0.5,zorder=1,label=gen_ID) 
            avg_piv_axes_not_alligned_ax.fill_between(time_avg,piv_avg-piv_std,piv_avg+piv_std,facecolor=colorsList[gen_counter],alpha= 0.3)
            # piv-alligned
            piv_avg, piv_std = full_avg_emb_piv_alligned
            time_avg = numpy.ma.array([item*GENOTYPE.time_between_frames for item in range(piv_avg.size)])
            avg_piv_axes_alligned_ax.plot(time_avg-transition_time,piv_avg,c = colorsList[gen_counter], ls  = '-', marker = 'o', ms = 2.0, lw = 0.5,zorder=1,label=gen_ID) 
            avg_piv_axes_alligned_ax.fill_between(time_avg-transition_time,piv_avg-piv_std,piv_avg+piv_std,facecolor=colorsList[gen_counter],alpha= 0.3)
            #####################################
            # temporal-piv:posterior-arc-length #
            #####################################
            # piv-not-alligned
            piv_avg,piv_std  = pos_avg_emb_piv_not_alligned
            pos_time = numpy.ma.array([item*GENOTYPE.time_between_frames for item in range(piv_avg.size)])
            pos_avg_piv_axes_not_alligned_ax.plot(pos_time,piv_avg,c = colorsList[gen_counter], ls  = '-', marker = 'o', ms = 2.0, lw = 0.5,zorder=1,label=gen_ID)  
            pos_avg_piv_axes_not_alligned_ax.fill_between(pos_time,piv_avg-piv_std,piv_avg+piv_std,facecolor=colorsList[gen_counter],alpha= 0.3)
            # piv-alligned
            piv_avg,piv_std  = pos_avg_emb_piv_alligned
            pos_time = numpy.ma.array([item*GENOTYPE.time_between_frames for item in range(piv_avg.size)])
            pos_avg_piv_axes_alligned_ax.plot(pos_time-transition_time,piv_avg,c = colorsList[gen_counter], ls  = '-', marker = 'o', ms = 2.0, lw = 0.5,zorder=1,label=gen_ID)  
            pos_avg_piv_axes_alligned_ax.fill_between(pos_time-transition_time,piv_avg-piv_std,piv_avg+piv_std,facecolor=colorsList[gen_counter],alpha= 0.3)     
            #***********#
            # genotypes #
            #***********#
            if viewGenotypes:
                print('===============================')
                GENOTYPE.view_GENOTYPE(parametersFileName=movieParameters['plotParametersFile'],viewAnimals=viewAnimals,pixel_to_micron_conversion_factor=pixel_to_micron_conversion_factor,time_steps=time_steps,figFormat='png')
        for axis_counter,axis in enumerate([avg_piv_axes_not_alligned_ax,avg_piv_axes_alligned_ax,pos_avg_piv_axes_not_alligned_ax,pos_avg_piv_axes_alligned_ax]): 
             inOutTools.customize_axis(axis,xlim=[],ylim=[],x_pad=0.0,leg_loc=2,leg_size=2,hline_pos=0.0,vline_pos=0.0,tick_size=5)
        # save-figure
        figName = self.sysPath  + '/FIG_avg_piv' + '.' + figFormat
        FIG_avg_piv.savefig(figName,format = figFormat, figsize=(10, 3), dpi = 500, bbox_inches='tight', pad_inches=0.01)
        plt.close(FIG_avg_piv)  
        
        return
        
    ##########
    # t-test #
    ##########
    def t_TEST(self,genotypes,bin_size,time_steps,pixel_to_micron_conversion_factor,figFormat): 
        print('--------------------------------')
        print('t-test in progress ...')
        # system-check
        for item in genotypes:
            if item not in self.GENOTYPES:
                print('genotype:',item,'does NOT EXIST !!!')
                inOutTools.terminate()
            else:
                pass
        # t-test 
        time_indices = []
        time_indices_all = []
        animal_genotype_s = []
        animal_genotype_frames = []
        animal_genotype_piv_tan = []
        for gen_counter,gen_ID in enumerate(genotypes):
            GENOTYPE = self.GENOTYPES[gen_ID]
            transition_time = GENOTYPE.transition_merge_frame_reference*GENOTYPE.time_between_frames
            time_indices.append(numpy.array([item*2 for item in numpy.array(time_steps)],int) + GENOTYPE.transition_merge_frame_reference)
            time_indices_all.append(numpy.array([item*2 for item in numpy.array(GENOTYPE.time_List)-transition_time],int) + GENOTYPE.transition_merge_frame_reference)
            animal_genotype_s.append(numpy.array([numpy.array(animal.s_frames) for animal in GENOTYPE.ANIMALS]))
            animal_genotype_piv_tan.append(numpy.array([numpy.array(animal.piv_tan_frames) for animal in GENOTYPE.ANIMALS]))
            animal_genotype_frames.append(numpy.array([piv_tan_frame.shape[0] for piv_tan_frame in animal_genotype_piv_tan[-1]]))
        p_val_piv_tan = None
        p_val_piv_tan_sp_avg = None
        if len(animal_genotype_frames) == 2:
            print('-> two-sided-t-test')
            shift_time_indices = [[[0,max(inOutTools.flatten_List(animal_genotype_frames)) - ele] for ele in item] for item in animal_genotype_frames]
            # temporal-(spatially-averaged)-profile
            time_indices_all = numpy.arange(0,min([max(ele) for ele in time_indices_all])+1)
            animal_genotype_piv_tan_sp_avg = numpy.array([numpy.array([numpy.array([numpy.array([inOutTools.area_under_curve(s,piv_tan,closed=False)/s[-1]]) for piv_tan,s in zip(item_piv_tan,item_s)]) for item_piv_tan,item_s in zip(item_gen_piv_tan,item_gen_s)]) for item_gen_piv_tan,item_gen_s in zip(animal_genotype_piv_tan,animal_genotype_s)])
            ANIMALS_g1_piv_tan_sp_avg,ANIMALS_g2_piv_tan_sp_avg = [numpy.ma.array([numpy.ma.array(inOutTools.masked_data(animal,array_shift=[],matrix_shift=shift_indx)) for animal,shift_indx in zip(item,indx)]) for item,indx in zip(animal_genotype_piv_tan_sp_avg,shift_time_indices)] 
            ANIMALS_g1_piv_tan_sp_avg,ANIMALS_g2_piv_tan_sp_avg = [numpy.ma.array([numpy.ma.array([numpy.ma.array(piv_tan_time_stamp[time_index]) for piv_tan_time_stamp in animal_g_piv_tan]) for time_index in time_Index_g]) for animal_g_piv_tan,time_Index_g in zip([ANIMALS_g1_piv_tan_sp_avg,ANIMALS_g2_piv_tan_sp_avg],numpy.tile(time_indices_all,(2,1)))] 
            p_val_piv_tan_sp_avg = inOutTools.flatten_List([[inOutTools.compute_p_value_two_sample(numpy.ma.array(e1),numpy.ma.array(e2),symmetry='two-sided',equal_var=False) for e1,e2 in zip(numpy.ma.array(animal_g1_piv_tan.T),numpy.ma.array(animal_g2_piv_tan.T))] for animal_g1_piv_tan,animal_g2_piv_tan in zip(ANIMALS_g1_piv_tan_sp_avg,ANIMALS_g2_piv_tan_sp_avg)])
            # spatial-profile
            ANIMALS_g1_piv_tan,ANIMALS_g2_piv_tan = [numpy.ma.array([numpy.ma.array(inOutTools.masked_data(animal,array_shift=[],matrix_shift=shift_indx)) for animal,shift_indx in zip(item,indx)]) for item,indx in zip(numpy.ma.array(animal_genotype_piv_tan),shift_time_indices)] 
            ANIMALS_g1_piv_tan,ANIMALS_g2_piv_tan = [numpy.ma.array([numpy.ma.array([numpy.ma.array(piv_tan_time_stamp[time_index]).reshape(-1,bin_size).mean(axis=1) for piv_tan_time_stamp in animal_g_piv_tan]) for time_index in time_Index_g]) for animal_g_piv_tan,time_Index_g in zip([ANIMALS_g1_piv_tan,ANIMALS_g2_piv_tan],time_indices)]
            p_val_piv_tan = [[inOutTools.compute_p_value_two_sample(numpy.ma.array(e1),numpy.ma.array(e2),symmetry='two-sided',equal_var=False) for e1,e2 in zip(numpy.ma.array(animal_g1_piv_tan.T),numpy.ma.array(animal_g2_piv_tan.T))] for animal_g1_piv_tan,animal_g2_piv_tan in zip(ANIMALS_g1_piv_tan,ANIMALS_g2_piv_tan)]
        else:
            print('-> one-sided-t-test')
            shift_time_indices = [[0,max(animal_genotype_frames[0]) - ele] for ele in animal_genotype_frames[0]]
            # temporal-(spatially-averaged)-profile
            time_indices_all = numpy.arange(0,min([max(ele) for ele in time_indices_all])+1)
            animal_genotype_piv_tan_sp_avg = numpy.array([numpy.array([numpy.array([inOutTools.area_under_curve(s,piv_tan,closed=False)/s[-1]]) for piv_tan,s in zip(item_piv_tan,item_s)]) for item_piv_tan,item_s in zip(animal_genotype_piv_tan[0],animal_genotype_s[0])])
            ANIMALS_g_piv_tan_sp_avg = numpy.ma.array([numpy.ma.array(inOutTools.masked_data(animal,array_shift=[],matrix_shift=shift_indx)) for animal,shift_indx in zip(animal_genotype_piv_tan_sp_avg,shift_time_indices)])
            ANIMALS_g_piv_tan_sp_avg = numpy.ma.array([numpy.ma.array([numpy.ma.array(piv_tan_time_stamp[time_index]) for piv_tan_time_stamp in ANIMALS_g_piv_tan_sp_avg]) for time_index in time_indices_all])
            p_val_piv_tan_sp_avg = inOutTools.flatten_List(numpy.array([inOutTools.compute_p_value_one_sample(numpy.ma.array(e),ref_val=0.0,symmetry='greater') for e in numpy.ma.array(ANIMALS_g_piv_tan_sp_avg.T)]))
            # spatail-profile
            ANIMALS_g_piv_tan = numpy.ma.array([numpy.ma.array(inOutTools.masked_data(animal,array_shift=[],matrix_shift=shift_indx)) for animal,shift_indx in zip(animal_genotype_piv_tan[0],shift_time_indices)])
            ANIMALS_g_piv_tan = numpy.ma.array([numpy.ma.array([numpy.ma.array(piv_tan_time_stamp[time_index]).reshape(-1,bin_size).mean(axis=1) for piv_tan_time_stamp in ANIMALS_g_piv_tan]) for time_index in time_indices[0]])
            p_val_piv_tan = [[inOutTools.compute_p_value_one_sample(numpy.ma.array(e),ref_val=0.0,symmetry='greater') for e in numpy.ma.array(animal_g_piv_tan.T)] for animal_g_piv_tan in ANIMALS_g_piv_tan]
        # plot-t-test
        time_avg = None
        FIG_p_val,piv_ax = plt.subplots(1,1,figsize=(2.6,1.3))
        for gen_counter,gen_ID in enumerate(genotypes): 
            transition_time = GENOTYPE.transition_merge_frame_reference*GENOTYPE.time_between_frames
            # piv-alligned
            piv_avg, piv_std = [ele[time_indices_all] for ele in self.GENOTYPES[gen_ID].full_avg_emb_piv_alligned]
            time_avg = numpy.ma.array([item*GENOTYPE.time_between_frames for item in range(piv_avg.size)]) - transition_time
            piv_ax.plot(time_avg,piv_avg,c = colorsList[gen_counter], ls  = '-', marker = 'o', ms = 2.0, lw = 0.5,zorder=1,label=gen_ID) 
            piv_ax.fill_between(time_avg,piv_avg-piv_std,piv_avg+piv_std,facecolor=colorsList[gen_counter],alpha= 0.3)
        inOutTools.add_significance_bar(piv_ax,numpy.array(time_avg),numpy.nan_to_num(numpy.array(p_val_piv_tan_sp_avg),nan=0.0)<0.05)  
        inOutTools.customize_axis(piv_ax,xlim=[],ylim=[],x_pad=0.0,leg_loc=1,leg_size=3,hline_pos=0.0,vline_pos=0.0,tick_size=5)
        # save-plot
        figName = self.sysPath  + '/FIG_p_val_piv_avg.' + figFormat
        FIG_p_val.savefig(figName,format = figFormat, figsize=(10, 3), dpi = 500, bbox_inches='tight', pad_inches=0.01)
        plt.close(FIG_p_val) 
        for indx,(t,p_val) in enumerate(zip(time_steps,p_val_piv_tan)):
            FIG_p_val,piv_ax = plt.subplots(1,1,figsize=(2.6,1.3))
            s = None
            for gen_counter,gen_ID in enumerate(genotypes): 
                time_Index = int(2*t) + GENOTYPE.transition_merge_frame_reference
                s,v_avg,v_std = [self.GENOTYPES[gen_ID].s_time_series[time_Index],self.GENOTYPES[gen_ID].piv_tan_time_series[time_Index],self.GENOTYPES[gen_ID].piv_tan_std_time_series[time_Index]]
                # unit-converion
                s,v_avg,v_std = [ele*pixel_to_micron_conversion_factor for ele in [s,v_avg,v_std]]
                s = s/s[-1]
                s = s-s[self.GENOTYPES[gen_ID].spatial_shift_by_node_index]
                piv_ax.plot(s,v_avg, c=colorsList[gen_counter],lw=1.0, ls='-',label=gen_ID)
                piv_ax.fill_between(s,v_avg-v_std,v_avg+v_std, facecolor=colorsList[gen_counter], alpha=0.3)
            inOutTools.add_significance_bar(piv_ax,numpy.array(s).reshape(-1,bin_size).mean(axis=1),numpy.nan_to_num(numpy.array(p_val))<0.05)  
            inOutTools.customize_axis(piv_ax,xlim=[],ylim=[],x_pad=0.0,leg_loc=1,leg_size=3,hline_pos=0.0,vline_pos=0.0,tick_size=5)
            # save-plot
            figName =  self.sysPath + '/FIG_p_val_piv_' + str(t) + '.' + figFormat
            FIG_p_val.savefig(figName,format = figFormat, figsize=(10, 3), dpi = 500, bbox_inches='tight', pad_inches=0.01)
            plt.close(FIG_p_val) 

        return
    
    ########
    # save #
    ########  
    def save(self,dataPath,fileName):
        inOutTools.createDirectory(dataPath)
        inOutTools.dump_data_via_pickle(dataPath+'/'+fileName+'_all',self)
        
        return
        
#======================================================================================================#
#                                         class: Fitting1D                                             #
#======================================================================================================#

class Fitting1D:
    
    ######################
    # initialize-fitting #
    ######################
    def __init__(self,*args,**kwarg):
   
        return
    
    ########################
    # process-fitting-data #
    ########################
    def process_fitting_data(self,inputData,fitting_parameters):   
        transition_merge_frame_reference,spatial_shift_by_node_index,full_avg_emb_piv_alligned_avg,full_avg_emb_piv_alligned_std,time_List,s_time_series,piv_tan_time_series,piv_tan_std_time_series,total_myoGrad_time_series,apical_myoGrad_time_series,basal_myoGrad_time_series,apical_mom_curvGrad_time_series,curv_apical_myoGrad_time_series,mom_curvGrad_time_series,curv_momGrad_time_series,basal_mom_curvGrad_time_series,curv_basal_myoGrad_time_series=inputData
        tmin,tmax = fitting_parameters['time_range']
        hypothesis = fitting_parameters['hypothesis']
        changingParameters = fitting_parameters['changingParameters']
        spatial_fitting_domain = fitting_parameters['fitting_domain']
        simultaneous_fitting = fitting_parameters['simultaneous_fitting'] 
        BOUNDARY_COND_SWITCH = fitting_parameters['BOUNDARY_COND_SWITCH']
        normalized_arc_length = fitting_parameters['normalized_arc_length']
        distinguish_myo_switch = fitting_parameters['distinguish_myo_switch']
        friction_domainSize,friction_domainLocation = fitting_parameters['friction_domainSize_domainLocation']
        viscosity_domainSize,viscosity_domainLocation = fitting_parameters['viscosity_domainSize_domainLocation']
        # parameter-formatting
        parameters_GUESS = {}
        parameters_FIXED = {}
        parameter_INDEXING = {}
        parameters_CONSTRAINT = {}
        for indx,(param_key,param_val) in enumerate(fitting_parameters['guess_parameters_Map'].items()):
            parameter_INDEXING.update({param_key:indx})
            parameters_GUESS.update({param_key:param_val['initial_value']})
            parameters_CONSTRAINT.update({param_key:param_val['constraint']})
            parameters_FIXED.update({} if param_val['fixed'] is None else {param_key:param_val['fixed']})
        initial_parameter = [[item] for item in list(parameters_GUESS.values())]
        # time-range-for-fitting
        time_range = numpy.arange(tmin,tmax+1)
        full_avg_emb_piv_alligned_avg,full_avg_emb_piv_alligned_std,time_List,s_time_series,piv_tan_time_series,piv_tan_std_time_series,total_myoGrad_time_series,apical_myoGrad_time_series,basal_myoGrad_time_series,apical_mom_curvGrad_time_series,curv_apical_myoGrad_time_series,mom_curvGrad_time_series,curv_momGrad_time_series,basal_mom_curvGrad_time_series,curv_basal_myoGrad_time_series = [numpy.array(item)[time_range+transition_merge_frame_reference] for item in  [full_avg_emb_piv_alligned_avg,full_avg_emb_piv_alligned_std,time_List,s_time_series,piv_tan_time_series,piv_tan_std_time_series,total_myoGrad_time_series,apical_myoGrad_time_series,basal_myoGrad_time_series,apical_mom_curvGrad_time_series,curv_apical_myoGrad_time_series,mom_curvGrad_time_series,curv_momGrad_time_series,basal_mom_curvGrad_time_series,curv_basal_myoGrad_time_series]]
        # normalize-epithelium
        if normalized_arc_length:
            total_myoGrad_time_series,apical_myoGrad_time_series,basal_myoGrad_time_series,curv_momGrad_time_series,mom_curvGrad_time_series,apical_mom_curvGrad_time_series,basal_mom_curvGrad_time_series,curv_basal_myoGrad_time_series,curv_apical_myoGrad_time_series = [numpy.array([ele*s[-1]*s[-1] for ele,s in zip(items,s_time_series)]) for items in [total_myoGrad_time_series,apical_myoGrad_time_series,basal_myoGrad_time_series,curv_momGrad_time_series,mom_curvGrad_time_series,apical_mom_curvGrad_time_series,basal_mom_curvGrad_time_series,curv_basal_myoGrad_time_series,curv_apical_myoGrad_time_series]]
            s_time_series = numpy.array([s/s[-1] for s in s_time_series]) 
        # reference-origin
        s_res_time_series = numpy.array([s-s[spatial_shift_by_node_index] for s in s_time_series])
        # heterogeneous-friction
        time_series_friction_star_ref = inOutTools.numpy.array([friction_domainLocation for time_frame in time_range])
        heteroGenFriction = numpy.array([inOutTools.rectangular_function(s, numpy.array([friction_center-friction_domainSize//2,friction_center+friction_domainSize//2])) for s, friction_center in zip(s_time_series,time_series_friction_star_ref)])
        # heterogeneous-viscosity
        time_series_viscosity_center_ref = inOutTools.numpy.array([viscosity_domainLocation  for time_frame in time_range])
        heteroGenViscosity = numpy.array([inOutTools.rectangular_function(s, numpy.array([viscosity_center-viscosity_domainSize//2,viscosity_center+viscosity_domainSize//2])) for s, viscosity_center in zip(s_time_series,time_series_viscosity_center_ref)])
        # hypothesis-initialization
        hetVisco_flag = 0 if viscosity_domainSize == 0 else 1
        curv_flag =  0 if (hypothesis == 'tension' or hypothesis == 'friction') else 1
        hetFric_flag = 0 if (hypothesis == 'tension' or hypothesis == 'curvature') else 1
        # strain-gradient
        strain_Grad = numpy.zeros_like(piv_tan_time_series)
        # input-data-for-fitting 
        eff_heteroGenFriction = hetFric_flag*heteroGenFriction 
        eff_heteroGenViscosity = hetVisco_flag*heteroGenViscosity
        model_INPUT_avg = [s_time_series,piv_tan_time_series,strain_Grad,total_myoGrad_time_series,apical_myoGrad_time_series,basal_myoGrad_time_series,mom_curvGrad_time_series,-1.0 *curv_apical_myoGrad_time_series,-1.0*curv_basal_myoGrad_time_series] 
        exp_data = numpy.array(model_INPUT_avg + [eff_heteroGenFriction] + [eff_heteroGenViscosity])
        # guessed-parameters  
        time_dependent_parameter_indices = [int(parameter_INDEXING[cp]) for cp in changingParameters]
        guess_parameter = [param*s_time_series.shape[0] if item_indx in time_dependent_parameter_indices else param for item_indx,param in enumerate(initial_parameter)]
        # fixed-parameters
        parameters_FIXED = {parameter_INDEXING[k]: v for k, v in parameters_FIXED.items()} 
        # fitting-switches
        piv_fittingDomain_List = numpy.arange(spatial_fitting_domain[0],spatial_fitting_domain[-1]) if spatial_fitting_domain else numpy.arange(0, s_time_series.shape[-1])
        # plot-variables
        time_ref = time_List[transition_merge_frame_reference]
        plot_variables = [time_ref,time_List,s_res_time_series,eff_heteroGenFriction,eff_heteroGenViscosity,piv_tan_time_series,piv_tan_std_time_series,full_avg_emb_piv_alligned_avg,full_avg_emb_piv_alligned_std]
        
        return plot_variables,normalized_arc_length,parameters_CONSTRAINT,curv_flag,distinguish_myo_switch,BOUNDARY_COND_SWITCH,piv_fittingDomain_List,parameter_INDEXING,parameters_FIXED,initial_parameter,simultaneous_fitting,hetVisco_flag,hetFric_flag,s_res_time_series,exp_data,guess_parameter
    
    #################### 
    # equation-fitting #
    ####################
    def model_fitting(self,s_ref,exp_data,guess_parameter,parameter_to_index_map,fix_PARAMETERS,fittingDomain,fit_constraints,boundary_condition,distinguish_myo_switch,curvature_flag): 
        # specify-input 
        s,piv,strain_Grad,total_myoGrad,apical_myoGrad,basal_myoGrad,total_mom_curvGrad,apical_mom_curvGrad,basal_mom_curvGrad,friction,viscosity = exp_data   
        myo_dependent_inputs = [apical_myoGrad,basal_myoGrad,curvature_flag*apical_mom_curvGrad,curvature_flag*basal_mom_curvGrad]     
        # distinguish-apical-basal_myo
        apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad = Model1D.distinguish_apical_basal_myo(distinguish_myo_switch,myo_dependent_inputs)
        # solution
        local_variables = locals().items()
        coefficient_data = {}
        for var in [strain_Grad,apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad,friction,viscosity]:
            coefficient_data.update({[item[0] for item in filter(lambda y: var is y[1], local_variables)][0]:var})
        model_data = [s,piv,coefficient_data,fittingDomain,guess_parameter,parameter_to_index_map,fix_PARAMETERS,fit_constraints,boundary_condition]
        # fitting 
        parameter,y_fit,chi_squr = inOutTools.equation_fit_to_data(Model1D.fun_eqn_coefficients,s,piv,coefficient_data,fittingDomain,guess_parameter,parameter_to_index_map,fix_PARAMETERS,fit_constraints,boundary_condition) 
        x_fit = [ele[fittingDomain] for ele in s_ref]
        # rescale-lh-by-total-arc-length
        s = numpy.array(s)
        lh = 1/numpy.sqrt(parameter[parameter_to_index_map['lh']])
        parameter[parameter_to_index_map['lh']] = [l/smax for l,smax in zip(lh,[ele[-1] for ele in numpy.array(s if s.ndim > 1 else [s])])] 
        
        return parameter,y_fit,chi_squr,x_fit if len(x_fit) > 1 else x_fit[0]

    ################
    # view-fitting #
    ################
    def view_FIT(self,savePath,uniformAxisLabel,pixel_to_micron_conversion_factor,hline_v_avg_pos,vline_v_avg_pos,rawLabel,fitLabel,figFormat): 
        # unit-conversion 
        s_fit,s_res_List = [numpy.array([numpy.array(ele)*pixel_to_micron_conversion_factor for ele in item]) for item in [self.s_fit,self.s_res_List]] if not self.normalized_arc_length else [self.s_fit,self.s_res_List]
        v_fit,piv_tan_time_series,piv_tan_std_time_series,full_avg_emb_piv_alligned_avg,full_avg_emb_piv_alligned_std = [numpy.array([numpy.array(ele)*pixel_to_micron_conversion_factor for ele in item]) for item in [self.v_fit,self.piv_tan_time_series,self.piv_tan_std_time_series,self.full_avg_emb_piv_alligned_avg,self.full_avg_emb_piv_alligned_std]]
        # v-fit-piv 
        Fig_v_avg,v_predict_avg_ax = plt.subplots(1, 1, figsize=(2.6, 1.3)) 
        v_exp_lim = [numpy.amin(piv_tan_time_series-piv_tan_std_time_series),numpy.amax(piv_tan_time_series+piv_tan_std_time_series)]
        v_fit_lim = [numpy.amin(v_fit),numpy.amax(v_fit)]
        ymin = numpy.amin([v_exp_lim[0],v_fit_lim[0]])
        ymax = numpy.amax([v_exp_lim[-1],v_fit_lim[-1]])
        v_lim = [ymin-(ymax-ymin)/10,ymax+(ymax-ymin)/10]
        for frame_counter,(s,v,s_ref,piv_tan_avg,piv_tan_std,hf,hv) in enumerate(zip(s_fit,v_fit,s_res_List,piv_tan_time_series,piv_tan_std_time_series,self.hetFriction,self.hetViscosity)): 
            FIG_v,v_predict_ax = plt.subplots(1, 1, figsize=(2.6, 1.3))
            v_predict_ax.plot(s, v, c='b', ls='-',label = fitLabel) 
            v_predict_ax.plot(s_ref, piv_tan_avg, c='k', ls='-',label = rawLabel) 
            v_predict_ax.fill_between(s_ref, piv_tan_avg-piv_tan_std,piv_tan_avg+piv_tan_std, facecolor='k', alpha=0.2)
            if uniformAxisLabel:
                v_predict_ax.set_ylim(v_lim)
            # friction
            range_fric = list(numpy.where(hf > 0)[0])
            if range_fric:
                range_fric_start,range_fric_end = [range_fric[0],range_fric[-1]] 
                fric_ax = v_predict_ax.twinx()
                fric_ax.axvspan(s[range_fric_start],s[range_fric_end],color='m',alpha = 0.3,linewidth=0.0,zorder=2)
                fric_ax.margins(x=0)
                fric_ax.axis('off')
            # viscosity
            range_visco = list(numpy.where(hv > 0)[0]) 
            if range_visco:
                range_visco_start,range_visco_end = [range_visco[0],range_visco[-1]]
                visco_ax = v_predict_ax.twinx()
                visco_ax.axvspan(s[range_visco_start],s[range_visco_end],color='b',alpha = 0.3,linewidth=0.0,zorder=2)
                visco_ax.margins(x=0)
                visco_ax.axis('off')
            # axis-atributes    
            inOutTools.customize_axis(v_predict_ax,xlim=[],ylim=[],x_pad=0.0,leg_loc=2,leg_size=3,hline_pos=0.0,vline_pos=0.0,tick_size=5)
            FIG_v.savefig(savePath + '/FIG_v_' + str(frame_counter) + '.' + figFormat, format = figFormat, figsize=(10, 3), dpi=500, bbox_inches='tight', pad_inches=0.02)
            plt.close(FIG_v)
        # v-fit-piv-avg 
        v_avg_predict = inOutTools.sliding_window_average_data([inOutTools.area_under_curve(s,v,closed=False)/s[-1] for s,v in zip(s_fit,v_fit)],window_SIZE=1) 
        v_predict_avg_ax.plot(self.time_List-self.time_ref,full_avg_emb_piv_alligned_avg,c = 'k', ls  = '-', lw = 1.0,zorder=1,label=rawLabel)
        v_predict_avg_ax.fill_between(self.time_List-self.time_ref,full_avg_emb_piv_alligned_avg-full_avg_emb_piv_alligned_std,full_avg_emb_piv_alligned_avg+full_avg_emb_piv_alligned_std,facecolor='k',alpha= 0.3)
        v_predict_avg_ax.plot(self.time_List-self.time_ref,inOutTools.sliding_window_average_data(v_avg_predict,window_SIZE=1), c='b', ls='-', lw=1.0, zorder=1,label = fitLabel)
        inOutTools.customize_axis(v_predict_avg_ax,xlim=[],ylim=[],x_pad=0.0,leg_loc=2,leg_size=3,hline_pos=hline_v_avg_pos,vline_pos=vline_v_avg_pos,tick_size=5)
        Fig_v_avg.savefig(savePath + '/FIG_v_avg.' + figFormat, format = figFormat, figsize=(10, 3), dpi=500, bbox_inches='tight', pad_inches=0.02)
        plt.close(Fig_v_avg) 
        # frame-dependent-parameter 
        for key,PARAMETER in self.fit_PARAMETERS.items():
            if len(PARAMETER) > 1:
                FIG,axis = plt.subplots(1, 1, figsize=(2.6, 1.3))
                axis.scatter(self.time_List-self.time_ref,PARAMETER, marker='o', s=10.0,facecolors='g', edgecolors='k', zorder=1, ls='-', lw=0.5, label = key)
                inOutTools.customize_axis(axis,xlim=[],ylim=[],x_pad=0.0,leg_loc='best',leg_size=3,hline_pos=0.0,vline_pos=0.0,tick_size=5)
                FIG.savefig(savePath + '/FIG_' + key + '.' + figFormat, format = figFormat, figsize=(10, 3), dpi=500, bbox_inches='tight', pad_inches=0.02)
                plt.close(FIG)
    
    ###########
    # fitting #
    ###########
    @classmethod
    def run_FITTING(cls,expData,parametersFileName,update_guess_parameters_Map):
        print('fitting in progre ...')
        fitting_parameters=inOutTools.read_parameter_file(parametersFileName)
        if update_guess_parameters_Map: fitting_parameters['guess_parameters_Map'] = update_guess_parameters_Map
        # fitting
        FIT = Fitting1D()
        plot_variables,normalized_arc_length,fit_constraints,curvature_flag,distinguish_myo_switch,boundary_condition,fittingDomain,parameter_to_index_map,parameters_fixed,initial_parameter,simultaneous_fitting,hetVisco_flag,hetFric_flag,s_ref,exp_data,all_parameter = FIT.process_fitting_data(expData,fitting_parameters)
        time_ref,time_List,s_res_List,eff_heteroGenFriction,eff_heteroGenViscosity,piv_tan_time_series,piv_tan_std_time_series,full_avg_emb_piv_alligned_avg,full_avg_emb_piv_alligned_std = plot_variables
        # simultaneous-fitting
        if simultaneous_fitting:
            print('simultinious fitting')
            fit_PARAMETERS,v_fit,chiSQ,s_fit = FIT.model_fitting(s_ref,exp_data,all_parameter,parameter_to_index_map,parameters_fixed,fittingDomain,fit_constraints,boundary_condition,distinguish_myo_switch,curvature_flag) 
            # update-FIT
            FIT.s_fit = s_fit
            FIT.v_fit = v_fit
            FIT.chiSQ = chiSQ
            FIT.normalized_arc_length = normalized_arc_length
            FIT.fit_PARAMETERS = dict(zip(list(parameter_to_index_map.keys()),fit_PARAMETERS))
        # individual-fitting
        else:
            print('individual fitting')
            fit_PARAMETERS_v_fit_chiSQ_s_fit_List = numpy.array([FIT.model_fitting([s],model_INPUT,initial_parameter.copy(),parameter_to_index_map,parameters_fixed,fittingDomain,fit_constraints,boundary_condition,distinguish_myo_switch,curvature_flag) for s,model_INPUT in zip(s_ref,numpy.swapaxes(exp_data,0,1))])
            fit_PARAMETERS,v_fit,chiSQ,s_fit = [fit_PARAMETERS_v_fit_chiSQ_s_fit_List[:,indx].tolist() for indx in range(fit_PARAMETERS_v_fit_chiSQ_s_fit_List.shape[1])]
            fit_PARAMETERS = numpy.swapaxes(numpy.array([inOutTools.flatten_List(p) for p in fit_PARAMETERS]),0,1).tolist()
            for key_indx,val in parameters_fixed.items():
                fit_PARAMETERS[key_indx] = [val] if {val} == set(fit_PARAMETERS[key_indx]) else fit_PARAMETERS[key_indx]
            # update-FIT
            FIT.s_fit = s_fit
            FIT.v_fit = v_fit
            FIT.chiSQ = list(numpy.concatenate(chiSQ).flat)
            FIT.normalized_arc_length = normalized_arc_length
            FIT.fit_PARAMETERS = dict(zip(list(parameter_to_index_map.keys()),fit_PARAMETERS))
        # plot-variables
        FIT.time_ref = time_ref
        FIT.time_List = time_List
        FIT.s_res_List = s_res_List
        FIT.hetFriction = eff_heteroGenFriction
        FIT.hetViscosity = eff_heteroGenViscosity
        FIT.piv_tan_time_series = piv_tan_time_series
        FIT.piv_tan_std_time_series = piv_tan_std_time_series
        FIT.full_avg_emb_piv_alligned_avg = full_avg_emb_piv_alligned_avg
        FIT.full_avg_emb_piv_alligned_std = full_avg_emb_piv_alligned_std
        
        return FIT
    
    ###########
    # fitting #
    ###########
    @classmethod
    def run_PARAMETER_SCAN(cls,expDataPath,parametersFileName,iniparametersFileName):
        print('chi-square-based-initial(guess)-parameter-scanning-in-progress ...')
        # load-scan-parameter-information
        parameter_KEY = []
        parameters_GUESS = []
        parameters_FIXED = []
        parameters_CONSTRAINT = []
        ini_parameters=inOutTools.read_parameter_file(iniparametersFileName)
        for indx,(param_key,param_val) in enumerate(ini_parameters['ini_guess_parameters_Map'].items()):
            parameter_KEY.append(param_key) 
            parameters_FIXED.append(param_val['fixed'])
            parameters_GUESS.append(param_val['initial_value'])
            parameters_CONSTRAINT.append(param_val['constraint'])
        # construct-scan(initial/guess)-parameter-list
        guess_parameters_Map_List = []
        for parameters in list(itertools.product(*parameters_GUESS)) :
            guess_parameters_Map = {}
            for key,val,cnst,status in zip(parameter_KEY,parameters,parameters_CONSTRAINT,parameters_FIXED): 
                guess_parameters_Map.update({key:{"initial_value":val,"constraint":cnst,"fixed":status}})
            guess_parameters_Map_List.append(guess_parameters_Map)
        # chi-square-minimization    
        chiSQ_Store = []
        for counter,update_guess_parameters_Map in enumerate(guess_parameters_Map_List):
            print('------------------------------------------------------------------')
            print(counter,':',update_guess_parameters_Map)
            FIT = cls.run_FITTING(expDataPath,parametersFileName,update_guess_parameters_Map)
            chiSQ_Store.append(sum(FIT.chiSQ))
        # select-initial-parameters
        chiSQ_Store = numpy.array(chiSQ_Store)
        guess_parameters_Map_List = numpy.array(guess_parameters_Map_List)
        chiSQ_Store_sorted_indices = numpy.argsort(chiSQ_Store) 
        chiSQ_Store = chiSQ_Store[chiSQ_Store_sorted_indices]
        update_guess_parameters_Map = guess_parameters_Map_List[chiSQ_Store_sorted_indices]
        print('-------------------------------------------')
        print('initial(guess)-parameter: SELECTED')
        print('-------------------------------------------')
        print(update_guess_parameters_Map[0])
        return update_guess_parameters_Map[0]
    
#======================================================================================================#
#                                         class: Model1D                                               #
#======================================================================================================#        
class Model1D:
    
    ####################
    # initialize-model #
    ####################
    def __init__(self,myoDomain,myoIntensity,ellipse_aspect_ratio,initial_myo_to_curv_offSet,physical_PARAMETERS,boundary_condition,distinguish_myo_switch,time_parameters,ellipse_semi_a,reMarker_Number,cell_width,HETEROGENEOUS_friction_domain):
        self.cell_width = cell_width
        self.time_step,time_max = time_parameters
        self.boundary_condition = boundary_condition
        self.physical_PARAMETERS = physical_PARAMETERS
        self.time_range = numpy.arange(0,int(time_max)-1)
        self.distinguish_myo_switch = distinguish_myo_switch
        self.HETEROGENEOUS_friction_domain = HETEROGENEOUS_friction_domain
        # friction/curvature-flag
        self.hetFric_flag = 0 if physical_PARAMETERS['gamma_del'] == 0 else 1
        self.curvature_flag = 0 if physical_PARAMETERS['gamma_del'] > 0 else 1
        # elliptic-model-parameterization
        self.mid_markers_ini = inOutTools.ellipse(ellipse_semi_a=ellipse_semi_a,ellipse_semi_b=ellipse_semi_a/ellipse_aspect_ratio-1e-3,numNode=2*reMarker_Number)
        self.intersection_scale_factor,self.ref_coordinate_orientation = inOutTools.set_ellipse_origin_on_semi_minor_axis(ellipse_semi_a,ellipse_semi_a/ellipse_aspect_ratio-1e-3,self.mid_markers_ini)
        self.mid_markers_ref = inOutTools.shift_origin_of_polygon_contour(self.mid_markers_ini,initial_myo_to_curv_offSet,self.intersection_scale_factor,self.ref_coordinate_orientation)
        # frame-series-varibles
        self.model_curv_List = []
        self.model_markers_List = []
        self.model_apical_myo_List = []
        self.model_heteroGenFriction_List = []
        self.model_v_inhomoFriction_PBC_List = []
        self.model_v_sp_avg_inhomoFriction_PBC = []
        self.model_apical_myo_patch_indices_List = []
        self.model_v_sp_avg_homoFriction_PBC_theo = []
        
        return
    
    ################
    # update-model #
    ################
    def update_MODEL(self,curv,apical_myo,updated_markers,heteroGenFriction,v_inhomoFriction_PBC,v_sp_avg_inhomoFriction_PBC,apical_myo_patch_indices,v_sp_avg_homoFriction_PBC_theo):
        self.model_curv_List.append(curv)
        self.model_apical_myo_List.append(apical_myo)
        self.model_markers_List.append(updated_markers)
        self.model_heteroGenFriction_List.append(heteroGenFriction)
        self.model_v_inhomoFriction_PBC_List.append(v_inhomoFriction_PBC)
        self.model_apical_myo_patch_indices_List.append(apical_myo_patch_indices)
        self.model_v_sp_avg_inhomoFriction_PBC.append(v_sp_avg_inhomoFriction_PBC)
        self.model_v_sp_avg_homoFriction_PBC_theo.append(v_sp_avg_homoFriction_PBC_theo)
        
        return
    
    #######################
    # equation-prediction #
    #######################
    def model_prediction(self,exp_data,physical_PARAMETERS): 
        # specify-input 
        s,strain_Grad,apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad,friction,viscosity = exp_data   
        # extract-input 
        myo_dependent_inputs = [apical_myoGrad,basal_myoGrad,self.curvature_flag*apical_mom_curvGrad,self.curvature_flag*basal_mom_curvGrad]     
        # distinguish-apical-basal_myo
        apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad = self.distinguish_apical_basal_myo(self.distinguish_myo_switch,myo_dependent_inputs)      
        # solution
        local_variables = locals().items()
        coefficient_data = {}
        for var in [strain_Grad,apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad,friction,viscosity]:
            coefficient_data.update({[item[0] for item in filter(lambda y: var is y[1], local_variables)][0]:var})
        coefficient_data.update(physical_PARAMETERS)
        A,B,C,D,fric = self.fun_eqn_coefficients(s,**coefficient_data)
        #############
        # solve-ODE #
        #############
        v_sol = inOutTools.ODE_solver_with_non_constant_coefficients(s,A,B,C,D,self.boundary_condition,boundary_value=[1e-6,1e-6])
        
        return v_sol,fric
    
    #############
    # modelling #
    #############
    @classmethod
    def run_MODEL(cls,parametersFileName,pixel_to_micron_conversion_factor,figFormat):
        print('modelling in progress ...')
        # parameters
        model_parameters=inOutTools.read_parameter_file(parametersFileName)
        outputPath = model_parameters['outputPath']
        physical_parameters = model_parameters['physical_parameters']
        boundary_condition = model_parameters['boundary_condition']
        distinguish_myo_switch = model_parameters['distinguish_myo_switch']
        myoDomains_List = [int(ele) for ele in model_parameters['myoDomains_List']] if isinstance(model_parameters['myoDomains_List'],list) else [int(model_parameters['myoDomains_List'])]
        myoIntensity_List,ellipse_aspect_ratio_List,initial_myo_to_curv_offSet_List = [[float(ele) for ele in item] if isinstance(item,list) else [item] for item in [model_parameters['myoIntensity_List'],model_parameters['ellipse_aspect_ratio_List'],model_parameters['initial_myo_to_curv_offSet_List']]]
        #*************#
        # start-model #
        #*************#
        inOutTools.recreateDirectory(outputPath + '/model')
        plot_instances = 0
        FIG_sim,Simulation_ax = plt.subplots(1, 1, figsize = (1.8,1.3))
        FIG_theo,Theoretical_ax = plt.subplots(1, 1, figsize = (1.8,1.3))
        FIG_v_predict_param_dep, v_predict_param_dep_ax = plt.subplots(1, 1, figsize=(2.6,1.3))
        for AR in ellipse_aspect_ratio_List:
            for IC_offSet in initial_myo_to_curv_offSet_List:
                for mD in myoDomains_List: 
                    for mI in myoIntensity_List:     
                        MODEL = Model1D(mD,mI,AR,IC_offSet,physical_parameters,boundary_condition,distinguish_myo_switch,model_parameters['time_parameters'],ellipse_semi_a=500,reMarker_Number=100,cell_width=60,HETEROGENEOUS_friction_domain=3) 
                        # default-origin-at-the-anterior-end-of-myo-patch 
                        half_length_myosin_patch = 2*mD*(len(MODEL.mid_markers_ini)+1) # myo-patch-length
                        origin_shift_index =  half_length_myosin_patch//200 # divide-by-number-of-epithelial-cells ~ 200 cells 
                        markers = numpy.roll(MODEL.mid_markers_ref,-origin_shift_index, axis=0) 
                        # myo-centre-displacement/starting-frame 
                        ds_next = 0.0  
                        markers_start_ref = numpy.copy(markers) 
                        #*************#
                        # time-series #
                        #*************#  
                        for time_indx in MODEL.time_range:
                            numNode = len(markers)
                            max_node_indx = numNode - 1
                            numNode_myo_domain = 2*mD-2
                            # position-of-the-myosin-patch-centre 
                            markers_centre_ref = inOutTools.numpy.array(inOutTools.Polygon(MODEL.mid_markers_ref).centroid.coords).flatten()
                            ref_intersetion_axis = numpy.array([markers_centre_ref + 2*(MODEL.intersection_scale_factor)*MODEL.ref_coordinate_orientation,markers_centre_ref])
                            _,myo_shift_detection_parameters = inOutTools.reset_starting_point_of_polygon(inOutTools.copy_DATA(markers),1.0*ref_intersetion_axis)
                            myo_marker_L,myo_indx_L = myo_shift_detection_parameters 
                            m_R_apical = max_node_indx - 1
                            m_L_apical = m_R_apical - 2*numNode_myo_domain
                            m_patch_apical = numpy.arange(m_L_apical,m_R_apical+1)
                            s,_ = inOutTools.arc_length_along_polygon(markers)
                            m_patch_apical_centre_indx = int(numpy.average(m_patch_apical))
                            # equation-inputs: pix-to-mic 
                            curv = inOutTools.smooth_data(inOutTools.curvature_along_polygon(markers,closed=True))
                            # equation-inputs: effective 
                            s_norm = s/s[-1]
                            apical_myo = numpy.zeros_like(s)
                            apical_myo[m_patch_apical] = mI 
                            basal_myo = numpy.zeros_like(s)
                            apical_mom = 0.5*MODEL.cell_width*apical_myo
                            basal_mom = 0.5*MODEL.cell_width*basal_myo
                            apical_myo_grad = inOutTools.gradients_of_data(s_norm,apical_myo,uniform_sampling=True,closed=True) 
                            basal_myo_grad = inOutTools.gradients_of_data(s_norm,basal_myo,uniform_sampling=True,closed=True)
                            curv_grad = inOutTools.gradients_of_data(s_norm,curv,uniform_sampling=True,closed=True)
                            heteroGenFriction = inOutTools.rectangular_function(s,[0,MODEL.HETEROGENEOUS_friction_domain]) 
                            apical_mom_curv_grad = apical_mom*curv_grad
                            basal_mom_curv_grad = basal_mom*curv_grad
                            strain_Grad = numpy.zeros(len(s))
                            INPUT = [s_norm,strain_Grad,apical_myo_grad,basal_myo_grad,apical_mom_curv_grad,basal_mom_curv_grad,MODEL.hetFric_flag*heteroGenFriction,inOutTools.numpy.zeros_like(heteroGenFriction)]
                            # simulation   
                            v_inhomoFriction_PBC,friction = MODEL.model_prediction(INPUT,MODEL.physical_PARAMETERS) 
                            # update-u    
                            v_sp_avg_inhomoFriction_PBC = inOutTools.area_under_curve(s_norm,v_inhomoFriction_PBC,closed=False)/s_norm[-1]
                            apical_myo_patch_indices = numpy.where(apical_myo)[0]
                            apical_myo_patch_indices = numpy.insert(apical_myo_patch_indices,[0,len(apical_myo_patch_indices)],[apical_myo_patch_indices[0]-1,apical_myo_patch_indices[-1]+1],axis=0)
                            # theoretical 
                            F_R,F_L = [0,MODEL.HETEROGENEOUS_friction_domain]
                            F_R = F_R - 2 if F_R > 0 else F_R
                            heterogeneous_friction_contribution = inOutTools.area_under_curve(s_norm[F_R:F_L+2],(friction[F_R:F_L+2]-1)*v_inhomoFriction_PBC[F_R:F_L+2],closed=False)
                            curvature_contribution = -1.0*MODEL.curvature_flag*(1/MODEL.physical_PARAMETERS['lh'])*(MODEL.physical_PARAMETERS['ra']*inOutTools.area_under_curve(s_norm,apical_mom*curv_grad,closed=True) - MODEL.physical_PARAMETERS['rb']*inOutTools.area_under_curve(s_norm,basal_mom*curv_grad,closed=True))
                            v_sp_avg_homoFriction_PBC_theo = curvature_contribution - heterogeneous_friction_contribution
                            # update-time-series-data
                            MODEL.update_MODEL(curv,apical_myo,markers,heteroGenFriction,v_inhomoFriction_PBC,v_sp_avg_inhomoFriction_PBC,apical_myo_patch_indices,v_sp_avg_homoFriction_PBC_theo)
                            # update-mid-markers: time-evolution 
                            ds = v_inhomoFriction_PBC[m_patch_apical_centre_indx]*MODEL.time_step # micron
                            ds_norm = ds/s[-1] # no-unit
                            ds_next += ds_norm
                            markers_next = markers_start_ref #
                            markers =  inOutTools.shift_position_of_a_point_along_polygon(markers_next,ds_next,m_patch_apical_centre_indx)
                            markers = numpy.roll(markers,-origin_shift_index, axis=0)   
                        #***************#
                        # parameter-key #
                        #***************#
                        model_markers = MODEL.model_markers_List[-1] 
                        s,_ = inOutTools.arc_length_along_polygon(model_markers)
                        if len(ellipse_aspect_ratio_List) >1:
                            key = 'AR = ' + str(AR)
                        elif len(myoIntensity_List) > 1: 
                            key = 'I = ' + str(round(mI,2))
                        elif len(myoDomains_List) > 1: 
                            key = 'ML = ' + str(round(2*mD*numpy.average(s[1:]-s[:-1])*pixel_to_micron_conversion_factor,2)) 
                        elif len(initial_myo_to_curv_offSet_List) > 1:
                            key = 'OFF-SET = ' + str(IC_offSet) 
                        else:
                            key = ' ' 
                        #***************#
                        # configuration #
                        #***************#
                        apical_myo_patch_indices = MODEL.model_apical_myo_patch_indices_List[-1]
                        apical_myo_patch_coordinates = model_markers[apical_myo_patch_indices]
                        if plot_instances == 1:
                            FIG_v_predict_config, v_predict_config_ax = plt.subplots(1, 1, figsize=(2.6,1.3))
                            # ellipse-contour
                            markers_line = numpy.insert(model_markers,0,model_markers[-1],axis=0)
                            v_predict_config_ax.plot(markers_line[:,0],markers_line[:,1],c='k',ls = '-',lw = 1.0,alpha = 1.0,zorder=2)  
                            # posterior-pole-reference
                            s,_ = inOutTools.arc_length_along_polygon(model_markers)
                            curv_peak_indx_first,curv_peak_indx_second = inOutTools.detection_of_peak_pairs_in_defined_region(s/s[-1],MODEL.model_curv_List[-1],[1.0,0.0],height=0.0,sorted_peaks=False)
                            posterior_pole = model_markers[curv_peak_indx_second]  
                            ellipse_centre = numpy.average(model_markers,axis = 0) 
                            v_predict_config_ax.plot([ellipse_centre[0],posterior_pole[0]],[ellipse_centre[1],posterior_pole[1]],ls='--', c='k', lw=1.0, zorder=3) 
                            # myosin-patch-reference
                            myo_centre_index = apical_myo_patch_indices[len(apical_myo_patch_indices)//2]
                            myo_centre = model_markers[myo_centre_index]
                            v_predict_config_ax.plot(apical_myo_patch_coordinates[:,0],apical_myo_patch_coordinates[:,1],c='g',ls = '-',lw = 2.0,zorder=10) 
                            v_predict_config_ax.plot([ellipse_centre[0],myo_centre[0]],[ellipse_centre[1],myo_centre[1]],ls='--', c='g', lw=1.0, zorder=3) 
                            # friction 
                            if MODEL.physical_PARAMETERS['gamma_del']:
                                hetFriction = MODEL.model_heteroGenFriction_List[-1]
                                if numpy.count_nonzero(hetFriction):
                                    friction_patch_indices = numpy.where(hetFriction)[0]
                                    friction_patch_coordinates = model_markers[friction_patch_indices]
                                    v_predict_config_ax.plot(friction_patch_coordinates[:,0],friction_patch_coordinates[:,1],c='m',ls = '-',lw = 2.0,alpha = 1.0,zorder=3)        
                            v_predict_config_ax.tick_params(axis='both', which='major', labelsize=3) 
                            # save-fig: config
                            FIG_v_predict_config.savefig(outputPath + '/model/FIG_config' + '.' + figFormat, format = figFormat, dpi=500, bbox_inches='tight', pad_inches=0.02)
                            plt.close(FIG_v_predict_config)
                        #***#
                        # v #
                        #***#
                        last_time_indx = len(MODEL.model_markers_List)-1 
                        # redefined-arc-length-reference: at-posterior-curvature-peak
                        s,s_max  = inOutTools.arc_length_along_polygon(MODEL.model_markers_List[last_time_indx])  
                        curv_peak_indx_first,curv_peak_indx_second = inOutTools.detection_of_peak_pairs_in_defined_region(s/s_max,MODEL.model_curv_List[last_time_indx],[0.5,0.0],height=0.0,sorted_peaks=False)
                        numNode = len(MODEL.model_markers_List[last_time_indx])
                        shift_indx = numNode -curv_peak_indx_second - int(0.31*numNode)  # -origin-shift-by, ds = 0.31
                        m,v,f,myo,curv = [numpy.roll(item,shift_indx,axis=0) for item in [MODEL.model_markers_List[last_time_indx],MODEL.model_v_inhomoFriction_PBC_List[last_time_indx],MODEL.model_heteroGenFriction_List[last_time_indx],MODEL.model_apical_myo_List[last_time_indx],MODEL.model_curv_List[last_time_indx]]]
                        s,s_max = inOutTools.arc_length_along_polygon(m)
                        curv_peak_indx_first,curv_peak_indx_second = inOutTools.detection_of_peak_pairs_in_defined_region(s/s_max,curv,[0.5,0.0],height=0.0,sorted_peaks=False)
                        s = s/s_max
                        s = s - s[curv_peak_indx_second]
                        # v 
                        v_predict_param_dep_ax.plot(s*pixel_to_micron_conversion_factor,v*pixel_to_micron_conversion_factor, c =colorsList[plot_instances], lw = 1.0, ls = '-',label = key)
                        curv_ax = v_predict_param_dep_ax.twinx()
                        curv_ax.plot(s*pixel_to_micron_conversion_factor, curv/pixel_to_micron_conversion_factor, c =colorsList[plot_instances], lw = 1.0, ls = '-',label = key)
                        # myosin
                        range_myo = list(numpy.where(myo > 0)[0])
                        if range_myo:
                            myo_ax = v_predict_param_dep_ax.twinx()
                            range_myo_start,range_myo_end = [range_myo[0],range_myo[-1]]
                            myo_ax.axvspan(s[range_myo_start],s[range_myo_end+1],color='g',alpha = 0.5,linewidth=0.0,zorder=2)
                            myo_ax.axis('off') 
                        # friction
                        if MODEL.physical_PARAMETERS['gamma_del']:
                            range_fric = list(numpy.where(f > 0)[0])
                            if range_fric:
                                fric_ax = v_predict_param_dep_ax.twinx()
                                range_fric_start,range_fric_end = [range_fric[0],range_fric[-1]]
                                fric_ax.axvspan(s[range_fric_start-1],s[range_fric_end],color='m',alpha = 0.5,linewidth=0.0,zorder=2)
                                fric_ax.axis('off') 
                        v_predict_param_dep_ax.axvline(s[curv_peak_indx_second], c =colorsList[plot_instances], lw = 1.0, ls = '-')
                        v_predict_param_dep_ax.margins(x=0) 
                        #*******#
                        # v-avg #
                        #*******#
                        for color_indx,(v_sp_avg,v_sp_avg_ax,line_style) in enumerate(zip([MODEL.model_v_sp_avg_inhomoFriction_PBC,MODEL.model_v_sp_avg_homoFriction_PBC_theo],[Simulation_ax,Theoretical_ax],['-','--'])):
                            v_sp_avg_ax.plot(MODEL.time_range*MODEL.time_step,numpy.array(v_sp_avg)*pixel_to_micron_conversion_factor,c=colorsList[plot_instances],markerfacecolor=colorsList[plot_instances], markeredgecolor=colorsList[plot_instances], ls = line_style, zorder=2,label = key)   
                        # increase-plot-number 
                        plot_instances += 1
        # save-figure: v-avg 
        for axis in [Simulation_ax,Theoretical_ax,v_predict_param_dep_ax]:
            inOutTools.customize_axis(axis,xlim=[],ylim=[],x_pad=0.0,leg_loc=0,leg_size=3,hline_pos=0.0,vline_pos=0.0,tick_size=5)
        # v-avg-theo
        FIG_theo.savefig(outputPath + '/model/FIG_v_avg_theo' + '.' + figFormat, format = figFormat, figsize=(10, 3), dpi=500, bbox_inches='tight', pad_inches=0.02)
        plt.close(FIG_theo)
        # v-avg-sim
        FIG_sim.savefig(outputPath + '/model/FIG_v_avg_sim' + '.' + figFormat, format = figFormat, figsize=(10, 3), dpi=500, bbox_inches='tight', pad_inches=0.02)
        plt.close(FIG_sim)
        # save-figure: v 
        FIG_v_predict_param_dep.savefig(outputPath + '/model/FIG_v_sim'  + '.' + figFormat, format = figFormat, dpi=500, bbox_inches='tight', pad_inches=0.02)
        plt.close(FIG_v_predict_param_dep)
        
        return 
    
    ###################################
    # distinguish-apical-basal-myosin #
    ###################################
    @classmethod
    def distinguish_apical_basal_myo(cls,distinguish_myo_switch,myo_dependent_inputs):
        apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad = myo_dependent_inputs
        # ra != rb 
        if distinguish_myo_switch:
            # apical: myo/mom-curv-grad
            apical_myoGrad = -1.0*apical_myoGrad # NOTE: flip-in-sign
            apical_mom_curvGrad = 1.0*apical_mom_curvGrad
            # basal: myo/mom-curv-grad
            basal_myoGrad = -1.0*basal_myoGrad # NOTE: flip-in-sign
            basal_mom_curvGrad = -1.0*basal_mom_curvGrad # NOTE: flip-in-sign
        # r_eff = ra, rb = 0 
        else:
            # apical: myo/mom-curv-grad
            apical_myoGrad = -1.0*apical_myoGrad -1.0*basal_myoGrad 
            apical_mom_curvGrad = 1.0*apical_mom_curvGrad -1.0*basal_mom_curvGrad
            # basal: myo/mom-curv-grad
            basal_myoGrad = numpy.zeros_like(basal_myoGrad) # NOTE: flip-in-sign
            basal_mom_curvGrad = numpy.zeros_like(apical_mom_curvGrad) # NOTE: flip-in-sign
            
        return apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad
    
    #######################################
    # function--for-eqnation-coefficients #
    #######################################
    @classmethod
    def fun_eqn_coefficients(cls,s,gamma_del,eta_del,lh,ra,rb,gamma_factor,eta_factor,elastic_modulus,strain_Grad,apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad,friction,viscosity):
        # include-elasticity 
        s_new = numpy.insert(s,[0,len(s)],[s[0],s[-1]],axis=0)
        # rescaling-parameters
        inv_sqr_L_H = lh*(gamma_factor/eta_factor)
        r_a = ra/eta_factor
        r_b = rb/eta_factor
        # viscosity
        A = 1.0 + viscosity*eta_del
        A = numpy.insert(A,[0,len(A)],[A[0],A[-1]],axis=0)
        # nothing
        B = numpy.ones_like(s_new)*0.0
        B = numpy.insert(B,[0,len(B)],[B[0],B[-1]],axis=0)
        # friction
        friction_0 = 1.0 + friction*gamma_del
        C = -1.0*friction_0*inv_sqr_L_H
        C = numpy.insert(C,[0,len(C)],[C[0],C[-1]],axis=0)
        # active-tension/curvature
        D = r_a*apical_mom_curvGrad + r_a*apical_myoGrad + r_b*basal_mom_curvGrad + r_b*basal_myoGrad - elastic_modulus*strain_Grad   
        D = numpy.insert(D,[0,len(D)],[D[0],D[-1]],axis=0)
        
        return A,B,C,D,friction_0
