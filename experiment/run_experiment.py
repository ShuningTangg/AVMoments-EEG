#!/usr/bin/env python

####import libraries：导入库
import sys,random,os,copy,time,json,numpy,cv2,psutil,gc
from psychopy import visual, core, event,monitors,parallel
from sys import maxsize
from math import atan,pi,sin, cos
from psychopy.visual.movies import MovieStim

# 检查并口设备
port = parallel.ParallelPort(address=0x3EFC) #创建并口对象

# 定义发送数据到并口设备
def send_triggers(value,duration=0.01):
    ## trigger 数字必须在0-255之间
    if not  0 <= value <= 255:
        raise ValueError("Trigger value 必须在 0-255 之间")
    port.setData(value)  #发trigger
    time.sleep(duration) #高电位持续时间
    port.setData(0)      #清零恢复低电平

#### Data manipulation functions####################################################
#get subject info：收集被试信息
def get_subj_info():
    subj_id = input("Subject ID: ")
    name = input("Subject Name: ")
    gender = input("Subject Gender (m/f): ")
    age = input("Subject Age: ")
    run = input("Run(0/1/2/3/4/5/6/7/8): ")
    part = input("Part(1/2/3, practice时填0): ")
    return [subj_id, name, gender, age, run, part]

#### define subject info:
SUBJ_INFO = get_subj_info()
RUN = int(SUBJ_INFO[4])
PART = int(SUBJ_INFO[5])
SUBJ_NUM  = int(SUBJ_INFO[0])

#create data files:创建文件夹
def init_data_file(SUBJ_INFO):
    """ define a function that initializes the data file and get sub_info"""
    if not os.path.exists("WatchVideo_csv_data"): os.mkdir("WatchVideo_csv_data")
    file_name = "WatchVideo_csv_data/" + SUBJ_INFO[0] + "_" + SUBJ_INFO[1] + "_" + SUBJ_INFO[4] + "_" + SUBJ_INFO[5] + ".csv"
    Data_file = open(file_name, "a")
    header = ["subj_id", "name", "gender", "age", "run", "part", "session", "trial_num","video_type", "video_number", "Condition", "detection","trigger_number","Detection_Resp","if_pause","pause_time","trial_start_time"]
    Data_file.write(",".join(header) + "\n")
    Data_file.close()

#### initialize the data files.
init_data_file(SUBJ_INFO)

####视角转换
view_distance = 60#cm
scn_width_cm = 54.0 #cm
scn_size = (1920,1080)

#屏幕对应视角
#scn_width_deg = (scn_width_cm/view_distance)*(180/pi)   # method1
scn_width_deg = 2 * atan(scn_width_cm/(2*view_distance))*(180/pi)  # method2

#一度视角对应多少像素
deg2pix = int(scn_size[0]/scn_width_deg)
print(scn_width_deg,deg2pix)

####some constants: 定义几个常量
fix_loc = (0,0)
background_color = [0,0,0] # gray

# crate all video path
video_stim_path_exp1 = {f"Type_{i+1}": [f"Videos/Exp1/type{i+1}/video_{j+1}.mp4" for j in range(56)] for i in range(16)}
video_stim_path_exp2_cond1 = {f"Type_{i+1}": [f"Videos/Exp2/Cond1/type{i+1}/video_{j+1}.mp4" for j in range(4)] for i in range(16)}
video_stim_path_exp2_cond2 = {f"Type_{i+1}": [f"Videos/Exp2/Cond2/type{i+1}/video_{j+1}.mp4" for j in range(4)] for i in range(16)}
video_stim_path_exp2_cond3 = {f"Type_{i+1}": [f"Videos/Exp2/Cond3/type{i+1}/video_{j+1}.mp4" for j in range(4)] for i in range(16)}

def build_detection_labels(trial_num, detection_ratio, allow_detection=True):
    if not allow_detection:
        return ['nonDetect'] * trial_num

    detection_num = int(trial_num * detection_ratio)
    detect1_num = detection_num // 2
    detect2_num = detection_num - detect1_num
    labels = ['Detect1'] * detect1_num + ['Detect2'] * detect2_num + ['nonDetect'] * (trial_num - detection_num)
    random.shuffle(labels)
    return labels

def attach_detection_labels(session_pairs, detection_ratio, allow_detection=True):
    labels = build_detection_labels(len(session_pairs), detection_ratio, allow_detection=allow_detection)
    return [[[*(trial_path[0]), label], trial_path[1]] for trial_path, label in zip(session_pairs, labels)]

def build_exp1_sessions(video_path_dict, num_sessions, detection_ratio):
    sessions = [[] for _ in range(num_sessions)]
    videos_per_session = 7
    repeats_per_video = 3

    for cat, video_paths in video_path_dict.items():
        video_numbers = list(range(1, len(video_paths) + 1))
        random.shuffle(video_numbers)

        for session_idx in range(num_sessions):
            start = session_idx * videos_per_session
            end = start + videos_per_session
            chosen_videos = video_numbers[start:end]

            for video_num in chosen_videos:
                video_path = video_paths[video_num - 1]
                for _ in range(repeats_per_video):
                    sessions[session_idx].append([[cat, video_num, 'exp1'], video_path])

    return [attach_detection_labels(session_pairs, detection_ratio) for session_pairs in sessions]


def build_exp2_condition_sessions(video_path_dict, condition_name, num_sessions, repeats_per_session, detection_ratio, allow_detection=True):
    sessions = []

    for _ in range(num_sessions):
        session_pairs = []
        for cat, video_paths in video_path_dict.items():
            for video_num, video_path in enumerate(video_paths, start=1):
                for _ in range(repeats_per_session):
                    session_pairs.append([[cat, video_num, condition_name], video_path])

        sessions.append(attach_detection_labels(session_pairs, detection_ratio, allow_detection=allow_detection))

    return sessions

## create and save the path_list
list_file = "WatchVideo_csv_data/" + SUBJ_INFO[0] + "_" + SUBJ_INFO[1]  + "_Shuffled_List"  + ".json"

if not os.path.exists(list_file):

    detection_ratio = 0.05
    num_mixed_session = 8
    exp2_repeats_per_session = 5   # 40 repeats / 8 sessions

    exp1_sessions = build_exp1_sessions(video_stim_path_exp1, num_mixed_session, detection_ratio)

    exp2_cond1_sessions = build_exp2_condition_sessions(
        video_stim_path_exp2_cond1, 'exp2cond1', num_mixed_session, exp2_repeats_per_session, detection_ratio
    )
    exp2_cond2_sessions = build_exp2_condition_sessions(
        video_stim_path_exp2_cond2, 'exp2cond2', num_mixed_session, exp2_repeats_per_session, detection_ratio
    )
    exp2_cond3_sessions = build_exp2_condition_sessions(
        video_stim_path_exp2_cond3, 'exp2cond3', num_mixed_session, exp2_repeats_per_session, detection_ratio, allow_detection=False
    )

    Mixed_Sessions = []
    for session_idx in range(num_mixed_session):
        session_pairs = (
            exp1_sessions[session_idx]
            + exp2_cond1_sessions[session_idx]
            + exp2_cond2_sessions[session_idx]
            + exp2_cond3_sessions[session_idx]
        )
        random.shuffle(session_pairs)

        Mixed_Sessions.append({
            "trials": [tp[0] for tp in session_pairs],
            "paths": [tp[1] for tp in session_pairs],
        })

    with open(list_file, 'w', encoding='utf-8') as f:
        json.dump({"Mixed_Sessions": Mixed_Sessions}, f, ensure_ascii=False, indent=4)


elif os.path.exists(list_file):   # load mixed sessions list

    with open(list_file, 'r', encoding='utf-8') as f:
        Mixed_Sessions = json.load(f)["Mixed_Sessions"]


#### Initialize PsychoPy Window
my_monitor = monitors.Monitor('DELL SE2723DS', width=scn_width_cm, distance=view_distance)
my_monitor.save()
win = visual.Window(size=scn_size, fullscr=False, color=background_color, monitor=my_monitor, units='pix')  # full screen
win.mouseVisible = False

#### define some instructions #####################################################################################################################################################################
def wait4key(KEYS_ALLOWED):
    event.waitKeys(keyList=[KEYS_ALLOWED])

def show_text(msg, loc):
    message = visual.TextStim(win, text=msg, pos=loc, height=0.65*deg2pix,color='black',bold=True)
    message.draw()
    win.flip()

def draw_fixation():
    #fixation = visual.Circle(win, radius=deg2pix/8, fillColor='white', lineColor='white',pos=fix_loc)
    fixation1 = visual.Line(win, start=[-0.26*deg2pix,0], end=[0.26*deg2pix,0], lineWidth=0.1*deg2pix, lineColor='white',pos=fix_loc)
    fixation2 = visual.Line(win, start=[0,-0.26*deg2pix], end=[0,0.26*deg2pix], lineWidth=0.1*deg2pix, lineColor='white', pos=fix_loc)
    fixation1.draw()
    fixation2.draw()

def draw_target():
    #target = visual.Circle(win, radius=deg2pix/8, fillColor='red', lineColor='red', pos=fix_loc)
    target1 = visual.Line(win, start=[-0.26*deg2pix,0], end=[0.26*deg2pix,0], lineWidth=0.1*deg2pix, lineColor='red',pos=fix_loc)
    target2 = visual.Line(win, start=[0,-0.26*deg2pix], end=[0,0.26*deg2pix], lineWidth=0.1*deg2pix, lineColor='red', pos=fix_loc)
    target1.draw()
    target2.draw()


def find_trigger_number(trial):
    type_num = int(trial[0][5:])   # "Type_1" -> 1

    if trial[3] == "nonDetect":
        trigger_num = type_num
    else:
        trigger_num = type_num + 100

    return trigger_num


def play_movie_without_response(movie,send_trigger_num):

    movie.seek(0)
    event.clearEvents()  # 等待被试反应的期间确保之前所有的event都被清空,以防之前的按键等影响当前事件
    trigger_sent = False
    pause = False
    pause_time = None
    timer = core.Clock()

    # display movie
    while True:
        current_time = timer.getTime()
        movie.draw()
        win.flip()
        if not trigger_sent:
            send_triggers(send_trigger_num)
            #print(send_trigger_num)
            trigger_sent = True

        keys = event.getKeys()
        if 'escape' in keys:
            core.quit()

        if 'space' in keys:
            send_triggers(66)
            pause_time = time.time()
            pause = True

        if current_time > movie.duration:
            movie.stop()
            #send_triggers(65) #movie end
            break
    return [pause,pause_time]

def input_movie_content(detection_type):
    if detection_type == "Detect1":
        instruction = visual.TextStim(win, text="刚才视频里发生的动作是什么?",pos=(0, int(0.5 * scn_size[1] * 0.5)), height=int(0.6 * deg2pix), color="white")
        input_box = visual.TextBox2(win, text="", font='Microsoft YaHei', pos=(0, 0), letterHeight=int(0.5 * deg2pix), size=(int(0.8 * scn_size[0]), int(0.2 * scn_size[1])),borderWidth=2, color='white', borderColor='gray', fillColor=background_color,editable=True)
    elif detection_type == "Detect2":
        instruction = visual.TextStim(win, text="刚才视频里的主体是什么?", pos=(0, int(0.5 * scn_size[1] * 0.5)), height=int(0.6 * deg2pix), color="white")
        input_box = visual.TextBox2(win, text="", font='Microsoft YaHei', pos=(0, 0), letterHeight=int(0.5 * deg2pix), size=(int(0.8 * scn_size[0]), int(0.2 * scn_size[1])),borderWidth=2, color='white', borderColor='gray', fillColor=background_color,editable=True)

    event.clearEvents()
    while True:
        instruction.draw()
        input_box.draw()
        win.flip()

        keys = event.getKeys()
        if 'return' in keys or 'enter' in keys:
            # 提交输入
            final_text = input_box.text.strip() or "Missing Answer"
            break

    return final_text

def load_all_videos(movie_paths):
    # preload all the movies  # movie_paths: path list of all the movies
    movie_list = []
    video_count = len(movie_paths)
    print(f"加载视频 ({video_count}个)")

    for path in movie_paths:

        movie = MovieStim(win, filename=path, size=8.4*deg2pix, loop=False) #修改成统一尺寸8.4°
        movie_list.append(movie)

    print(f"加载完成")
    return movie_list


def run_block(subj_info,session,Run_LIST,movie_path_list,trial_offset=0):

    count = 0

    # preload the movie
    all_movies = load_all_videos(movie_path_list)

    show_text("视频加载完成，按空格开始实验", (fix_loc[0] - 0.5 * deg2pix * 2, fix_loc[1]))
    wait4key('space')

    # present the target
    for trial in Run_LIST:
        trial_start_time = time.time()
        trigger_number = find_trigger_number(trial)

        pause_info = play_movie_without_response(all_movies[count], send_trigger_num = trigger_number)

        # detect movie content
        Detection_Resp = None  # 不需要detection的trial默认返回none
        if trial[3] in ("Detect1", "Detect2"):
            Detection_Resp = input_movie_content(trial[3])

        ## if rest
        if pause_info[0]:
            show_text("休息一下，按空格继续", (fix_loc[0] - 0.5 * deg2pix * 3, fix_loc[1]))
            wait4key('space')

        core.wait(random.uniform(0.1, 0.2))

        trial_num = trial_offset + count + 1

        # write data to file写入数据  # 还需要补充：绝对时间，当前trial试次
        data_file = open("WatchVideo_csv_data/" + SUBJ_INFO[0] + "_" + SUBJ_INFO[1] + "_" + SUBJ_INFO[4] + "_" + SUBJ_INFO[5] + ".csv", "a",encoding="utf-8")
        trial_data = subj_info  + [session] + [trial_num] + trial + [trigger_number] + [Detection_Resp] + pause_info + [trial_start_time]
        trial_data_1 = ",".join(map(str,trial_data)) + "\n"
        data_file.write(trial_data_1)
        data_file.close()

        count = count + 1

    # release memory
    del all_movies
    gc.collect()


#### real experiment starts here#######################################################################################################################################################################

#### prepare for the task
show_text("请自由观看视频，并回答视频后的内容。自行按空格键休息。", (fix_loc[0]-0.5*deg2pix*3,fix_loc[1]))
wait4key('space')

#### run Sessions
## Practice
if RUN == 0:  ## run = 0
    run_block(SUBJ_INFO, RUN, Mixed_Sessions[0]["trials"][:20], Mixed_Sessions[0]["paths"][:20])
    show_text("练习任务结束", (fix_loc[0] - 0.5 * deg2pix * 1, fix_loc[1]))
    wait4key('space')

## Real Experiment Start Here
else:
    Run_LIST = Mixed_Sessions[RUN - 1]["trials"]
    Movie_LIST = Mixed_Sessions[RUN - 1]["paths"]

    total_trials = len(Run_LIST)
    n_parts = 3
    part_size = total_trials // n_parts

    if PART not in [1, 2, 3]:
        raise ValueError("Formal experiment part must be 1, 2, or 3.")

    start = (PART - 1) * part_size
    end = PART * part_size if PART < n_parts else total_trials
    trial_offset = start

    run_block(
        SUBJ_INFO,
        f"{RUN}_Part{PART}",
        Run_LIST[start:end],
        Movie_LIST[start:end],
        trial_offset=trial_offset)

    show_text(f"Session {RUN} Part {PART} 结束", fix_loc)
    wait4key('space')

    show_text("辛苦啦，任务结束", (fix_loc[0] - 0.5 * deg2pix * 1, fix_loc[1]))
    wait4key('space')


# exit
core.quit()
sys.exit()
