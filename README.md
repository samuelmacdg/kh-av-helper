# Pre-requisites
### Python 3.6
OBS requires Python 3.6 installation for scripts written in Python. Other versions won't work. You can download Python 3.6 from the Python website or on this [link](https://www.python.org/downloads/release/python-360/)

Make sure to take note of the installation folder while doing the installation. If you forgot where it's placed, the default installation folder is at `C:\Users\*Your Username*\AppData\Local\Programs\Python\Python36`

### Song Sources
Create 3 different media sources for the opening, middle song, and closing song. This is required by the script.

### Timer Sources
The script uses a text source to display the timer. Prepare a text source which shall serve as the timer. 

### Songs Folder
Download all the songs used for the meetings (video). Make sure that all songs are in the same resolution (preferrably 720p) and same language. You can also download all song using the JW Library app.

# Download
Download the latest zip from the Release and extract to the directory of your choice. Go to the Releases page by clicking on [this link](https://github.com/samuelmacdg/kh-av-helper/releases/).

# Installation
Launch OBS and go to *Tools > Scripts > Python Settings*. Click *Browse* and select the Python 3.6 installation directory. 

Go to the Scripts tab and click on the plus icon and select the `kh-av-helper.py` file. Click Fetch Data so the script can retrieve the meeting data for the current and subsequent meetings. You can also use this button to retrieve the current songs and timers. It will only connect to the server once every 2 months. This connects to a personal server and not on the WOL website as it would be against the site's terms of use.

# Configuration
### Songs
You can access the song settings on the *Song Settings* group.
##### Songs Directory
Select the directory where the songs are stored. This could be your JW Library media folder if you chose to download all the songs using the JW Library App. Make sure that the files are not renamed.
##### Language Code
The Language Code is the publication language code for the video. You will see this at the first underscore after the publication code. Ex.: TG for Tagalog, E for English. Make sure that it is in all caps.
##### Song Sources
Select the respective media sources for the opening, middle, and closing song. An option for those using only one source will be available in the future.

### Timer
You can access the song settings on the *Song Settings* group. Other settings can also be found on the Timer group.
##### Timer Text Source
Select the text source that will be used to display the timer. Configure the size and style of this source on OBS. Please note that the color will be overriden.
##### Timer Colors
-Clock Color - color used for the standby clock
-Default Color - color used for the timer and countdown
-Warning Color - color used when the timer is less than 30 seconds
-Overtime Color - color used time limit has exceeded
##### Count-up After Time Ends
This is important for timers which needs to show the overtime
##### Persist Student's Time
This only works for TMS parts. The timer will persist for 1 minute after being stopped. This allows the counselor to see the student's time as well as an indication that the 1 minute alloted for counsel is up.
##### CO's Visit
This changes the times to fit the additional talks during CO's Visit. Please press Fetch Data to reload the CO's Visit Time.

# Use
Access the script settings, set songs, set time, and other things by going to *Tools > Scripts > kh-av-helper.py*

# Bugs
-When closing OBS, a message appears that "OBS has crashed".
-You can file a bug report on the Issue tab if you found any bug or has any suggestion.
