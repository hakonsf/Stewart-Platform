import numpy as np
from math import pi
import serial
import time

# defining serial variables


ser = serial.Serial(
    'COM7',  # COM7 = windows usb port
    baudrate=57600
)
startMarker = 60
endMarker = 62

start = 0

t_max = 20  # total cycle time (s)
sample_rate = 0.0625  # 16 points per period
no_sample = int(t_max / sample_rate)
running = 0


def oscillator(trans_adj, rot_adj, surge_a_adj, sway_a_adj,
               heave_a_adj, roll_a_adj, pitch_a_adj, yaw_a_adj):
    trans_freq = (1 / 20) * trans_adj  # translation signal frequency
    rot_freq = (6 / 10) * rot_adj  # rotation signal frequency

    # surge (x) values
    surge_A = 40 * 0.1 * surge_a_adj
    surge_bias = 0
    surge_offset = 0

    # sway (y) values
    sway_A = 40 * 0.1 * sway_a_adj
    sway_bias = 0
    sway_offset = -pi / 2

    # heave (z) values
    heave_A = 40 * 0.1 * heave_a_adj
    heave_bias = 48
    heave_offset = 0

    # roll (alpha) values
    roll_A = 20 * 0.1 * roll_a_adj
    roll_bias = 0
    roll_offset = 0

    # pitch (beta) values
    pitch_A = 20 * 0.1 * pitch_a_adj
    pitch_bias = 0
    pitch_offset = -pi / 2

    # yaw (gamma) values
    yaw_A = 20 * 0.1 * yaw_a_adj
    yaw_bias = 0
    yaw_offset = 0

    # defining x positions based on sample rate and runtime
    trans_x = np.arange(0, t_max, sample_rate)  # calculating translation points
    rot_x = np.arange(0, t_max, sample_rate)  # calculating rotation points

    # y position generation
    # translation
    surge_y = surge_A * np.sin(2 * pi * trans_x * trans_freq + surge_offset) + surge_bias
    sway_y = sway_A * np.sin(2 * pi * trans_x * trans_freq + sway_offset) + sway_bias
    heave_y = heave_A * np.sin(2 * pi * trans_x * trans_freq + heave_offset) + heave_bias

    # rotation
    roll_y = roll_A * (pi / 180) * np.sin(2 * pi * rot_x * rot_freq + roll_offset) + roll_bias
    pitch_y = pitch_A * (pi / 180) * np.sin(2 * pi * rot_x * rot_freq + pitch_offset) + pitch_bias
    yaw_y = yaw_A * (pi / 180) * np.sin(2 * pi * rot_x * rot_freq + yaw_offset) + yaw_bias
    return surge_y, sway_y, heave_y, roll_y, pitch_y, yaw_y


def calc_kinematics(x_in, y_in, z_in, alpha_in, beta_in, gamma_in):
    # defining input variables
    alpha = alpha_in
    beta = beta_in
    gamma = gamma_in

    x = x_in
    y = y_in
    z = 190 + z_in

    # calculating sin and cos values for matrices
    a_sin = np.sin(alpha)
    a_cos = np.cos(alpha)

    b_sin = np.sin(beta)
    b_cos = np.cos(beta)

    g_sin = np.sin(gamma)
    g_cos = np.cos(gamma)

    # defining rotation matrices
    r_a = np.array([
        [1., 0., 0.],
        [0., a_cos, -a_sin],
        [0., a_sin, a_cos]
    ])

    r_b = np.array([
        [b_cos, 0., b_sin],
        [0., 1., 0.],
        [-b_sin, 0., b_cos]
    ])

    r_g = np.array([
        [g_cos, -g_sin, 0.],
        [g_sin, g_cos, 0.],
        [0., 0., 1.]
    ])

    # defining total rotation matrix
    r = r_g @ r_b @ r_a

    # defining position vector
    p = np.array([
        [x],
        [y],
        [z]
    ])

    # defining base plate position vectors
    a1 = np.array([
        [-142.28], [-47.5], [0.]
    ])

    a2 = np.array([
        [-112.28], [-99.47], [0.]
    ])

    a3 = np.array([
        [112.28], [-99.47], [0.]
    ])

    a4 = np.array([
        [142.28], [-47.5], [0.]
    ])

    a5 = np.array([
        [30.], [146.97], [0.]
    ])

    a6 = np.array([
        [-30.], [146.97], [0.]
    ])

    # defining tool plate position vectors
    b1 = np.array([
        [-97.61], [21.72], [0.]
    ])

    b2 = np.array([
        [-30.], [-95.39], [0.]
    ])

    b3 = np.array([
        [30.], [-95.39], [0.]
    ])

    b4 = np.array([
        [97.61], [21.72], [0.]
    ])

    b5 = np.array([
        [67.61], [73.68], [0.]
    ])

    b6 = np.array([
        [-67.61], [73.68], [0.]
    ])

    # calculating leg vectors
    s1 = p + (r @ b1) - a1
    s2 = p + (r @ b2) - a2
    s3 = p + (r @ b3) - a3
    s4 = p + (r @ b4) - a4
    s5 = p + (r @ b5) - a5
    s6 = p + (r @ b6) - a6

    # calculating leg lengths
    l1 = np.sqrt(np.float_power(s1[0, 0], 2) + np.float_power(s1[1, 0], 2) + np.float_power(s1[2, 0], 2))
    l2 = np.sqrt(np.float_power(s2[0, 0], 2) + np.float_power(s2[1, 0], 2) + np.float_power(s2[2, 0], 2))
    l3 = np.sqrt(np.float_power(s3[0, 0], 2) + np.float_power(s3[1, 0], 2) + np.float_power(s3[2, 0], 2))
    l4 = np.sqrt(np.float_power(s4[0, 0], 2) + np.float_power(s4[1, 0], 2) + np.float_power(s4[2, 0], 2))
    l5 = np.sqrt(np.float_power(s5[0, 0], 2) + np.float_power(s5[1, 0], 2) + np.float_power(s5[2, 0], 2))
    l6 = np.sqrt(np.float_power(s6[0, 0], 2) + np.float_power(s6[1, 0], 2) + np.float_power(s6[2, 0], 2))

    d1 = l1 - 207
    d2 = l2 - 207
    d3 = l3 - 207
    d4 = l4 - 207
    d5 = l5 - 207
    d6 = l6 - 207

    return np.array([d1, d2, d3, d4, d5, d6])


def sendToArduino(sendStr):
    ser.write(sendStr.encode('utf-8'))
    print(sendStr)


def recvFromArduino():
    global startMarker, endMarker

    ck = ""
    x = "z"  # any value that is not an end- or startMarker
    byteCount = -1  # to allow for the fact that the last increment will be one too many

    # wait for the start character
    while ord(x) != startMarker:
        x = ser.read()

    # save data until the end marker is found
    while ord(x) != endMarker:
        if ord(x) != startMarker:
            ck = ck + x.decode("utf-8")  # change for Python3
            byteCount += 1
        x = ser.read()

    return ck


def waitForArduino():
    # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded

    global startMarker, endMarker

    msg = ""
    while msg.find("Arduino is ready") == -1:

        while ser.inWaiting() == 0:
            pass

        msg = recvFromArduino()

        print(msg)
        print()


def waitForStart():
    # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded

    global startMarker, endMarker

    startSend = ""
    while startSend != "Yes":
        startSend = "Yes"
        if startSend == "Yes":
            sendToArduino("<Start>")
            msg = ""
            while msg.find("Start") == -1:

                while ser.inWaiting() == 0:
                    pass

                msg = recvFromArduino()

                print(msg)
                print()
        else:
            pass


def forceReset():
    sendToArduino("<-1><0><0><0><0><0>")
    sendToArduino("<Reset>")
