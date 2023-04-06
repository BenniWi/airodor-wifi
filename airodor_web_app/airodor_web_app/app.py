import ipaddress
import threading
import time
from datetime import datetime, timedelta
from queue import Queue

import pytz
from airodor_wifi_api import airodor
from flask import Flask, redirect, render_template, request, url_for

default_IP = ipaddress.ip_address("192.168.2.122")
current_ip = default_IP
lock_timer_dict = threading.Lock()
timer_dict = {"A": airodor.VentilationTimerList(), "B": airodor.VentilationTimerList()}
timezone = pytz.timezone('Europe/Berlin')

lock_message_queue = threading.Lock()
return_message_queue = Queue(maxsize=10)

do_real_communication = True

app = Flask(__name__)

backend_running = False


def backend_thread():
    while 1:
        # print(datetime.now().time())
        check_and_update_timers()
        time.sleep(10)


def add_message_to_queue(message: str):
    global return_message_queue
    with lock_message_queue:
        if return_message_queue.full():
            return_message_queue.get()
        return_message_queue.put(message)


def message_queue_to_string() -> str:
    global return_message_queue
    with lock_message_queue:
        return str("\n".join(return_message_queue.queue))


def check_and_update_timers():
    with lock_timer_dict:
        global timer_dict
        is_ok = False
        now = datetime.now(timezone)
        for td in timer_dict:
            for timer in timer_dict[td].timer_list[:]:  # loop over a copy but ...
                if timer.execution_time < now:
                    if do_real_communication:
                        is_ok = airodor.set_mode(current_ip, timer.group, timer.mode)
                    else:
                        is_ok = True
                    # remove the timer from the list
                    if is_ok:
                        print("removing timer {}".format(timer))
                        timer_dict[td].timer_list.remove(timer)  # ... remove from the original
                        add_message_to_queue(
                            "success for timer with group {} and mode {}".format(timer.group, timer.mode)
                        )
                    else:
                        add_message_to_queue("Error processing queue")


@app.route('/')
def index():
    global backend_running
    if not backend_running:
        threading.Thread(target=backend_thread).start()
        backend_running = True
    now = datetime.now(timezone)
    if do_real_communication:
        vent_mode_A = airodor.get_mode(current_ip, group=airodor.VentilationGroup.A)
        if vent_mode_A:
            add_message_to_queue("Success reading status for group A")
        else:
            add_message_to_queue("Error reading status for group A")
        vent_mode_B = airodor.get_mode(current_ip, group=airodor.VentilationGroup.B)
        if vent_mode_B:
            add_message_to_queue("Success reading status for group B")
        else:
            add_message_to_queue("Error reading status for group B")
    else:
        vent_mode_A = airodor.VentilationMode.ALTERNATING_MAX
        add_message_to_queue("Success reading status for group A")
        vent_mode_B = airodor.VentilationMode.INSIDE_MED
        add_message_to_queue("Success reading status for group B")
    return render_template(
        'index.html',
        ip_address=current_ip,
        ventilation_modes=airodor.VentilationMode,
        status_string_group_A=vent_mode_A.name,
        status_time_group_A=now.strftime("%X"),
        status_string_group_B=vent_mode_B.name,
        status_time_group_B=now.strftime("%X"),
        timer_list_A=timer_dict["A"].create_string_list(),
        timer_list_B=timer_dict["B"].create_string_list(),
        comm_log=message_queue_to_string(),
    )


@app.route('/updateIP/', methods=['POST'])
def updateIP():
    if request.method == "POST":
        try:
            new_ip = ipaddress.ip_address(request.form.get('ip_address'))
            global current_ip
            current_ip = new_ip
        except ValueError:
            print("Got invalid ipaddress: {}".format(request.form.get('ip_address')))
    return redirect(url_for("index"))


@app.route('/add_timer/', methods=['POST'])
def add_timer():
    print('new timer')
    if request.method == "POST":
        deltatime = int(request.form.get('timerValue'))
        mode = int(request.form.get('mode_select'))
        group = request.form.get('group_select')
        print("timer:group {}, mode {}, value {}".format(group, mode, deltatime))
        if mode >= 0:
            mode = airodor.VentilationMode(mode)
            if group == "both":
                group = [airodor.VentilationGroup("A"), airodor.VentilationGroup("B")]
            else:
                group = [airodor.VentilationGroup(group)]

            for g in group:
                global timer_dict
                timer_dict[g.name].add_list_item(datetime.now(timezone) + timedelta(minutes=deltatime), g, mode)

    print(timer_dict["A"].create_string_list())
    print(timer_dict["B"].create_string_list())
    check_and_update_timers()
    return redirect(url_for("index"))


@app.route('/remove_timer/', methods=['POST'])
def remove_timer():
    print('remove timer')
    if request.method == "POST":
        remove_from = dict()
        remove_from["A"] = request.form.getlist('timer_list_A')
        remove_from["B"] = request.form.getlist('timer_list_B')

        global timer_dict
        for remove_list_key in remove_from:
            for remove_index in remove_from[remove_list_key]:
                del timer_dict[remove_list_key].timer_list[int(remove_index)]

    return redirect(url_for("index"))


def main():
    app.run(debug=True, host="0.0.0.0")


if __name__ == '__main__':
    main()
