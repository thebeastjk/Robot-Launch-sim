import math
import pandas as pd
import os


Speaker_Height_high = 6.90625
Speaker_Height_low = 6.5
Speaker_depth = 2 + (1/3)
global G
G = 32.174

restart = False
yes = "yes"
no = "no"

def Anglecalc(v = 0.0,x = 0.0,y = 0.0):
    temp =(v**2 - math.sqrt(v**4 - G * (G*x**2 + 2*y*v**2)))
    temp2 = math.degrees(math.atan(temp/(G*x)))
    return temp2



while True:
    launch_speed = float(input("Launch Speed: "))
    distance = float(input("Distance: "))
    distancetall = abs(distance - Speaker_depth)
    Height = float(input("Shooter height from floor: "))
    deltashort = abs(Speaker_Height_low - Height)
    deltatall = abs(Speaker_Height_high - Height)
    NoteShortDistance = float(abs(math.sqrt(pow(deltashort, 2) + pow(distance, 2))))
    NoteLongDistance = float(abs(math.sqrt(pow(deltatall,2) + pow(distancetall, 2))))
    try:
        ShortAngle = Anglecalc(v=launch_speed,x=distance,y=deltashort)
        LongAngle = Anglecalc(v=launch_speed, x=distancetall, y=deltatall)
        MiddleAngle = LongAngle - ((LongAngle - ShortAngle)/2)
        print(f"Angle needs to be between {ShortAngle:.2f} degrees and {LongAngle:.2f} degrees")
        print(f"The note will go between {NoteShortDistance:.2f} feet and {NoteLongDistance:.2f} feet") 
        print(f"To aim at the center: {MiddleAngle:.2f} degrees")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_exists = os.path.exists(f'{dir_path}/Save.csv')
        if file_exists == False:
            open(f'{dir_path}/Save.csv', 'w')
            df = pd.DataFrame.from_dict({'Velocity':[launch_speed], 'X':[distance], 'Y':[Height], 'Short Angle':[ShortAngle], 'Long Angle':[LongAngle]},orient = 'columns')
        else:
            df = pd.DataFrame.from_dict({'Velocity':[launch_speed], 'X':[distance], 'Y':[Height], 'Short Angle':[ShortAngle], 'Long Angle':[LongAngle]},orient = 'columns')
            df.columns = df.iloc[0]
            df = df.reindex(df.index.drop(0)).reset_index(drop=True)
        df.columns.name = None
        df.to_csv(path_or_buf=f'{dir_path}/Save.csv',float_format="%.3f",mode='a')

    except:
       ValueError
       print("You can't hit the target with that, try getting closer or raising the launch speed")
    
    
  
    
