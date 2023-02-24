from flask import Flask, render_template, url_for, redirect, request
from airodor_wifi_api import airodor
import ipaddress
from datetime import datetime, timedelta
import pytz

default_IP = ipaddress.ip_address("192.168.2.122")
current_ip = default_IP
timer_dict = {"A": airodor.VentilationTimerList(), "B": airodor.VentilationTimerList()}

app = Flask(__name__)


@app.route('/')
def index():
    now = datetime.now(pytz.timezone('Europe/Berlin'))
    #vent_mode_A = airodor.get_mode(current_ip,
    #                               group=airodor.VentilationGroup.A)
    #vent_mode_B = airodor.get_mode(current_ip,
    #                               group=airodor.VentilationGroup.B)
    vent_mode_A = airodor.VentilationMode.ALTERNATING_MAX
    vent_mode_B = airodor.VentilationMode.INSIDE_MED
    return render_template('index.html',
                           ip_address=current_ip,
                           ventilation_modes=airodor.VentilationMode,
                           status_string_group_A=vent_mode_A.name,
                           status_time_group_A=now.strftime("%X"),
                           status_string_group_B=vent_mode_B.name,
                           status_time_group_B=now.strftime("%X"),
                           timer_list_A=timer_dict["A"].create_string_list(),
                           timer_list_B=timer_dict["B"].create_string_list())


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
                timer_dict[g.name].add_list_item(datetime.now(pytz.timezone('Europe/Berlin'))
                                                 + timedelta(minutes=deltatime), g, mode)

    print(timer_dict["A"].create_string_list())
    print(timer_dict["B"].create_string_list())
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


if __name__ == '__main__':
    app.run(debug=True)
