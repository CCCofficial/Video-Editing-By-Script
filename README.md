# Video-Editing-By-Script

Edits video into separate video segments from a tagged text script. 
Works for any transcript format. Insert these tags into your transcript file in this exact format.
Requires ffmpeg.exe to be installed in path or in the same directory as this program (www.ffmpeg.org)

00:15:10:START_SEG: Title Of Segment   
00:19:33:STOP_SEG                   

The first tag tells the program where to start the video segment and gives it the name "Title_Of_Segment", replacing spaces with '_'.
The second tag tells the program where to stop the video segment. 
Make sure there are not any extra spaces after STOP_SEG or else it will not recognize the command!

Tom Zimmerman, IBM Research-Almaden
This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction.
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation. 

