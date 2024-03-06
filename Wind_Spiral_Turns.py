
import math
import matplotlib.pyplot as plt

#----------------------------------------------------
# Python program for ICAO PANS-OPS turn computations 
#----------------------------------------------------
# Version: 1                                        
# Author: Óscar Rigol                               
#----------------------------------------------------

# Input Data
Semi_Width = 2.5

# Parameter calculation
Primary_area = Semi_Width
Secondary_area = Semi_Width - 0.5*Primary_area

# IAS to TAS conversion
def Temp_Conversion (IAS, Altitude, VAR):
    TAS = IAS * 171233 * ((288 + VAR - (0.00198 * Altitude))**0.5) / (288 - (0.00198 * Altitude))**2.628
    return (TAS)

# Rate of Turn calculation
def Rate_of_Turn (TAS, Angle):
    R = (3431 * math.tan(Angle))/(math.pi * TAS)
    return (R)

# MOC applicable at the secondary area
def MOC_secondary (X):
    MOC_sec = MOC * (1 - (X / Secondary_area))
    return (MOC_sec)

# Radius of turn
def Radius_of_Turn (TAS, R):
    r = TAS/(20 * R * math.pi)
    return(r)

# Set of radii of the wind spiral
def Wind_Effect_Radii (R, Wind):
    E = []
    Angle = 45
    Iterations = int(360 / Angle)

    for i in range (1, Iterations): 
        Eo = ((Angle*i) / R) * (Wind / 3600)
        E.append(Eo)

    return(E) 

# Plots the spiral curves
def Arch_plotting(p1, p2):

    n = 1000
    r_0 = math.sqrt((p1[0]**2) + (p1[1]**2))
    r_1 = math.sqrt((p2[0]**2) + (p2[1]**2))
    step = abs(r_1 - r_0)/n
    X = []
    Y = []
    X.append(p1[0])
    Y.append(p1[1])

    angle_0 = math.atan2(p1[1], p1[0]) 
    angle_1 = math.atan2(p2[1], p2[0])
    angle_step = (angle_1 - angle_0)/n

    for i in range (1, n):
        x = (r_0 + (step*i)) * math.cos((i*angle_step) + angle_0)
        y = (r_0 + (step*i)) * math.sin((i*angle_step) + angle_0)
        X.append(x)
        Y.append(y)

    return(X, Y)

# Computes the Wind Spiral
def Wind_Spiral (r, E, Wind, TAS, Label):

    # Definition of the field
    figure, axes = plt.subplots()
    Angle = math.pi/4
    axes.set_aspect(1)
    Sub_circles = []
    Spiral_X = []
    Spiral_Y = []
    Spiral_X.append(- r)
    Spiral_Y.append(0)

    # Set of circles
    Main_circle = plt.Circle((0, 0), r, fill = False, color = "grey", linewidth = 0.5)
    axes.add_artist(Main_circle)
    axes.plot([0, 0], [r, -r], color = "grey", linewidth = 0.5)
    axes.plot([r, -r], [0, 0], color = "grey", linewidth = 0.5)

    for i in range (0, len(E)):

        # Calculate the points of application
        x = - (r * math.cos((i + 1) * Angle))
        y = r * math.sin((i + 1) * Angle)
        axes.plot([0, x], [0, y], color = "grey", linewidth = 0.5)

        # Calculate the internal radii points
        x_i = - (E[i] * math.cos((i + 1) * Angle)) 
        y_i = E[i] * math.sin((i + 1) * Angle) 
        axes.plot([x, (x + x_i)], [y, (y + y_i)], color = "grey", linewidth = 0.5)

        # Calculate the modified radii due to the wind
        sub_angle = math.asin(Wind/TAS)
        x_c = - (E[i] * math.cos(((i + 1) * Angle) - sub_angle))
        y_c = E[i] * math.sin(((i + 1) * Angle) - sub_angle)
        axes.plot([x, (x + x_c)], [y, (y + y_c)], color = "black", linewidth = 1)
        Spiral_X.append(x_c + x)
        Spiral_Y.append(y_c + y)

        # Draw the circle
        Sub_circles.append(plt.Circle((x, y), E[i], fill = False, color = "black", linewidth = 0.5))
        axes.add_artist(Sub_circles[i])

    # Draw the curvature arches of the spiral
    for i in range (0, len(E)):
        Arch = Arch_plotting([Spiral_X[i], Spiral_Y[i]], [Spiral_X[i + 1], Spiral_Y[i + 1]])
        axes.plot(Arch[0], Arch[1], color = "blue", linewidth = 2)

    # Final additions
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    plt.xlabel("Relative Distance Along Latitude (NM)", fontsize = 8) 
    plt.ylabel("Relative Distance Along Longitude (NM)", fontsize = 8)
    plt.text(-1.75, 1.75, ("IAS: %3d" % (Label[0])), fontsize = 8)
    plt.text(-0.875, 1.75, ("TAS: %5.2f" % (Label[1])), fontsize = 8)
    plt.text(0, 1.75, ("Altitude: %4d" % (Label[2])), fontsize = 8)
    plt.text(0.875, 1.75, ("Bank: %2d" % (Label[3])), fontsize = 8)
    plt.text(-1.75, 1.5, ("Wind: %3d" % (Label[4])), fontsize = 8)
    plt.text(-0.875, 1.5, ("ROT: %5.2f" % (Label[5])), fontsize = 8)
    plt.text(0, 1.5, ("Radius: %5.2f" % (Label[6])), fontsize = 8)
    plt.title("Wind Spiral and Computed Data")
    plt.show()

# Calculate all airplane data
def Airplane_computation(IAS, Bank, Altitude, Wind):
    TAS = Temp_Conversion(IAS, Altitude, 15)
    R = Rate_of_Turn(TAS, Bank)
    radius = Radius_of_Turn(TAS, R)
    E = Wind_Effect_Radii(R, Wind)
    Label = [IAS, TAS, Altitude, int(Bank * (180/math.pi)), Wind, R, radius]
    Wind_Spiral(radius, E, Wind, TAS, Label)
    print(Label)


# Example 1: CAT C aircraft with a maximum bank angle of 25º
Airplane_computation(160, (math.radians(25)), 4000, 30)

# Example 2: CAT B aircraft with a maximum bank angle of 25º
Airplane_computation(120, (math.radians(25)), 4000, 30)

# Example 2: CAT B aircraft with a maximum bank angle of 25º
Airplane_computation(90, (math.radians(25)), 4000, 30)


