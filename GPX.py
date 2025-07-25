import numpy as np
import time
from astropy.constants import G
from astropy.table import Table
import matplotlib.pyplot as plt

# Creating a function which prompts the user until a valid float or int is entered, based on dtype
def only_num(inpl,dtype):
  # Repeatedly ask until a valid int / float is entered
  while True:
    val=input(inpl)

    if dtype=='int':
      # Accept only integer input
      try:
        return int(val)
      except ValueError:
        # Show error and retry
        print(f"{val} is NOT a VALID input !!!")
        print("Input involving ONLY INTEGER data type is ALLOWED !!!",end='\n\n')
        time.sleep(1.5)
        continue

    else:
      # Accept only float input
      try:
        return float(val)
      except ValueError:
        print(f"{val} is NOT a VALID input !!!")
        print("Input involving ONLY FLOATING POINT data type is ALLOWED !!!",end='\n\n')
        time.sleep(1.5)
        continue

#####################################################################################################################################################################################

# Start of GPX
# Creating a variable loop and setting its initial value to 0
loop=0
while True:
  # If the loop repeats more than once, execute the below block
  if loop!=0:
    print("The program is now returning back to the MAIN MENU !!!",end='\n\n')
    print('****************************************************************************************************************************************',end='\n\n')
  # If the loop executes for the first time, execute the below block
  else:
    print("Welcome to GPX (Gravitational Potential Xplorer) !",end='\n\n')

    # A few important notes
    print("Some IMPORTANT PRECAUTIONS before using GPX.",end='\n\n')
    time.sleep(0.5)

    print("1--NOTE: ORIGIN CONSISTENCY",end='\n\n')
    print('****************************************************************************************************************************************',end='\n\n')
    print("> This program does not assume or enforce any specific origin for coordinates.")
    print("> However, all source positions and evaluation points must be measured relative to the SAME ORIGIN.")
    print("> Inconsistent coordinate origins may lead to incorrect results.",end='\n\n')
    print('****************************************************************************************************************************************',end='\n\n')
    time.sleep(1.5)

    print("2--NOTE: COORDINATE STRUCTURE",end='\n\n')
    print('****************************************************************************************************************************************',end='\n\n')
    print("> All 3D coordinates - whether entered manually or via file - must be provided in THREE SEPARATE VALUES for X, Y, and Z.")
    print("> Combined entries like 'x,y,z' or '(1 2 3)' are not supported and will lead to errors or misinterpretation.",end='\n\n')
    print('****************************************************************************************************************************************',end='\n\n')
    time.sleep(1.5)

    print("3-- NOTE: Gravitational Sources Configuration", end='\n\n')
    print('****************************************************************************************************************************************',end='\n\n')
    print("> The mass and coordinates you provide at the beginning define the gravitational sources.")
    print("> These values will be used for BOTH numerical potential evaluation and visualization.")
    print("> Make sure the configuration reflects your desired physical setup accurately.", end='\n\n')
    print('****************************************************************************************************************************************', end='\n\n')

  time.sleep(1.5)
  # Main Menu
  # After each loop, append 1 to the loop variable value
  loop+=1
  print(":::::::::::::::::::::::::  MAIN MENU  :::::::::::::::::::::::::",end='\n\n')
  print("1. Calculate Gravitational Potential.")
  print("2. Visualize Potential Distribution.")
  print("3. Terminate the Session.",end='\n\n')
  time.sleep(1.5)

  # Asking user for their choice from the main menu
  ch=input("Enter a choice from the Main Menu: ").strip()
  print('\n')
  print('****************************************************************************************************************************************',end='\n\n')

#####################################################################################################################################################################################
#####################################################################################################################################################################################

  # If the user goes with the choice for gravitational potential calculation
  if ch=='1' or ch=='2':
    print("NOTE: UNIT POLICY",end='\n\n')
    print('****************************************************************************************************************************************',end='\n\n')
    print("> All masses MUST be in kg, and coordinates MUST be in meters.")
    print("> This program does NOT ask for units or convert them - inputs are assumed to be in SI.",end='\n\n')
    print('****************************************************************************************************************************************',end='\n\n')
    time.sleep(1.5)

    # Gravitational Source Configuration Menu
    print(":::::::::::::::::::::::::  GRAVITATIONAL SOURCE CONFIGURATION MENU  :::::::::::::::::::::::::",end='\n\n')
    print("How would you like to provide source mass and position data?",end='\n')
    print("1. Manual Entry.")
    print("2. Load from CSV File.",end='\n\n')
    time.sleep(1.5)

    # Asking user for their choice from the gravitational source configuration menu
    chmc=input("Enter a choice from the gravitational source configuration menu:").strip()
    print('\n')
    print('****************************************************************************************************************************************',end='\n\n')

    m,x_m,y_m,z_m=[],[],[],[]       # Creating empty lists which would store the source data

    # If the user wants to manually enter the source data
    if chmc=='1':
      n=only_num("Enter the no.of source masses: ",'int')
      for i in range(n):
        while True:    # Ensuring that the source mass is always positive
          mass=only_num(f"Enter mass of source {i+1}: ",'float')
          if mass<0:
            print(f"ERROR: The mass of the source entered was found to be {mass}, which is INVALID !!!")
            print("Mass of the source MUST ALWAYS BE GREATER THAN OR EQUAL TO ZERO !!!",end='\n\n')
            continue
          else:
            break
        xcood_m=only_num(f"Enter the x coordinate of the source {i+1}: ",'float')
        ycood_m=only_num(f"Enter the y coordinate of the source {i+1}: ",'float')
        zcood_m=only_num(f"Enter the z coordinate of the source {i+1}: ",'float')
        time.sleep(1)

        # Appending the data one at a time to the empty lists
        m.append(mass)
        x_m.append(xcood_m)
        y_m.append(ycood_m)
        z_m.append(zcood_m)

      # Creating NumPy arrays of the source data lists
      M,X_M,Y_M,Z_M=np.array(m,dtype=float),np.array(x_m,dtype=float),np.array(y_m,dtype=float),np.array(z_m,dtype=float)

#####################################################################################################################################################################################

    # If the user wants to load the source data from a csv file
    elif chmc=='2':
      print("NOTE: FILE SEPARATION",end='\n\n')
      print('****************************************************************************************************************************************',end='\n\n')
      print("> You are about to load source data from a CSV file.")
      print("> Use TWO SEPARATE CSV FILES - one for source masses, one for evaluation points.")
      print("> Combining them in one file may create NULL values and CORRUPT the RESULT.",end='\n\n')
      print('****************************************************************************************************************************************',end='\n\n')
      time.sleep(1.5)

      # Asking user for the csv file containing the source data
      fsource=input("Enter the filename containing source mass and position data: ")
      print('\n')

      # Ensuring the file has a .csv extension
      if not fsource.lower().endswith('.csv'):
        print("This program ONLY SUPPORTS .csv file format !!!")
        continue

      # Ensuring the file exists
      try:
        tsource=Table.read(fsource,format='csv')
      except FileNotFoundError:
        print(f"The filename {fsource} provided does NOT EXIST !!! Please ENSURE that the file names provided do EXIST !",end='\n\n')
        continue

      # Ensuring the table in the file is non empty
      if len(tsource)==0:
        print(f"The table in the file {fsource} provided IS EMPTY !!! Please ENSURE that the tables are ALWAYS NON EMPTY !!!")
        continue

      time.sleep(1.5)
      print(f"The table extracted from the file {fsource} is:",end='\n\n')
      tsource.pprint_all()                                                      # Printing the extracted table
      print('\n')
      print('****************************************************************************************************************************************',end='\n\n')
      time.sleep(1.5)

      # Variables storing the column name
      masscol=x_mcol=y_mcol=z_mcol=''
      # List containing the variables
      varml=[masscol,x_mcol,y_mcol,z_mcol]
      # List containing the prompts to be displayed to the user
      dispml=[f"Enter the column name containing the mass values of the source bodies from {fsource}: ",f"Enter the column name for the x-coordinates of the source bodies from {fsource}: ",
              f"Enter the column name for the y-coordinates of the source bodies from {fsource}: ",f"Enter the column name for the z-coordinates of the source bodies from {fsource}: "]

      print("NOTE: COLUMN NAME ENTRY",end='\n\n')
      print('****************************************************************************************************************************************',end='\n\n')
      print("> You will now be asked to enter the column names for source mass and its position data.")
      print("> If the file looks INCORRECT or you're UNSURE, type 'EXIT' during any column name prompt to RETURN to the main menu.",end='\n\n')
      print('****************************************************************************************************************************************',end='\n\n')
      time.sleep(1.5)

      # Asking user for the name of the columns consisting of the required source data
      # The loop continues till a correct column name is entered
      # The user can opt to return back to the main manu via entering EXIT during any column prompt
      for i in range(4):
        chexitm=0                                                               # Variable which would check if the user enters EXIT
        invalm=0                                                                # Variable to ensure that no source mass is <0
        while not (chexitm==1 or invalm==1):
          varml[i]=input(dispml[i])

          # If EXIT is entered chexitm would point to 1
          if varml[i]=='EXIT':
            chexitm=1
            continue

          # If the column name is not found the loop restarts
          elif varml[i] not in tsource.colnames:
            print(f"The column name {varml[i]} is NOT PRESENT in the file {fsource} !!!")
            time.sleep(0.5)
            print("Please ENSURE that the column name being entered is present in the table !")
            time.sleep(0.5)
            print("PLEASE TRY AGAIN !!!")
            time.sleep(1)
            continue

          # Ensuring the data under the column name proivded is numeric
          elif not isinstance(tsource[varml[i]][0],(float,np.floating)):
            print(f"The data present under the column {varml[i]}, in the file {fsource} provided DOES NOT have NUMERIC data type !!!")
            time.sleep(0.5)
            print("Please ENSURE that the data under the column names provided MUST HAVE a NUMERIC data type !")
            time.sleep(0.5)
            print("PLEASE TRY AGAIN !!!")
            time.sleep(1)
            continue

          # For mass, if any of the row has mass<0 raise an error and break the loop and return to main menu
          # If no issue then, break the while loop and return back to the for loop
          else:
            if i==0:
              for j in range(len(tsource)):
                if (list(tsource[varml[0]]))[j]<0:
                  print(f"ERROR: The mass of the source at row number {j+1} was found to be {varml[0][j]}, which is INVALID !!!")
                  print("Mass of the source MUST ALWAYS BE GREATER THAN OR EQUAL TO ZERO !!!",end='\n\n')
                  invalm=1
                  continue
            else:
              break

        else:
          if chexitm==1:
            print("You have SUCCESSFULLY EXITED the gravitational source configuration loop !")
            break
          else:
            print("The gravitational source configuration loop is being TERMINATED !!!")
            break

      # Return  back to the main menu
      if chexitm==1 or invalm==1:
        continue

      # Extracting the data from each column and converting them to NumPy arrays
      M,X_M,Y_M,Z_M=np.array(tsource[masscol],dtype=float),np.array(tsource[x_mcol],dtype=float),np.array(tsource[y_mcol],dtype=float),np.array(tsource[z_mcol],dtype=float)

#####################################################################################################################################################################################

    # Invalid choice from gravitational source configuration menu
    else:
      print("INVALID choice from Gravitational Source Configuration Menu !!!")
      continue

#####################################################################################################################################################################################
#####################################################################################################################################################################################
  if ch=='1':
    evalloop=0
    while True:
      if evalloop!=0:
        print("The program is now returning back to the EVALUATION MENU !!!",end='\n\n')
        print('****************************************************************************************************************************************',end='\n\n')

      time.sleep(1.5)
      # Evaluation Menu
      evalloop+=1
      print(":::::::::::::::::::::::::  EVALUATION MENU  :::::::::::::::::::::::::",end='\n\n')
      print("How would you like to provide the positions at which gravitational potential should be evaluated?",end='\n')
      print("1a. Discrete Points (Manual Entry)  -  Enter coordinates directly into the terminal.")
      print("1b. Discrete Points (CSV File)      -  Load coordinates from a CSV file.")
      print("2. Uniform Grid                     -  Generate 3D grid using start/end values and resolution.")
      print("3. Return to Main Menu.",end='\n\n')
      time.sleep(1.5)

      # Asking user for their choice from evaluation menu
      chev=input("Enter a choice from the Evaluation Menu (e.g., 1a, 2, and etc): ").strip()
      print('\n')
      print('****************************************************************************************************************************************',end='\n\n')

#####################################################################################################################################################################################

      # Creating empty lists which would store the coordinates of the evaluation points
      x,y,z=[],[],[]

      # If the user wants to manually enter the coordinates of evaluation points
      if chev=='1a':

        np=only_num("Enter the no.of points where gravitational potential is to be evaluated: ",'int')
        for i in range(np):
          xcood=only_num(f"Enter the x coordinate of evaluation point {i+1}: ",'float')
          ycood=only_num(f"Enter the y coordinate of evaluation point {i+1}: ",'float')
          zcood=only_num(f"Enter the z coordinate of evaluation point {i+1}: ",'float')
          time.sleep(1)

          x.append(xcood)
          y.append(ycood)
          z.append(zcood)

        X,Y,Z=np.array(x,dtype=float),np.array(y,dtype=float),np.array(z,dtype=float)

        break

#####################################################################################################################################################################################

      # If the user wants to load the coordinates of evaluation points from a csv file
      elif chev=='1b':
        # Asking user to enter the file name consisting of the coordinates of evaluation points
        feval=input("Enter the filename containing the points for evaluation: ")
        print('\n')

        if not feval.lower().endswith('.csv'):
          print("This program ONLY SUPPORTS .csv file format !!!")
          continue

        try:
          teval=Table.read(feval,format='csv')
        except FileNotFoundError:
          print(f"The filename {feval} provided does NOT EXIST !!! Please ENSURE that the file names provided do EXIST !")
          continue

        if len(teval)==0:
          print(f"The table in the file {feval} provided IS EMPTY !!! Please ENSURE that the tables are ALWAYS NON EMPTY !!!")
          continue

        time.sleep(1.5)
        print(f"The table extracted from the file {feval} is:",end='\n\n')
        teval.pprint_all()
        print('\n')
        print('****************************************************************************************************************************************',end='\n\n')
        time.sleep(1.5)

        print("NOTE: COLUMN NAME ENTRY",end='\n\n')
        print('****************************************************************************************************************************************',end='\n\n')
        print("> You will now be asked to enter the column names for the evaluation point coordinates.")
        print("> If the file looks INCORRECT or you're UNSURE, type EXIT during any column name prompt to RETURN to the evaluation menu.",end='\n\n')
        print('****************************************************************************************************************************************',end='\n\n')
        time.sleep(1.5)

        xcol=ycol=zcol=''
        varl=[xcol,ycol,zcol]
        displ=[f"Enter the column name for the x-coordinate of the evaluation points from {feval}: ",f"Enter the column name for the y-coordinate of the evaluation points from {feval}: ",
               f"Enter the column name for the z-coordinate of the evaluation points {feval}: "]

        for i in range(3):
          chexit=0
          while chexit!=1:
            varl[i]=input(displ[i])

            if varl[i]=='EXIT':
              chexit=1
              break

            elif varl[i] not in teval.colnames:
              print(f"The column name {varl[i]} is NOT PRESENT in the file {feval} !!!")
              time.sleep(0.5)
              print("Please ENSURE that the column name being entered is present in the table !")
              time.sleep(0.5)
              print("PLEASE TRY AGAIN !!!")
              time.sleep(1)
              continue

            elif not isinstance(teval[varl[i]][0],(float,np.floating)):
              print(f"The data present under the column {varl[i]}, in the file {feval} provided DOES NOT have NUMERIC data type !!!")
              time.sleep(0.5)
              print("Please ENSURE that the data under the column names provided MUST HAVE a NUMERIC data type !")
              time.sleep(0.5)
              print("PLEASE TRY AGAIN !!!")
              time.sleep(1)
              continue

            else:
              break

          else:
            print("You have SUCCESSFULLY EXITED from column name entry loop !")
            break

        if chexit==1:
          continue

        X,Y,Z=np.array(teval[xcol],dtype=float),np.array(teval[ycol],dtype=float),np.array(teval[zcol],dtype=float)

        break

#####################################################################################################################################################################################

      # User has selected a uniform 3D grid - generate meshgrid from start/terminal points and resolution
      elif chev=='2':
        # Creating empty lists which would store the start and terminal points where the potential evaluation would occur
        s,e=[],[]
        # Asking user for the start and terminal points for each axis
        for q in ['X','Y','Z']:
          while True:
            spt=only_num(f"Enter the start point at which potential is to be evaluated wrt to origin along {q} axis:",'float')
            tpt=only_num(f"Enter the terminal point at which potential is to be evaluated wrt to origin along {q} axis:",'float')
            # Ensuring that the start point lies before the terminal point along the chosen axis
            if spt<tpt:
              s.append(spt)
              e.append(tpt)
              break
            else:
              print("The start point MUST ALWAYS be LESS THAN the terminal point !!!")
              print("Please TRY AGAIN !",end='\n\n')
              time.sleep(1.5)
              continue

        # Asking user for grid resolution
        while True:
          h=only_num("Enter the no.of points in between the start and the terminal in which the potential is to be evaluated:",'int')
          if h<2:
            print("No. of evaluation points must be at least 2 to generate a field plot !!!")
            print("Please TRY AGAIN !",end='\n\n')
            continue
          else:
            break

        # Creating equally spaced points along each axis
        x=np.linspace(s[0],e[0],h)
        y=np.linspace(s[1],e[1],h)
        z=np.linspace(s[2],e[2],h)

        X,Y,Z=np.meshgrid(x,y,z,indexing='ij')         # Creating a uniform 3D grid

        break

#####################################################################################################################################################################################

      # If the user wants to exit from the evaluation menu
      elif chev=='3':
        # Reconfirming whether they really want to exit
        print("Are you sure? You would return back to the Main Menu.",end='\n\n')
        sure=input("If you still want to CONTINUE with evaluation process, enter (y / Y / yes / YES): ")
        if sure in ['y','Y','yes','YES']:                                       # If they dont want to exit, the program returns back to the evaluation menu
          continue
        else:                                                                   # Else the program exits from the evaluation menu
          break

#####################################################################################################################################################################################

      # If the user goes with an invalid choice from the evaluation menu
      else:
        print("INVALID choice from the Evaluation Menu !!! Please enter a VALID choice !")
        continue

#####################################################################################################################################################################################

    # To return back to the main menu
    if chev=='3':
      continue

    # CENTRAL LOGIC SECTION
    # ---------------------------------------------------------------

    # Creating an empty array which would store the net potential for each point on the grid
    P=np.zeros_like(X)

    # Asking user to enter a softening constant and also ensuring that it is >0
    while True:
      eps=only_num("Enter a small softening constant ε to avoid singularities (recommended: 1e-6 (i.e., 10^-6) to 1e-2 (i.e., 10^-2), must be > 0): ",'float')
      if eps>0:
        break
      else:
        print("The value of ε MUST ALWAYS be > 0 !!!",end='\n\n')
        print("Please TRY AGAIN !",end='\n\n')
        continue

    # Calculating the potential for each point by each source mass and appending it to P
    for i in range(len(M)):
      p=(-(G)*(M[i]))/((X-X_M[i])**2+(Y-Y_M[i])**2+(Z-Z_M[i])**2+(eps)**2)**(0.5)
      P+=p

    # Constructing the output table with evaluation coordinates, radial distances, and computed potentials
    output=Table()

    # Compute radial distance of each evaluation point from the origin
    r_eval=np.sqrt((X**2)+(Y**2)+(Z**2))

    output['x_eval']=np.ravel(X)
    output['y_eval']=np.ravel(Y)
    output['z_eval']=np.ravel(Z)
    output['r_eval']=np.ravel(r_eval)
    output['Potential']=np.ravel(P)

#####################################################################################################################################################################################

    # POST-COMPUTATION INTERFACE
    # ---------------------------------------------------------------

    dsloop=0
    while True:
      if dsloop!=0:
        print("The program is now returning back to the DISPLAY & SAVE MENU !!!",end='\n\n')
        print('****************************************************************************************************************************************',end='\n\n')

      time.sleep(1.5)
      # Display & Save Menu
      dsloop+=1
      print(":::::::::::::::::::::::::  DISPLAY & SAVE MENU  :::::::::::::::::::::::::",end='\n\n')
      print("1. Show truncated result table  -  Preview mode.")
      print("2. Show full result table       -  All rows.")
      print("3. Show summary                 -  Min/Max potential values and their coordinates.")
      print("4. Save result table to a CSV file.")
      print("5. Return to Main Menu.",end='\n\n')
      time.sleep(1.5)

      # Asking user to enter a choice from display & save menu
      chds=input("Enter a choice from Display & Save Menu: ").strip()
      print('\n')
      print('****************************************************************************************************************************************',end='\n\n')

#####################################################################################################################################################################################

      # Two display options because-
      # Astropy's Table prints truncated or summary views (fast, clean output)
      # Pandas DataFrame allows full view to support full row visibility customization

      if chds=='1':
        print("The table below shows a PREVIEW of the evaluation coordinates and their corresponding gravitational potentials:",end='\n\n')
        print(output,end='\n\n')
        print('****************************************************************************************************************************************',end='\n\n')

      elif chds=='2':
        print("The FULL result table of evaluation coordinates and their corresponding gravitational potentials is shown below:",end='\n\n')
        output.pprint_all()
        print('****************************************************************************************************************************************',end='\n\n')

#####################################################################################################################################################################################

      # If the user wants to know the summary of the potential evaluation
      elif chds=='3':
        # 1D lists containg potential and the coordinates for the evaluation points
        RX,RY,RZ,RP=np.ravel(X),np.ravel(Y),np.ravel(Z),np.ravel(P)

        mincood,maxcood=[],[]       # Lists that would store the coordinates where min and max potential is found
        min_reval=max_reval=0       # Variables which would store the distance where the min and max potential is found wrt origin

        # Value of the min and max potential
        minp=min(RP)
        maxp=max(RP)

        # Finding the coordinates and the distance (wrt origin) for min and max potential
        for i in range(len(RP)):
          mint,maxt=(0,0,0),(0,0,0)

          if RP[i]==min(RP):
            a,b,c=mint
            a,b,c=RX[i],RY[i],RZ[i]
            mint=(a,b,c)                                                      # Storing the coordinates in a tuple form
            mincood.append(mint)                                              # Appending the coordinate tuples to pre defined lists
            min_reval=((RX[i])**2+(RY[i])**2+(RZ[i])**2)**0.5                 # Calculating the distance

          elif RP[i]==max(RP):
            d,e,f=maxt
            d,e,f=RX[i],RY[i],RZ[i]
            maxt=(d,e,f)
            maxcood.append(maxt)
            max_reval=((RX[i])**2+(RY[i])**2+(RZ[i])**2)**0.5

          else:
            pass

        # Printing the summary
        print('****************************************************************************************************************************************',end='\n\n')
        print(f"Minimum gravitational potential was evaluated to be: {minp} units and at a distance of {min_reval} units from the origin.")
        print("Coordinate(s) at which this occurs:",end='\n\n')
        for k in range(len(mincood)):
          print(f"{k+1}) {mincood[k]}")
        print('****************************************************************************************************************************************',end='\n\n')
        print(f"Maximum gravitational potential was evaluated to be: {maxp} units and at a distance of {max_reval} units from the origin.")
        print("Coordinate(s) at which this occurs:",end='\n\n')
        for k in range(len(maxcood)):
          print(f"{k+1}) {maxcood[k]}")
        print('****************************************************************************************************************************************',end='\n\n')

#####################################################################################################################################################################################

      # If the user wants to save the result table
      elif chds=='4':
        svloop=0
        while True:
          if svloop!=0:
            print("The program is now returning back to the SAVE SUBMENU !!!",end='\n\n')
            print('****************************************************************************************************************************************',end='\n\n')
          else:
            print("NOTE: SAVE OUTPUT STRUCTURE",end='\n\n')
            print('****************************************************************************************************************************************',end='\n\n')
            print("The following columns will be added to your file:",end='\n\n')
            print("1) Evaluation point coordinates (X, Y, Z): stored in three separate columns.")
            print("2) Radial distance from origin.")
            print("3) Gravitational potential at each evaluation point.",end='\n\n')
            print('****************************************************************************************************************************************',end='\n\n')

          time.sleep(1.5)
          # Save Menu
          svloop+=1
          print(":::::::::::::::::::::::::  SAVE SUBMENU  :::::::::::::::::::::::::",end='\n\n')
          print("1. Save to a new file or overwrite an existing file.")
          print("2. Append the result to an existing file.")
          print("3. Cancel and return to the Display & Save Menu.",end='\n\n')
          time.sleep(1.5)

          # Asking user for a choice from the save menu
          svch=input("Enter a choice from the Save Submenu: ").strip()
          print('\n')
          print('****************************************************************************************************************************************',end='\n\n')

    ########################################################################################################################

          # If the user wants to save the table to a new file or overwrite existing file
          if svch=='1':
            # Asking user for a name of the new file to be created / name of the existing file to be overwritten
            fname=input("Enter the name of new file to be created / existing file to be overwritten (in .csv): ")
            print('\n')

            if not fname.lower().endswith('.csv'):
              print("This program ONLY SUPPORTS .csv file format !!!")
              continue

            print("NOTE: COLUMN NAMING POLICY",end='\n\n')
            print('****************************************************************************************************************************************',end='\n\n')
            print("> You can now assign custom column names for the saved output table.")
            print("> These names will appear in the CSV file.")
            print("> You may leave it blank if you do not wish to assign a custom name.",end='\n\n')
            print('****************************************************************************************************************************************',end='\n\n')
            time.sleep(1.5)

            # Asking user for the column names under which the data would be stored
            xcoodcol=input("Enter the column name you want to use for the X-coordinate of evaluation points: ")
            print('\n')
            ycoodcol=input("Enter the column name you want to use for the y-coordinate of evaluation points: ")
            print('\n')
            zcoodcol=input("Enter the column name you want to use for the z-coordinate of evaluation points: ")
            print('\n')
            distcol=input("Enter the column name for the distance from the origin to each evaluation point: ")
            print('\n')
            potcol=input("Enter the column name for gravitational potential values: ")
            print('\n')

            # Creating a new table and appending the data into it
            owtable=Table()
            owtable[xcoodcol]=np.ravel(X)
            owtable[ycoodcol]=np.ravel(Y)
            owtable[zcoodcol]=np.ravel(Z)
            owtable[distcol]=np.ravel(r_eval)
            owtable[potcol]=np.ravel(P)

            # Creating a new file / overwrting an existing file
            owtable.write(fname,format='csv',overwrite=True)

            # Ensuring the new file creation / overwrite of existing file was successful
            if (Table.read(fname,format='csv'))==owtable:
              print(f"The file {fname} has been SUCCESSFULLY OVERWRITTEN !!!")
              break
            else:
              print("The overwrite was UNSUCCESSFUL !!! ")
              print("Please TRY AGAIN !!!",end='\n\n')
              continue

    ########################################################################################################################

          # If the user wants to append the result to an existing file
          elif svch=='2':
            # Asking user to enter the name of the existing file
            fname=input("Enter the name of an existing file (in .csv): ")
            print('\n')

            if not fname.lower().endswith('.csv'):
              print("This program ONLY SUPPORTS .csv file format !!!")
              continue

            try:
              exrct=Table.read(fname,format='csv')
            except FileNotFoundError:
              print(f"The filename {fname} provided does NOT EXIST !!! Please ENSURE that the file names provided do EXIST !")
              continue

            if len(exrct)==0:
              print(f"The table in the file {fname} provided IS EMPTY !!! Please ENSURE that the tables are ALWAYS NON EMPTY !!!")
              continue

            # Printing the extracted table
            time.sleep(1.5)
            print(f"The table extracted from the file {fname} provided is:",end='\n\n')
            print(exrct,end='\n\n')
            print('****************************************************************************************************************************************',end='\n\n')
            time.sleep(1.5)

            print("NOTE: COLUMN NAMING POLICY",end='\n\n')
            print('****************************************************************************************************************************************',end='\n\n')
            print("> You can now assign custom column names for the saved output table.")
            print("> These names will appear in the CSV file.")
            print("> You may leave it blank if you do not wish to assign a custom name.",end='\n\n')
            print('****************************************************************************************************************************************',end='\n\n')
            time.sleep(1.5)

            xcoodcol=input("Enter the column name you want to use for the X-coordinate of evaluation points: ")
            print('\n')
            ycoodcol=input("Enter the column name you want to use for the y-coordinate of evaluation points: ")
            print('\n')
            zcoodcol=input("Enter the column name you want to use for the z-coordinate of evaluation points: ")
            print('\n')
            distcol=input("Enter the column name for the distance from the origin to each evaluation point: ")
            print('\n')
            potcol=input("Enter the column name for gravitational potential values: ")
            print('\n')

            exrct[xcoodcol]=np.ravel(X)
            exrct[ycoodcol]=np.ravel(Y)
            exrct[zcoodcol]=np.ravel(Z)
            exrct[distcol]=np.ravel(r_eval)
            exrct[potcol]=np.ravel(P)

            # Appending the result to the extracted table and overwriting the original table in the extracted file
            exrct.write(fname,format='csv',overwrite=True)

            if (Table.read(fname,format='csv'))==exrct:
              print(f"The columns were SUCCESFULLY appended to the table in file {fname} !!!")
              break
            else:
              print("The append was UNSUCCESSFUL !!! ")
              print("Please TRY AGAIN !!!",end='\n\n')
              continue

    ########################################################################################################################

          # If the user wants to exit the save menu
          elif svch=='3':
            break

    ########################################################################################################################

          # If the user goes with an invalid choice from the save menu
          else:
            print("INVALID choice from the SAVE SUBMENU !!! Please enter a VALID choice !",end='\n\n')

#####################################################################################################################################################################################

      # If the user wants to exit the display and save menu
      elif chds=='5':
        # Ensuring that the user really want to return back to main menu
        print("Are you sure you want to return back to the Main Menu?",end='\n\n')
        # Reminding the user to save the results if not done
        print('NOTE: SAVE CONFIRMATION REMINDER',end='\n\n')
        print('****************************************************************************************************************************************',end='\n\n')
        print("> Ensure you have saved your results to avoid losing valuable output.")
        print("> Unsaved data will not be retained after exiting this menu.",end='\n\n')
        print('****************************************************************************************************************************************',end='\n\n')
        time.sleep(1.5)

        dssure=input("If you still want to continue with display and save process, enter (y / Y / yes / YES): ")
        if dssure in ['y','Y','yes','YES']:                                   # If the user doesnt want to exit, the program returns back to d&s menu
          continue
        else:                                                                 # Else, the program returns back to the main menu
           break

#####################################################################################################################################################################################

      # If the user enters an invalid choice from the d&s menu
      else:
        print("INVALID choice from the DISPLAY & SAVE MENU !!! Please enter a VALID choice !",end='\n\n')

#####################################################################################################################################################################################
#####################################################################################################################################################################################

  # If the user wants to visualize potential distribution
  elif ch=='2':

    # Creating a function which asks user for contour levels for contour() and contourf() functions
    def clc():
      global lvl        # Declaring the variable storing the contour levels global
      lvl=0

      print("=> Contour Levels Configuration: ")
      print("Set the values at which contour lines will be drawn (heights of potential).")
      print("Examples: 10 => Number of levels | [-51, -37, 0, 21, 45] => Specific values",end='\n\n')
      time.sleep(1.5)

      # Ensuring that the user enters a valid contour level configuration (integer or list data type)
      while True:
        time.sleep(0.5)
        # Evaluating the user input to handle invalid Python syntax
        try:
          lvl=eval(input("Enter number of levels or list of values: "))
        except SyntaxError:
          print("ERROR: INVALID syntax detected !!! Please enter either an integer or a list (e.g., 10 or [-10, 0, 5]) !")
          print('Please try again !!!',end='\n\n')
          continue

        # If the contour level configuration is invalid, an error arises
        if not (isinstance(lvl,(int)) or isinstance(lvl,(list))):
          print(f"The {lvl} provided for levels DOES NOT have an INTEGER or LIST data type !!! Please ENSURE that values of ONLY those two data type are ENTERED !!!")
          print("Please try again !!!",end='\n\n')
          continue

        # Ensuring that all elements are numeric in a list type cotour level configuration
        if isinstance(lvl, list) and not all(isinstance(val, (int, float)) for val in lvl):
          print("ERROR: ALL ELEMENTS in the list MUST be NUMERIC (int or float) values !!!")
          print("Please try again !!!",end='\n\n')
          continue

        # Ensuring an error is raised upon encountering an invalid contour level value
        if isinstance(lvl,(int)) and lvl<0:
          print(f"ERROR: The contour level count: {lvl} provided is INVALID !!! Contour level count MUST ALWAYS be ≥ 0 !")
          print("Please try again !!!",end='\n\n')
          continue

        break

#####################################################################################################################################################################################

    # Creating a function which asks user for figure metadeta
    def common():
      global xlabel,ylabel,ptitle
      xlabel,ylabel,ptitle='','',''

      xlabel=input("Enter a label for X-axis: ")
      ylabel=input("Enter a label for Y-axis: ")
      ptitle=input("Enter the title for the plot (leave blank for none): ")

#####################################################################################################################################################################################

    # Creating a function which displays and saves the plot
    def showsave():
      # Displaying the graph
      plt.tight_layout()
      plt.show(block=False)
      plt.pause(1)
      print('\n')
      print('****************************************************************************************************************************************',end='\n\n')

      # Creating a loop with a two-tier verification, asking user whether to save the plot or not
      while True:
        # Asking user whether the plot is to be save
        pltsave=input("Enter (y / Y / yes / YES), if you want to save the above graph: ")
        # If the user wants to save the plot
        if pltsave in ['y','Y','yes','YES']:
          print("SETTINGS: Save Settings – ACADEMIC DEFAULTS APPLIED")
          print("DPI = 300 | BBOX_INCHES = 'tight' | TRANSPARENT = False")
          print('****************************************************************************************************************************************',end='\n\n')
          time.sleep(1.5)

          print("NOTE: Only .png and .pdf formats are supported. Please name your file accordingly.", end='\n\n')
          print('****************************************************************************************************************************************',end='\n\n')
          time.sleep(1.5)

          while True:
            # Asking user for the name of the file where the plot will be saved
            pltf=input("Enter a name for the file where the plot is to be saved (include .png or .pdf extension): ")

            # Ensuring that the file has only .png or .pdf extension
            if not (pltf.lower().endswith('.png') or pltf.lower().endswith('.pdf')):
              print(f"The file name {pltf} does NOT end with a .png or .pdf extension !!!")
              time.sleep(0.5)
              print("Please try again !!!",end='\n\n')
              time.sleep(0.5)
              continue
            else:
              break
          # Saving the plot
          plt.savefig(pltf,dpi=300,bbox_inches='tight',transparent=False)
          print("Plot has been SAVED SUCCESSFULLY !!!",end='\n\n')

        # If the use does not want to save the plot
        else:
          print("Are you sure you don't want to save the plot? The plot would be discarded and shall not be retrievable.")
          pltsure=input("If you don't want to loose progress, enter (y / Y / yes / YES): ")   # Reaffirming user's decision
          # If the user wants to continue with saving the plot
          if pltsure in ['y','Y','yes','YES']:
            time.sleep(1)
            continue    # The loop starts again
          # If the user wants to discard the plot
          else:
            break       # The loop breaks

#####################################################################################################################################################################################

    vizloop=0
    while True:
      if vizloop!=0:
        print("The program is now returning back to the VISUALIZATION MENU !!!",end='\n\n')
        print('****************************************************************************************************************************************',end='\n\n')
      else:
        print("NOTE: ACADEMIC DEFAULTS APPLIED",end='\n\n')
        print('****************************************************************************************************************************************',end='\n\n')
        print("> Certain VISUAL SETTINGS are FIXED for CLARITY and NOT USER-CONFIGURABLE.")
        print("> These will be SHOWN when the RELEVANT PLOT TYPE is selected.")
        print("> To MODIFY them, EDIT the SOURCE CODE DIRECTLY.",end='\n\n')
        print('****************************************************************************************************************************************',end='\n\n')

      time.sleep(1.5)
      errincsv=0 # Error variable for cvsentry() function. After every loop it is set back to 0

      # Visualization Menu
      vizloop+=1
      print(":::::::::::::::::::::::::  VISUALIZATION MENU  :::::::::::::::::::::::::",end='\n\n')
      print("1. Render 2D Gravitational Slice via Color Mapping.")
      print("2. Render Equipotential Contours (Line Representation).")
      print("3. Render Equipotential Contours (Filled Representation).")
      print("4. Exit Visualization Menu.", end='\n\n')
      time.sleep(1.5)

      # Asking user for their choice from the visualization menu
      vizch=input("Enter a choice from Visualization Menu: ").strip()
      print('\n')
      print('****************************************************************************************************************************************',end='\n\n')

#####################################################################################################################################################################################

      if vizch=='1' or vizch=='2' or vizch=='3':
        if vizch=='1':
          # Display default settings based on the selected plot type
          print("SETTINGS: Color Map (imshow) – ACADEMIC DEFAULTS APPLIED",end='\n\n')
          print("CMAP = 'magma' | ORIGIN = 'lower' | COLORBAR = ON | ORIENTATION = 'vertical' | GRID= OFF",end='\n\n')
        elif vizch=='2':
          print("SETTINGS: Line Contour Plot (contour) – ACADEMIC DEFAULTS APPLIED",end='\n\n')
          print("CMAP = 'magma' | COLORBAR = OFF | CLABEL = ON | INLINE = False | FONTSIZE = 8 | FMT = '%.1f' | GRID= OFF",end='\n\n')
        else:
          print("SETTINGS: Filled Contour Plot (contourf) – ACADEMIC DEFAULTS APPLIED")
          print("CMAP = 'magma' | COLORBAR = ON | ORIENTATION = 'vertical' | CLABEL = OFF | GRID= OFF")
        print('****************************************************************************************************************************************',end='\n\n')
        time.sleep(1.5)

        print("NOTE: Slice Configuration", end='\n\n')
        print('****************************************************************************************************************************************',end='\n\n')
        print("> To generate a 2D slice of the 3D gravitational potential field, one coordinate axis must be held constant while varying the other two.")
        print("> This will generate a planar cross-section of the potential for analysis.", end='\n\n')
        print('****************************************************************************************************************************************',end='\n\n')
        time.sleep(1.5)

        # Asking user which axis to hold constant (slice direction)
        while True:
          constaxis=input("Select the axis to hold constant for slicing (X, Y, or Z): ").strip().lower()
          print('\n')
          if constaxis not in ['x','y','z']:
            print()
            print('Please TRY AGAIN !',end='\n\n')
            time.sleep(1.5)
            continue
          else:
            break

        # Creating a fucntion to print configured slice information
        def defaxis(cax,hax,vax):
          print("SETTINGS: Slice-Based Potential Plot – ACADEMIC DEFAULTS APPLIED", end='\n\n')
          print('****************************************************************************************************************************************', end='\n\n')
          print("> This plot shows a 2D SLICE of the 3D gravitational potential field by holding one axis CONSTANT.")
          print(f"> Constant Axis: {cax} | Horizontal (X-Axis): {hax} | Vertical (Y-Axis): {vax}")
          print("> This configuration is applied based on your slice selection and cannot be changed within this mode.", end='\n\n')
          print('****************************************************************************************************************************************', end='\n\n')
          time.sleep(1.5)

        # Assigning axes dynamically based on user's constant axis selection
        if constaxis=='x':
          defaxis('X','Y','Z')
          XPLOT=only_num("Enter the value of X where the slice is to be taken (X = constant): ", 'float')
          dispaxes=['Y','Z']
          varaxes=[yplot,zplot]=[None,None]
          VARAXES=[YPLOT,ZPLOT]=[None,None]

        elif constaxis=='y':
          defaxis('Y','X','Z')
          YPLOT=only_num("Enter the value of Y where the slice is to be taken (Y = constant): ", 'float')
          dispaxes=['X','Z']
          varaxes=[xplot,zplot]=[None,None]
          VARAXES=[XPLOT,ZPLOT]=[None,None]

        else:
          defaxis('Z','X','Y')
          ZPLOT=only_num("Enter the value of Z where the slice is to be taken (Z = constant): ", 'float')
          dispaxes=['X','Y']
          varaxes=[xplot,yplot]=[None,None]
          VARAXES=[XPLOT,YPLOT]=[None,None]

        # Creating empty lists which would store the start and terminal points for the remaining two axis for potential visualization
        s,e=[],[]
        while True:
          # Asking user for the start and end point for the remaining two axis in the 2D slice
          for i in range(2):
            spt=only_num(f"Enter the start point at which potential is to be visualized wrt to origin along {dispaxes[i]} axis:",'float')
            tpt=only_num(f"Enter the terminal point at which potential is to be visualized wrt to origin along {dispaxes[i]} axis:",'float')
            # Ensuring that the start point lies before the terminal point along the chosen axis
            if spt<tpt:
              s.append(spt)
              e.append(tpt)
              break
            else:
              print("The start point MUST ALWAYS be < than the terminal point !!!",end='\n\n')
              print("Please TRY AGAIN !",end='\n\n')
              time.sleep(1.5)
              continue

        # Asking user for grid resolution
        while True:
          h=only_num("Enter the no.of points in between the start and the terminal at which the potential is to be visualized:",'int')
          if h<2:
            print("No. of evaluation points must be at least 2 to generate a field plot !!!")
            print("Please TRY AGAIN !",end='\n\n')
            continue
          else:
            break

        # Generate equally spaced grid points for horizontal and vertical axes
        varaxes[0]=np.linspace(s[0],e[0],h)
        varaxes[1]=np.linspace(s[1],e[1],h)

        # Perfroming a meshgrid to create 2D coordinate matrices required by contour/contourf
        VARAXES[0],VARAXES[1]=np.meshgrid(varaxes[0],varaxes[1],indexing='ij')

        # Creating an empty array which would store the net potential for each point on the grid
        GPPLOT=np.zeros_like(VARAXES[0])

        # Asking user to enter a softening constant and also ensuring that it is >0
        while True:
          eps=only_num("Enter a small softening constant ε to avoid singularities (recommended: 1e-6 (i.e., 10^-6) to 1e-2 (i.e., 10^-2), must be > 0): ",'float')
          if eps>0:
            break
          else:
            print("The value of ε MUST ALWAYS be > 0 !!!",end='\n\n')
            print("Please TRY AGAIN !",end='\n\n')
            continue

        # Calculating the potential for each point by each source mass and appending it to GPPLOT
        for i in range(len(M)):
          gpplot=(-(G)*(M[i]))/((XPLOT-X_M[i])**2+(YPLOT-Y_M[i])**2+(ZPLOT-Z_M[i])**2+(eps)**2)**(0.5)
          GPPLOT+=gpplot

        # clc() allows user to set the contour levels
        if vizch=='2' or vizch=='3':
          clc()

        # common() allows user to set certain figure metadata
        common()

        # Asking user for a label for the colorbar
        if vizch=='1' or vizch=='3':
          cblabel=input("Label for colorbar (e.g., 'Potential'): ")

        # Constructing the graph according to user's choice
        if vizch=='1':
          graph=plt.imshow(GPPLOT,cmap='magma',origin='lower',extent=[s[0],e[0],s[1],e[1]])
        elif vizch=='2':
          graph=plt.contour(VARAXES[0],VARAXES[1],GPPLOT,levels=lvl,cmap='magma')
        else:
          graph=plt.contourf(VARAXES[0],VARAXES[1],GPPLOT,levels=lvl,cmap='magma')

        # Displaying colorbar or labels depending on plot type
        if vizch=='1' or vizch=='3':
          plt.colorbar(graph,label=cblabel)
        else:
          plt.clabel(graph,inline=False,fontsize=8,fmt='%.1f')

        # Setting plot title and axis labels
        plt.title(ptitle)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        # showsave() allows the plot to be displayed and saved
        showsave()

#####################################################################################################################################################################################

      elif vizch=='4':
        print("Are you sure? You would return back to the Main Menu.",end='\n\n')
        vizsure=input("If you still want to CONTINUE with visualization process, enter (y / Y / yes / YES): ")
        if vizsure in ['y','Y','yes','YES']:
          continue
        else:
          break

#####################################################################################################################################################################################

      else:
        print("INVALID choice from VISUALIZATION MENU !!! Please ENTER a VALID choice !!!",end='\n\n')

#####################################################################################################################################################################################
#####################################################################################################################################################################################

  # If the user wants to termiante the session
  elif ch=='3':
    print("Are you sure you want to TERMINATE the SESSION and EXIT the Xplorer?",end='\n\n')

    mainsure=input("If you still want to continue with session, enter (y / Y / yes / YES): ")
    if mainsure in ['y','Y','yes','YES']:
      continue
    else:
      print("Thank you for using GPX (Gravitational Potential Xplorer) !!")
      print("Potential mapped! Space explored! See you next orbit!! :)",end='\n\n')
      time.sleep(1)
      print("Your session is being terminated...")
      time.sleep(1)
      print(".....")
      time.sleep(1)
      print("Your session has been SUCCESSFULLY TERMINATED !!!",end='\n\n')
      print('****************************************************************************************************************************************',end='\n\n')
      break

#####################################################################################################################################################################################
#####################################################################################################################################################################################

  # If the user enters an invalid choice from the main menu
  else:
    print("INVALID choice from the Main Menu !!! Please enter a VALID choice !")

#####################################################################################################################################################################################
#####################################################################################################################################################################################

