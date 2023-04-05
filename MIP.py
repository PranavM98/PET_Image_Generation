import argparse
import numpy as np
from scipy.ndimage import rotate
import os
import matplotlib.pyplot as plt
import imageio
#Algorithm
'''
Input:
    1. Filename
    2. Angles
    3. Size of the Image (Width, Height, # Slices)
    4. Depth Weighting

Output:
    1.MIP image in the format (Width, # Slices, Angles of Rotations)
'''



def exponential_attenuation(mip,arg,r):

    final_mip=final_mip=np.zeros((mip.shape[0],mip.shape[1]))
    for i in range(mip.shape[1]):
        for j in range(mip.shape[0]):
            final_mip[j,i]=mip[j,i]*(1-r)**arg[j,i]
    return final_mip

def linear_attenuation(mip,arg):
    la=np.linspace(1,0.9,mip.shape[0])
    final_mip=final_mip=np.zeros((mip.shape[0],mip.shape[1]))
    for i in range(mip.shape[1]):
        for j in range(mip.shape[0]):
            final_mip[j,i]=mip[j,i]*la[arg[j,i]]
    return final_mip


def mip(img,angles,depth_weighting):
    final_matrix=np.zeros((img.shape[0],img.shape[2],angles))
    if depth_weighting=='Exponential':
        r=float(input("Enter the Exponential Constant, between 0 and 0.1 for better clarity\n"))
    if depth_weighting=='Linear':
        r=float(input("Enter the Linear Lower Limit (must be a number between 0 and 1)\n"))
    angles_final=np.linspace(0,360,angles)
    for i,angle in enumerate(angles_final):
        rotated = rotate(img, angle=angle,reshape=False)
        mip=np.amax(rotated, axis=0)
        arg=np.argmax(rotated, axis=0)

        if depth_weighting=='Linear':
            final_matrix[:,:,i]= linear_attenuation(mip,arg)
        elif depth_weighting=='Exponential':
            
            final_matrix[:,:,i]= exponential_attenuation(mip,arg,r)
        else:
            final_matrix[:,:,i]=mip
    return final_matrix


def main():
    while(True):
        file=input("Enter the File\n")
        
        try:
            angles=int(input("Enter Projection Angles (Must be an integer between 0-360)\n"))
        except:
            angles=int(input("Please enter the correct type for Projection Angle (Must be an integer between 0-360)\n"))
        
        try:
            width=int(input("Enter the width (Must be an Integer)\n"))
        except:
            width=int(input("Please enter the correct type for Width (Must be an integer)\n"))
        
        try:
            slices=int(input("Enter the Number of Slices (Must be an Integer)\n"))
        except:
            slices=int(input("Please enter the correct type for Slice (Must be an integer)\n"))

        try:
            img=np.fromfile(file, np.float32).reshape(slices,width,width)
            img=np.transpose(img,(1,2,0))
            break
        except:
            print("Error with inputting file. Please check the file name or the shape")
    print("Input Successful")

    depth_weighting=input("Type of Depth Weighting? No, Linear, Exponential (Capitalization Matters)\n")
    mip_image=mip(img,angles,depth_weighting)
    mip_image=mip_image.astype('float32')
  
    mip_image=np.transpose(mip_image,(1,0,2))

    print("Binary File Saved as: ",
                file+'_mip_Rot_'+str(angles)+'_DW_'+depth_weighting+'.bin')
                
    mip_image.tofile(file+'_mip_Rot_'+str(angles)+'_DW_'+depth_weighting+'.bin')

    final_list=[]
    for i in range(mip_image.shape[2]):
       
        final_list.append( mip_image[:,:,i])
    print("GIF File Saved as: ",
                file+'_mip_Rot_'+str(angles)+'_DW_'+depth_weighting+'.gif')
                
    imageio.mimsave(file+'_mip_Rot_'+str(angles)+'_DW_'+depth_weighting+'.gif', final_list)

main()
