'''
createVideoSegments V10

Edits video into separate video segments from a tagged text script. Works for any transcript format. Insert these tags into your transcript file in this exact format
Requires ffmpeg.exe to be installed in path or in the same directory as this program (www.ffmpeg.org)
00:15:10:START_SEG: Title Of Segment
00:19:33:STOP_SEG

The first tag tells the program where to start the video segment and gives it the name "Title_Of_Segment", replacing spaces with '_'. The second tag tells the program where to stop the video segment. Make sure there are not any extra spaces after STOP_SEG or else it will not recognize the command!
If the clip starts with a slide with no motion, set "RE_ENCODE=1". It will recode the segment, so capture the first slide, but it will take a lot longer to process (e.g. twice as long as the video play time!).

v10 9.01.21 Added carrage return to end of script in case there wasn't one, vital for parcing script
v9 8.18.21 Checks to see if files exist, allow spaces after "STOP_SEG"
v8 8.01.21 Add lead in/out before and after video edit

Tom Zimmerman, IBM Research-Almaden
This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction.
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation. 
'''
import subprocess
import os.path
from os import path

############## FILE LOCATIONS #################
#scriptFile=r'C:\Users\ThomasZimmerman\Videos\CCC_SFSU_Pipeline_Fall2020_CSC698\9_9\9_9_Detection_Part2.txt'     # script with time coded tags instrucing program how to break video into segments
#videoIn=r'C:\Users\ThomasZimmerman\Videos\CCC_SFSU_Pipeline_Fall2020_CSC698\9_9\GMT20200909-193639_Temp-for-C_avo_640x360.mp4'          # original video to be broken up into segments
#videoOutDir=r'C:\Users\ThomasZimmerman\Videos\CCC_SFSU_Pipeline_Fall2020_CSC698\9_9\TomFaceSegments\\'    # where to put the segments

scriptFile=r'C:\Users\ThomasZimmerman\Videos\microscope\Hologram\ShortHoloVideo\M6_3sec.txt'     # script with time coded tags instrucing program how to break video into segments
videoIn=r'C:\Users\ThomasZimmerman\Videos\microscope\Hologram\ShortHoloVideo\M6.mp4'          # original video to be broken up into segments
videoOutDir=r'C:\Users\ThomasZimmerman\Videos\microscope\Hologram\ShortHoloVideo\edit\\'    # where to put the segments

############ USER SETTINGS #################
RE_ENCODE=0     # set to 1 to re-encode video segments, slower but necessary if no movement in beginning of video (e.g. just static opening slide)
CREATE_VIDEO=1  # set to 1 to enable creation of video, set to 0 to debug program without creating videos
LEAD_TIME=0    # time added before and after video clip (seconds) MUST BE LESS THAN 60 ! ! !

############ FUNCTIONS #############
def checkScript(script):
    scriptList=[]
    startSeg=0; stopSeg=0; startCut=0; stopCut=0; segName=''
    segStatus='stop'; cutStatus='stop'; scriptStatus='Pass'
    for i in range(len(script)):
        a=script[i]
        if ':' in a:
            tc=a[:-1]
            b=tc.split(':') # get rid of carrage return and split time code with ':'
            if len(b)>=4:
                command=b[3]
                ts=b[0]+':'+b[1]+':'+b[2]
                if command=='START_SEG':
                    if segStatus=='start':
                        scriptStatus='START_SEG without STOP_SEG at timestamp ' + ts
                        break
                    segStatus='start'
                    if len(b)==5:
                        segName=b[4]
                    else:
                        scriptStatus='Missing segment name at timestamp ' + ts
                        break
                    scriptList.append(tc)
                elif 'STOP_SEG' in command:
                    if segStatus=='stop':
                        scriptStatus='STOP_SEG without START_SEG at timestamp '+ ts
                        break
                    segStatus='stop'
                    scriptList.append(tc)
    return(scriptStatus,scriptList)

def createVideo(segName,startT,stopT):
    # remove forbidden characters from segment name
    segName=segName.replace(' ','_')  
    segName=segName.replace('.','')  
    segName=segName.replace('/','_')  
    segName=segName.replace('\\','_')  
    
    videoName=segName+'.mp4'
    videoFile=videoOutDir+videoName 
    if RE_ENCODE:
        print('Creating segment (RE-ENCODED):',videoName,'start:',startT,'stop:',stopT)
        subprocess.call(['ffmpeg.exe','-i', videoIn, '-ss',startT,'-to',stopT, videoFile]) # re-encodes, use if static image like a slide
    else:
        print('Creating segment:',videoName,'start:',startT,'stop:',stopT)
        subprocess.call(['ffmpeg.exe','-i', videoIn, '-ss',startT,'-to',stopT,'-c:v','copy','-c:a','copy', videoFile]) # does not re-encode
    return

def adjustTimeIn(b): # correct time for lead in
    b0=int(b[0]); b1=int(b[1]); b2=int(b[2]);

    b2-=LEAD_TIME
    if b2<0:
        b2+=60
        b1-=1
        if b1<0:
            b1+=60
            b0-=1
            if b0<0:
                b0=0; b1=0; b2=0; # min time is 0:0:0
    b0=str(b0); b1=str(b1); b2=str(b2)

    # add leading zero if missing
    if len(b0)==1:
        b0='0'+b0
    if len(b1)==1:
        b1='0'+b1
    if len(b2)==1:
        b2='0'+b2

    ts=b0+':'+b1+':'+b2
    return(ts)
        
def adjustTimeOut(b): # correct time for lead out
    b0=int(b[0]); b1=int(b[1]); b2=int(b[2]);

    b2+=LEAD_TIME
    if b2>59:
        b2-=60
        b1+=1
        if b1>59:
            b1-=60
            b2+=1
    b0=str(b0); b1=str(b1); b2=str(b2)

    # add leading zero if missing
    if len(b0)==1:
        b0='0'+b0
    if len(b1)==1:
        b1='0'+b1
    if len(b2)==1:
        b2='0'+b2

    ts=b0+':'+b1+':'+b2
    return(ts)

def processScript(scriptList):
    s=scriptList # so I don't have to type so much
    segName=''; startT=0; stopT=0;  

    if CREATE_VIDEO:
        print('\nCreating video segments',s)
    else:
        print('\nVerifying video segments')
    for i in range(len(s)):
        b=s[i].split(':') # get rid of carrage return and split time code with ':'
        command=b[3]
        #ts=b[0]+':'+b[1]+':'+b[2]
        if command=='START_SEG':
            ts=adjustTimeIn(b)      # subtract LEAD_TIME
            cutList=[] # clear in case this seg has cuts
            segName=b[4]
            startT=ts
            cutCount=0
        elif 'STOP_SEG' in command:
            ts=adjustTimeOut(b)     # add LEAD_TIME
            stopT=ts
            if CREATE_VIDEO:
                createVideo(segName,startT,stopT)   #No cuts so save entire video
            else:
                print(segName,startT,stopT)            
    return

############# MAIN ##################
# Load text from file
error=0
if path.exists(scriptFile)==0:
    print('Error: Can not find script file',scriptFile,'\n')
    error=1
if path.exists(videoIn)==0:
    print('Error: Can not find source video',videoIn,'\n')
    error=1
if path.exists(videoOutDir)==0:
    print('Error: Can not find video segment directory',videoOutDir,'\n')
    error=1

if error==0:
    print('Videos will be made with lead in/out time of',LEAD_TIME,'seconds')
    print('\nOpening script',scriptFile)
    file = open(scriptFile,mode='r')
    script = file.readlines()
    file.close()

    # add carrage return to end of file, in case it doesn't have one (essential for parsing file)
    c=len(script)
    script[c-1]=script[c-1]+'\n'   
    
    # Check script
    print('\nChecking script for format...')
    (scriptStatus,scriptList)=checkScript(script)
    print(scriptStatus)

    # Create segments if script is error-free
    if scriptStatus=='Pass':
        processScript(scriptList)
        
    print('Program finished, bye!')
else:
    print('Please fix errors and try again, bye!')
    
