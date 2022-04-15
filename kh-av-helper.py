import datetime
from turtle import update
import obspython as S
import json
import threading
from urllib.request import urlopen
from pathlib import Path


class Timer:
    time_start = datetime.datetime.now()
    time_end = datetime.datetime.now()
    timer_persist = datetime.datetime.now()
    active = False
    status = -1
    handler = None
    isTMS = False
    isPersisting = False
    isStopWatch = False


class Data:
    meeting_data = None
    settings = None


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def script_description():
    return "This script helps you setup your timer and songs for your KH AV using OBS"


def script_load(settings):
    Data.meeting_data = get_meeting_data()
    if Timer.handler == None:
        Timer.handler = RepeatedTimer(0.3, update_timer)
    print("script_load")

def script_unload():
    Timer.handler.stop()


def script_defaults(settings):
    S.obs_data_set_default_int(settings, "timer_text_clock_color", 4294967295)
    S.obs_data_set_default_int(
        settings, "timer_text_default_color", 4278255360)
    S.obs_data_set_default_int(
        settings, "timer_text_warning_color", 4278255615)
    S.obs_data_set_default_int(
        settings, "timer_text_overtime_color", 4278190335)

    S.obs_data_set_default_bool(settings, "timer_idle_clock", True)
    S.obs_data_set_default_bool(settings, "timer_countup", True)
    S.obs_data_set_default_bool(settings, "timer_stopwatch", False)
    S.obs_data_set_default_bool(settings, "timer_co_visit", False)

    S.obs_data_set_default_string(settings, "songs_lang", "TG")
    S.obs_data_set_default_string(settings, "songs_reso", "720p")


def script_update(settings):
    print("script_update")
    if Timer.handler == None:
        Timer.handler = RepeatedTimer(0.3, update_timer)
    if Data.meeting_data == None:
        Data.meeting_data = get_meeting_data()
    Data.settings = settings


def get_meeting_data():
    p = Path(__file__).absolute()
    has_existing_data = False
    today = datetime.date.today()

    day_num = int(today.strftime('%w'))
    adjuster = day_num
    if day_num == 0:
        adjuster = 6
    else:
        adjuster = (day_num - 1)

    today = today + datetime.timedelta(days=(-1 * adjuster))

    week_num = int(today.strftime("%V"))
    year = today.year

    try:
        with open(p.parent / "meeting_data.json", "r") as midweek_file:
            midweek_text = midweek_file.read()
            meeting_data = {}

            if midweek_text == "":
                has_existing_data = False
            else:
                try:
                    meeting_data = json.loads(midweek_text)
                    try:
                        return_data = meeting_data[str(year)][str(week_num)]
                        has_existing_data = True
                        print(return_data)
                        return return_data
                    except:
                        has_existing_data = False
                except:
                    has_existing_data = False
    except:
        print("no file yet")

    if not has_existing_data:
        with open(p.parent / "meeting_data.json", "w") as midweek_file:
            meeting_data = json.loads(urlopen('https://kh-av-helper-sam.glitch.me/').read().decode("utf-8"))
            midweek_file.write(json.dumps(meeting_data))
            print(meeting_data)
            try:
                return_data = meeting_data[str(year)][str(week_num)]
                print(return_data)
                return return_data
            except:
                return {
                    "year": str(year),
                    "week": str(week_num),
                    "from_online": False,
                    "mw_songs": [
                        1,
                        1,
                        1
                    ],
                    "mw_times": [
                        {
                            "title": "Opening Comments",
                            "duration": 1,
                            "isTMS": False
                        },
                        {
                            "title": "Treasures Talk",
                            "duration": 10,
                            "isTMS": False
                        },
                        {
                            "title": "Spiritual Gems",
                            "duration": 10,
                            "isTMS": False
                        },
                        {
                            "title": "Bible Reading",
                            "duration": 4,
                            "isTMS": True
                        },
                        {
                            "title": "Apply Yourself 1",
                            "duration": 5,
                            "isTMS": True
                        },
                        {
                            "title": "Apply Yourself 2",
                            "duration": 5,
                            "isTMS": True
                        },
                        {
                            "title": "Apply Yourself 3",
                            "duration": 5,
                            "isTMS": True
                        },
                        {
                            "title": "Living As Christians 1",
                            "duration": 15,
                            "isTMS": False
                        },
                        {
                            "title": "Living As Christians 2",
                            "duration": 15,
                            "isTMS": False
                        },
                        {
                            "title": "Congregation Bible Study",
                            "duration": 30,
                            "isTMS": False
                        },
                        {
                            "title": "Concluding Comments",
                            "duration": 3,
                            "isTMS": False
                        }
                    ],
                    "wt_songs": [
                        1,
                        1
                    ]
                }


def get_meeting_times():
    today = datetime.date.today()
    day_of_the_week = int(today.strftime("%w"))
    covisit = S.obs_data_get_bool(Data.settings, "timer_co_visit")

    if day_of_the_week >= 1 and day_of_the_week <= 5:
        if covisit:
            meeting_times = []
            for time_data in Data.meeting_data["mw_times"]:
                if time_data["title"] == "Congregation Bible Study":
                    meeting_times.append({
                        "title": "Service Talk",
                        "duration": 30,
                        "isTMS": False
                    })
                else:
                    meeting_times.append(time_data)
            return meeting_times
        else:
            return Data.meeting_data["mw_times"]
    elif covisit:
        return [{
            "title": "Public Talk",
            "duration": 30,
            "isTMS": False
        },
            {
            "title": "Watchtower Study",
            "duration": 30,
            "isTMS": False
        },
            {
            "title": "Service Talk",
            "duration": 30,
            "isTMS": False
        }]
    else:
        return [{
            "title": "Public Talk",
            "duration": 30,
            "isTMS": False
        },
            {
            "title": "Watchtower Study",
            "duration": 60,
            "isTMS": False
        }]


def auto_fill(props, prop):
    Data.meeting_data = get_meeting_data()
    md = Data.meeting_data
    today = datetime.date.today()
    day_of_the_week = int(today.strftime("%w"))

    timer_selector = S.obs_properties_get(props, "timer_selector")
    S.obs_property_list_clear(timer_selector)
    manual_timer_obj = {
        "title": "Manual Timer",
        "duration": -1,
        "isTMS": False
    }
    meeting_countdown_obj = {
        "title": "Meeting Countdown",
        "duration": -2,
        "isTMS": False
    }
    S.obs_property_list_add_string(timer_selector, "Manual Timer", json.dumps(manual_timer_obj))
    S.obs_property_list_add_string(timer_selector, "Meeting Countdown", json.dumps(meeting_countdown_obj))
    for x in get_meeting_times():
        S.obs_property_list_add_string(timer_selector, x["title"] + " (" + str(
            x["duration"]) + " min" + ("s" if x["duration"] > 1 else "") + ")", json.dumps(x))

    if day_of_the_week > 0 and day_of_the_week < 6:
        S.obs_data_set_int(Data.settings, "song_opening", md["mw_songs"][0])
        S.obs_data_set_int(Data.settings, "song_middle", md["mw_songs"][1])
        S.obs_data_set_int(Data.settings, "song_closing", md["mw_songs"][2])
    else:
        S.obs_data_erase(Data.settings, "song_opening")
        S.obs_data_set_int(Data.settings, "song_middle", md["wt_songs"][0])
        S.obs_data_set_int(Data.settings, "song_closing", md["wt_songs"][1])
    return True


def set_source_setting_str(source_name, setting_name, value):
    source = S.obs_get_source_by_name(source_name)
    setting = S.obs_data_create()
    S.obs_data_set_string(setting, setting_name, value)
    S.obs_source_update(source, setting)
    S.obs_data_release(setting)
    S.obs_source_release(source)


def set_source_setting_int(source_name, setting_name, value):
    source = S.obs_get_source_by_name(source_name)
    setting = S.obs_data_create()
    S.obs_data_set_int(setting, setting_name, value)
    S.obs_source_update(source, setting)
    S.obs_data_release(setting)
    S.obs_source_release(source)

def nextTimer(selected, props):
    selector = S.obs_properties_get(props, "timer_selector")
    count = S.obs_property_list_item_count(selector)
    sel_string = json.dumps(selected)
    manual_str = S.obs_property_list_item_string(selector, 0)

    for idx in range(count):
        val = S.obs_property_list_item_string(selector, idx)
        if val == sel_string:
            break

    print(idx)

    if idx == (count - 1):
        S.obs_data_set_string(Data.settings, "timer_selector", manual_str)
    else:
        next_val = S.obs_property_list_item_string(selector, idx + 1)
        S.obs_data_set_string(Data.settings, "timer_selector", next_val)


def timer_start_callback(props, prop):
    if Timer.handler == None:
        Timer.handler = RepeatedTimer(0.8, update_timer)
    timer_names = ["timer_start", "timer_m_start"]
    persistTime = S.obs_data_get_bool(Data.settings, "persist_student_time")
    timer_obj = json.loads(S.obs_data_get_string(Data.settings, "timer_selector"))
    stopwatch_mode = S.obs_properties_get(props, "timer_stopwatch")


    if Timer.active:
        S.obs_property_set_enabled(stopwatch_mode, True)
        for timer_name in timer_names:
            timer_button = S.obs_properties_get(props, timer_name)
            S.obs_property_set_description(timer_button, "Start")
                

        if(Timer.isTMS and persistTime and not Timer.isPersisting):
            delta = datetime.timedelta(minutes=1)
            Timer.timer_persist = datetime.datetime.now() + delta
            Timer.isPersisting = True
            Timer.active = False
        else:
            set_timer_status(0)
            Timer.active = False
            if Timer.isPersisting:
                Timer.isPersisting = False

        if timer_obj["duration"] != -1:
            nextTimer(timer_obj, props)
            update_time_menu(props, prop, Data.settings)

    else:
        S.obs_property_set_enabled(stopwatch_mode, False)
        if Timer.isPersisting:
            Timer.isPersisting = False
        for timer_name in timer_names:
            timer_button = S.obs_properties_get(props, timer_name)
            if(timer_obj["isTMS"] and persistTime):
                S.obs_property_set_description(timer_button, "Persist")
            else:
                S.obs_property_set_description(timer_button, "Stop")
        
        duration = timer_obj["duration"]
        delta = None

        hours = S.obs_data_get_int(Data.settings, "timer_m_hour")
        minutes = S.obs_data_get_int(Data.settings, "timer_m_mins")
        seconds = S.obs_data_get_int(Data.settings, "timer_m_secs")

        a_minutes = S.obs_data_get_int(Data.settings, "timer_a_mins")

        if duration == -1:
            delta = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        elif duration == -2:
            delta = datetime.datetime.now().replace(hour=hours, minute=minutes, second=seconds) - datetime.datetime.now()
        elif duration > 0:
            delta = datetime.timedelta(minutes=a_minutes)
            
        Timer.time_start = datetime.datetime.now()
        Timer.active = True
        Timer.isTMS = timer_obj["isTMS"]
        set_timer_status(1)
        Timer.time_end = Timer.time_start + delta
    return True


def set_timer_status(status):
    if Timer.status != status:
        color_setting_name = ""

        if status == 1:
            color_setting_name = "timer_text_default_color"
        elif status == 2:
            color_setting_name = "timer_text_warning_color"
        elif status == 3:
            color_setting_name = "timer_text_overtime_color"
        else:
            color_setting_name = "timer_text_clock_color"

        clock_color = S.obs_data_get_int(Data.settings, color_setting_name)
        timer_source = S.obs_data_get_string(
            Data.settings, "timer_text_source")
        set_source_setting_int(timer_source, "color", clock_color)
        Timer.status = status


def update_timer():
    now = datetime.datetime.now()

    if Timer.isPersisting:
        if now < Timer.timer_persist:
            return
        else:
            Timer.isPersisting = False
            Timer.active = False
            set_timer_status(0)

    timer_source = S.obs_data_get_string(Data.settings, "timer_text_source")

    if not Timer.active:
        timer_idle_clock = S.obs_data_get_bool(
            Data.settings, "timer_idle_clock")
        if Timer.status != 0:
            clock_color = S.obs_data_get_int(
                Data.settings, "timer_text_clock_color")
            timer_source = S.obs_data_get_string(
                Data.settings, "timer_text_source")
            set_source_setting_int(timer_source, "color", clock_color)
            Timer.status = 0
        time_text = ""
        if timer_idle_clock:
            time_text = now.strftime('%I:%M %p')
        set_source_setting_str(timer_source, "text", time_text)
        return
    else:
        delta = datetime.timedelta(seconds=0)

        if Timer.isStopWatch:
            delta = now - Timer.time_start
            if Timer.status != 1:
                default_color = S.obs_data_get_int(
                    Data.settings, "timer_text_default_color")
                set_source_setting_int(
                    timer_source, "color", default_color)
                Timer.status = 1

        elif Timer.time_end > now:
            delta = Timer.time_end - now
            if(delta.seconds <= 30):
                if Timer.status != 2:
                    warning_color = S.obs_data_get_int(
                        Data.settings, "timer_text_warning_color")
                    set_source_setting_int(
                        timer_source, "color", warning_color)
                    Timer.status = 2
        else:
            delta = now - Timer.time_end
            count_up = S.obs_data_get_bool(Data.settings, "timer_countup")
            if count_up:
                if Timer.status != 3:
                    overtime_color = S.obs_data_get_int(
                        Data.settings, "timer_text_overtime_color")
                    set_source_setting_int(
                        timer_source, "color", overtime_color)
                    Timer.status = 3
            else:
                if Timer.status != 0:
                    clock_color = S.obs_data_get_int(
                        Data.settings, "timer_text_clock_color")
                    timer_source = S.obs_data_get_string(
                        Data.settings, "timer_text_source")
                    set_source_setting_int(timer_source, "color", clock_color)
                    Timer.status = 0
                Timer.active = False
                return

        secs = delta.seconds
        if secs == 0 and not Timer.isStopWatch:
            if Timer.status != 3:
                overtime_color = S.obs_data_get_int(
                    Data.settings, "timer_text_overtime_color")
                set_source_setting_int(timer_source, "color", overtime_color)
                Timer.status = 3
        time_text = str(int(secs / 60)) + ":" + '%02d' % (int(secs % 60),)
        set_source_setting_str(timer_source, "text", time_text)


def set_song_sources(props, prop):
    songs_folder = S.obs_data_get_string(Data.settings, "songs_path")
    song_opening = S.obs_data_get_int(Data.settings, "song_opening")
    song_middle = S.obs_data_get_int(Data.settings, "song_middle")
    song_closing = S.obs_data_get_int(Data.settings, "song_closing")
    songs_opening_source = S.obs_data_get_string(
        Data.settings, "songs_opening_source")
    songs_middle_source = S.obs_data_get_string(
        Data.settings, "songs_middle_source")
    songs_closing_source = S.obs_data_get_string(
        Data.settings, "songs_closing_source")
    songs_lang = S.obs_data_get_string(Data.settings, "songs_lang")
    songs_reso = S.obs_data_get_string(Data.settings, "songs_reso")

    def get_song_path(song_num):
        return songs_folder + "/sjjm_" + songs_lang + "_" + '%03d' % (song_num,) + "_" + songs_reso + ".mp4"

    print(songs_folder + "/" + get_song_path(song_opening))

    set_source_setting_str(songs_opening_source,
                           "local_file", get_song_path(song_opening))
    set_source_setting_str(songs_middle_source,
                           "local_file", get_song_path(song_middle))
    set_source_setting_str(songs_closing_source,
                           "local_file", get_song_path(song_closing))

def set_manual_timer_visibility(props, is_visible):
    m_hour = S.obs_properties_get(props, "timer_m_hour")
    m_mins = S.obs_properties_get(props, "timer_m_mins")
    m_secs = S.obs_properties_get(props, "timer_m_secs")
    a_mins = S.obs_properties_get(props, "timer_a_mins")

    for prop in [m_hour, m_mins, m_secs]:
        S.obs_property_set_visible(prop, is_visible)

    S.obs_property_set_visible(a_mins, not is_visible)

def stopwatch_callback(props, prop, settings):
    stopwatch_mode = S.obs_data_get_bool(settings, "timer_stopwatch")

    m_hour = S.obs_properties_get(props, "timer_m_hour")
    m_mins = S.obs_properties_get(props, "timer_m_mins")
    m_secs = S.obs_properties_get(props, "timer_m_secs")
    a_mins = S.obs_properties_get(props, "timer_a_mins")
    select = S.obs_properties_get(props, "timer_selector")

    print(stopwatch_mode)

    if stopwatch_mode:
        for prop in [m_hour, m_mins, m_secs, a_mins, select]:
            S.obs_property_set_visible(prop, not stopwatch_mode)
    else:
        S.obs_property_set_visible(select, not stopwatch_mode)
        update_time_menu(props, prop, settings)

    Timer.isStopWatch = S.obs_data_get_bool(settings, "timer_stopwatch")
    return True

def update_time_menu(props, prop, settings):
    timer_obj = json.loads(S.obs_data_get_string(Data.settings, "timer_selector"))
    duration = timer_obj["duration"]

    if duration > 0:
        set_manual_timer_visibility(props, False)
    else:
        set_manual_timer_visibility(props, True)

    if duration > 0:
        S.obs_data_set_int(Data.settings, "timer_a_mins", duration)

    return True

def persist_callback(props, prop, settings):
    Timer.persistTime = S.obs_data_get_bool(settings, "persist_student_time")
    return True

#def update_mode(props, prop, settings):
#    mode = S.obs_data_get_string(settings, "meeting_mode")
#    return True

def script_properties():
    props = S.obs_properties_create()

    auto_data_fetch = S.obs_properties_add_button(
        props, "auto_data_fetch", "Fetch Data", auto_fill)
    #meeting_mode = S.obs_properties_add_list(props, "meeting_mode", "Meeting", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    #S.obs_property_list_add_string(meeting_mode, "Weekday", "Weekday")
    #S.obs_property_list_add_string(meeting_mode, "Weekend", "Weekend")
    #S.obs_property_set_modified_callback(meeting_mode, update_mode)

    # Timer Menu
    props_timer = S.obs_properties_create()
    timer_stopwatch = S.obs_properties_add_bool(props_timer, "timer_stopwatch", "Stopwatch Mode")
    S.obs_property_set_modified_callback(timer_stopwatch, stopwatch_callback)
    timer_selector = S.obs_properties_add_list(props_timer, "timer_selector", "Timer Selector", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    manual_timer_obj = {
        "title": "Manual Timer",
        "duration": -1,
        "isTMS": False
    }
    meeting_countdown_obj = {
        "title": "Meeting Countdown",
        "duration": -2,
        "isTMS": False
    }
    S.obs_property_list_add_string(timer_selector, "Manual Timer", json.dumps(manual_timer_obj))
    S.obs_property_list_add_string(timer_selector, "Meeting Countdown", json.dumps(meeting_countdown_obj))
    for x in get_meeting_times():
        S.obs_property_list_add_string(timer_selector, x["title"] + " (" + str(
            x["duration"]) + " min" + ("s" if x["duration"] > 1 else "") + ")", json.dumps(x))
    S.obs_property_set_modified_callback(timer_selector, update_time_menu)
    #timer_start = S.obs_properties_add_button(props_timer, "timer_start", "Start/Stop", timer_start_callback)
    timer_a_mins = S.obs_properties_add_int(props_timer, "timer_a_mins", "Minutes", 0, 120, 1)
    S.obs_property_set_visible(timer_a_mins, False)
    timer_m_hour = S.obs_properties_add_int(props_timer, "timer_m_hour", "Hour", 0, 24, 1)
    timer_m_mins = S.obs_properties_add_int(props_timer, "timer_m_mins", "Minutes", 0, 60, 1)
    timer_m_secs = S.obs_properties_add_int(props_timer, "timer_m_secs", "Seconds", 0, 60, 1)
    timer_m_start = S.obs_properties_add_button(props_timer, "timer_m_start", "Start/Stop", timer_start_callback)
    if(Timer.handler == None or Timer.active == False):
        S.obs_property_set_description(timer_m_start, "Start")
    else:
        S.obs_property_set_description(timer_m_start, "Stop")
    timer_countup = S.obs_properties_add_bool(props_timer, "timer_countup", "Count-Up After Time Ends")
    persist_student_time = S.obs_properties_add_bool(props_timer, "persist_student_time", "Persist Student Time")
    S.obs_property_set_modified_callback(persist_student_time, persist_callback)
    timer_co_visit = S.obs_properties_add_bool(props_timer, "timer_co_visit", "CO's Visit")
    S.obs_properties_add_group(props, "timer_menu", "Timer", S.OBS_GROUP_NORMAL, props_timer)

    # Song Menu
    props_song = S.obs_properties_create()
    song_opening = S.obs_properties_add_int(props_song, "song_opening", "Opening Song", 1, 151, 1)
    song_middle = S.obs_properties_add_int(props_song, "song_middle", "Middle Song", 1, 151, 1)
    song_closing = S.obs_properties_add_int(props_song, "song_closing", "Closing Song", 1, 151, 1)
    song_set = S.obs_properties_add_button(props_song, "song_set", "Set Songs", set_song_sources)
    S.obs_properties_add_group(props, "song_menu", "Songs", S.OBS_GROUP_NORMAL, props_song)

    text_sources = []
    video_sources = []

    sources = S.obs_enum_sources()
    for source in sources:
        source_type = S.obs_source_get_unversioned_id(source)
        source_name = S.obs_source_get_name(source)
        if source_type == "text_gdiplus":
            text_sources.append(source_name)
        elif source_type == "ffmpeg_source":
            video_sources.append(source_name)

    # Song Settings
    settings_song = S.obs_properties_create()
    songs_path = S.obs_properties_add_path(settings_song, "songs_path", "Songs Directory", S.OBS_PATH_DIRECTORY, "", "")
    songs_lang = S.obs_properties_add_text(settings_song, "songs_lang", "Language Code", S.OBS_TEXT_DEFAULT)
    songs_reso = S.obs_properties_add_list(settings_song, "songs_reso", "Songs Resolution", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    songs_opening_source = S.obs_properties_add_list(settings_song, "songs_opening_source", "Opening Song Source", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    songs_middle_source = S.obs_properties_add_list(settings_song, "songs_middle_source", "Middle Song Source", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    songs_closing_source = S.obs_properties_add_list(settings_song, "songs_closing_source", "Closing Song Source", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    for prop in [songs_opening_source, songs_middle_source, songs_closing_source]:
        for source in video_sources:
            S.obs_property_list_add_string(prop, source, source)
    for reso in ["240p", "360p", "480p", "720p"]:
        S.obs_property_list_add_string(songs_reso, reso, "r" + reso)
    S.obs_properties_add_group(
        props, "song_settings", "Song Settings", S.OBS_GROUP_NORMAL, settings_song)

    # Timer Settings
    settings_timer = S.obs_properties_create()
    timer_text_source = S.obs_properties_add_list(settings_timer, "timer_text_source", "Timer Text Source", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    timer_text_clock_color = S.obs_properties_add_color(settings_timer, "timer_text_clock_color", "Timer Clock Color")
    timer_text_default_color = S.obs_properties_add_color(settings_timer, "timer_text_default_color", "Timer Default Color")
    timer_text_warning_color = S.obs_properties_add_color(settings_timer, "timer_text_warning_color", "Timer Warning Color")
    timer_text_overtime_color = S.obs_properties_add_color(settings_timer, "timer_text_overtime_color", "Timer Overtime Color")
    timer_idle_clock = S.obs_properties_add_bool(settings_timer, "timer_idle_clock", "Clock When Idle")
    for source in text_sources:
        S.obs_property_list_add_string(timer_text_source, source, source)
    S.obs_properties_add_group(
        props, "timer_settings", "Timer Settings", S.OBS_GROUP_NORMAL, settings_timer)

    return props
