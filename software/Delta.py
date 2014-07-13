# Delta.py

# Helper functions for kinematics for Delta printers
import numpy as np                                                          # Needed for sqrt
import logging

class Delta:
    Hez = 0.0   # Distance head extends below the effector. 
    L   = 0.135 # Length of the rod
    r   = 0.144 # Radius of the columns
    Ae  = 0.026 # Effector offset
    Be  = 0.026
    Ce  = 0.026
    Aco = 0.019 # Carriage offset
    Bco = 0.019
    Cco = 0.019

    # Column theta
    At = np.pi/2.0
    Bt = 7.0*np.pi/6.0
    Ct = 11.0*np.pi/6.0

    # Calculate the column positions
    Apx = r*np.cos(At)
    Apy = r*np.sin(At)
    Bpx = r*np.cos(Bt)
    Bpy = r*np.sin(Bt)
    Cpx = r*np.cos(Ct)
    Cpy = r*np.sin(Ct)

    # Calculate the effector positions
    Aex = Ae*np.cos(At)
    Aey = Ae*np.sin(At)
    Bex = Be*np.cos(Bt)
    Bey = Be*np.sin(Bt)
    Cex = Ce*np.cos(Ct)
    Cey = Ce*np.sin(Ct)

    # Calculate the virtual column positions
    Avx = Apx - Aex
    Avy = Apy - Aey
    Bvx = Bpx - Bex
    Bvy = Bpy - Bey
    Cvx = Cpx - Cex
    Cvy = Cpy - Cey


    ''' Inverse kinematics for Delta bot. Returns position for column A, B, C '''
    @staticmethod
    def inverse_kinematics(X, Y, Z):

        # Calculate the translation in carriage position
        Acz = np.sqrt(Delta.L**2 - (X - Delta.Avx)**2 - (Y - Delta.Avy)**2)
        Bcz = np.sqrt(Delta.L**2 - (X - Delta.Bvx)**2 - (Y - Delta.Bvy)**2)
        Ccz = np.sqrt(Delta.L**2 - (X - Delta.Cvx)**2 - (Y - Delta.Cvy)**2)

        # Calculate the position of the carriages
        Az = Z + Acz + Delta.Hez
        Bz = Z + Bcz + Delta.Hez
        Cz = Z + Ccz + Delta.Hez
        
        return np.array([Az, Bz, Cz])

    ''' Forward kinematics for Delta Bot. Returns the X, Y, Z point given column translations '''
    @staticmethod
    def forward_kinematics(Az, Bz, Cz):
        p1 = np.array([Delta.Avx, Delta.Avy, Az])
        p2 = np.array([Delta.Bvx, Delta.Bvy, Bz])
        p3 = np.array([Delta.Cvx, Delta.Cvy, Cz])
        
        p12 = p2-p1
        
        ex = p12/np.linalg.norm(p12)
        p13 = p3-p1
        i = np.dot(ex, p13)
        iex = i*ex
        ey = (p13-iex)/np.linalg.norm(p13-iex)
        ez = np.cross(ex,ey)
    
        d = np.linalg.norm(p12)

        j = np.dot(ey,p13) # Signed magnitude of the Y component
        
        D = Delta.L

        x = d/2;
        y = ((i**2 + j**2)/2 -i*x)/j;
        z = np.sqrt(D**2 - x**2 - y**2);

        # Construct the final point
        XYZ = p1 + x*ex + y*ey + -z*ez

        return XYZ




