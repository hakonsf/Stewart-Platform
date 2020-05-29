from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import mainwindow
import calcKinematicsV2 as ck

import time


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        print("Thread started")
        self.fn(*self.args, **self.kwargs)
        print("Thread stopped")


class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.threadpool = QThreadPool()
        self.setupUi(self)
        self.var_prog = 0
        self.is_running = False
        self.stop = False
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    # gui slider value read and update
    def heave_changed(self):
        heave_value_string = str(self.slider_heave.value())
        self.label_heave_value.setText(heave_value_string)
        self.var_prog = 1
        self.textBrowser_progselected.setText("Custom Wave")

    def surge_changed(self):
        surge_value_string = str(self.slider_surge.value())
        self.label_surge_value.setText(surge_value_string)
        self.var_prog = 1
        self.textBrowser_progselected.setText("Custom Wave")

    def sway_changed(self):
        sway_value_string = str(self.slider_sway.value())
        self.label_sway_value.setText(sway_value_string)
        self.var_prog = 1
        self.textBrowser_progselected.setText("Custom Wave")

    def roll_changed(self):
        roll_value_string = str(self.slider_roll.value())
        self.label_roll_value.setText(roll_value_string)
        self.var_prog = 1
        self.textBrowser_progselected.setText("Custom Wave")

    def pitch_changed(self):
        pitch_value_string = str(self.slider_pitch.value())
        self.label_pitch_value.setText(pitch_value_string)
        self.var_prog = 1
        self.textBrowser_progselected.setText("Custom Wave")

    def yaw_changed(self):
        yaw_value_string = str(self.slider_yaw.value())
        self.label_yaw_value.setText(yaw_value_string)
        self.var_prog = 1
        self.textBrowser_progselected.setText("Custom Wave")

    def transfreq_changed(self):
        transfreq_value_string = str(self.slider_transfreq.value())
        self.label_transfreq_value.setText(transfreq_value_string)
        self.var_prog = 1
        self.textBrowser_progselected.setText("Custom Wave")

    def rotfreq_changed(self):
        rotfreq_value_string = str(self.slider_rotfreq.value())
        self.label_rotfreq_value.setText(rotfreq_value_string)
        self.var_prog = 1
        self.textBrowser_progselected.setText("Custom Wave")

    # start or stop selected program

    def startbutton_advanced_clicked(self):
        self.var_prog = 1
        self.run_worker()

    def stopbutton_advanced_clicked(self):
        if self.var_prog == 1:
            self.stop = True
            self.run_worker()

    def startbutton_easy_clicked(self):
        self.run_worker()

    def stopbutton_easy_clicked(self):
        if self.var_prog == 1:
            self.stop = True
            self.run_worker()

    # predefined programs
    def program1(self):
        print("=================Program 1 loaded=================")
        self.var_prog = 1

        self.slider_surge.setValue(0)
        self.slider_sway.setValue(0)
        self.slider_heave.setValue(0)
        self.slider_roll.setValue(8)
        self.slider_pitch.setValue(8)
        self.slider_yaw.setValue(0)
        self.slider_rotfreq.setValue(1)
        self.slider_transfreq.setValue(1)
        self.textBrowser_progselected.setText("Wave 1")

    def program2(self):
        print("=================Program 2 loaded=================")
        self.var_prog = 1

        self.slider_surge.setValue(5)
        self.slider_sway.setValue(5)
        self.slider_heave.setValue(5)
        self.slider_roll.setValue(4)
        self.slider_pitch.setValue(4)
        self.slider_yaw.setValue(4)
        self.slider_rotfreq.setValue(1)
        self.slider_transfreq.setValue(2)
        self.textBrowser_progselected.setText("Wave 2")

    def program3(self):
        self.textBrowser_progselected.setText("Fixed Path")
        print("=================Program 3 loaded=================")
        self.var_prog = 2

    def program4(self):
        self.textBrowser_progselected.setText("Reset")
        print("=================Reset program loaded=================")
        self.var_prog = 3

    def execute(self):
        if self.var_prog == 1:
            ck.forceReset()
            ck.waitForStart()
            data = ck.oscillator(self.slider_transfreq.value(), self.slider_rotfreq.value(),
                                 self.slider_surge.value(), self.slider_sway.value(),
                                 self.slider_heave.value(), self.slider_roll.value(),
                                 self.slider_pitch.value(), self.slider_yaw.value())
            time_0 = time.time()
            for count in range(0, ck.no_sample):
                if self.is_running:
                    output = ck.calc_kinematics(data[0][count], data[1][count],
                                                data[2][count], data[3][count],
                                                data[4][count], data[5][count])
                    while time.time() < time_0 + ck.sample_rate * count:  # sending delay
                        pass
                    for i in range(0, 6):
                        send = str('<') + str(output[i]) + str('>')
                        ck.sendToArduino(send)
                else:
                    return
        elif self.var_prog == 2:
            ck.forceReset()
            ck.waitForStart()
            time.sleep(1)
            if self.is_running:
                output = ck.calc_kinematics(0, 0, 90, 0, 0, 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
                time.sleep(2)
                output = ck.calc_kinematics(0, 0, 10, 0, 0, 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)

                time.sleep(1)
                output = ck.calc_kinematics(0, 0, 42, 0, 0, 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
                time.sleep(1)
                output = ck.calc_kinematics(30, 0, 42, 0, 0, 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
                time.sleep(1)
                output = ck.calc_kinematics(-30, 0, 42, 0, 0, 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)

                time.sleep(1)
                output = ck.calc_kinematics(0, 0, 42, 0, 0, 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
                time.sleep(1)
                output = ck.calc_kinematics(0, 30, 42, 0, 0, 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
                time.sleep(1)
                output = ck.calc_kinematics(0, -30, 42, 0, 0, 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
                time.sleep(1)

                output = ck.calc_kinematics(0, 0, 42, 0, 0, 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
                time.sleep(1)
                output = ck.calc_kinematics(0, 0, 42, 8 * (3.1415 / 180), 0, 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
                time.sleep(1)
                output = ck.calc_kinematics(0, 0, 42, -8 * (3.1415 / 180), 0, 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
                time.sleep(1)

                output = ck.calc_kinematics(0, 0, 42, 0, 0, 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
                time.sleep(1)
                output = ck.calc_kinematics(0, 0, 42, 0, 8 * (3.1415 / 180), 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
                time.sleep(1)
                output = ck.calc_kinematics(0, 0, 42, 0, -8 * (3.1415 / 180), 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
                time.sleep(1)

                output = ck.calc_kinematics(0, 0, 42, 0, 0, 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
                time.sleep(1)
                output = ck.calc_kinematics(0, 0, 42, 0, 0, 8 * (3.1415 / 180))
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
                time.sleep(1)
                output = ck.calc_kinematics(0, 0, 42, 0, 0, -8 * (3.1415 / 180))
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
                time.sleep(1)

                output = ck.calc_kinematics(0, 0, 42, 0, 0, 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
                time.sleep(1)
            else:
                return
        elif self.var_prog == 3:
            ck.forceReset()
            ck.waitForStart()
            time.sleep(1)
            if self.is_running:
                output = ck.calc_kinematics(0, 0, 1, 0, 0, 0)
                for i in range(0, 6):
                    send = str('<') + str(output[i]) + str('>')
                    ck.sendToArduino(send)
        else:
            pass
        self.is_running = False

    def run_worker(self):
        # Pass the function to execute
        worker = Worker(self.execute)  # Any other args, kwargs are passed to the run function
        if not self.is_running:
            # Execute
            self.is_running = True
            self.threadpool.start(worker)
        elif self.stop:
            self.is_running = False
            self.threadpool.clear()
            self.stop = False


def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()


if __name__ == '__main__':
    ck.waitForArduino()
    main()
