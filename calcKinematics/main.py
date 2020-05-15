from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import mainwindow
import calcKinematicsV2 as ck
import time


class MyWindow(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        self.thread = QtCore.QThread()
        self.worker = None
        self.var_program = 0

    def start_worker(self):
        self.thread.quit()
        self.thread.start()
        if self.var_program == 0:

            self.worker = Worker(self.slider_transfreq.value(), self.slider_rotfreq.value(),
                                 self.slider_surge.value(), self.slider_sway.value(),
                                 self.slider_heave.value(), self.slider_roll.value(),
                                 self.slider_pitch.value(), self.slider_yaw.value())
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.runVar)
        elif self.var_program == 1:
            pass
        elif self.var_program == 2:
            self.worker = Worker()
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.runFixed)
        elif self.var_program == 3:
            self.worker = Worker()
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.runHome)
        else:
            pass

    def stop_thread(self):
        self.worker.stop()  # stop all long loops
        self.thread.quit()

    # gui slider value read and update
    def heave_changed(self):
        heave_value_string = str(self.slider_heave.value())
        self.label_heave_value.setText(heave_value_string)

    def surge_changed(self):
        surge_value_string = str(self.slider_surge.value())
        self.label_surge_value.setText(surge_value_string)

    def sway_changed(self):
        sway_value_string = str(self.slider_sway.value())
        self.label_sway_value.setText(sway_value_string)

    def roll_changed(self):
        roll_value_string = str(self.slider_roll.value())
        self.label_roll_value.setText(roll_value_string)

    def pitch_changed(self):
        pitch_value_string = str(self.slider_pitch.value())
        self.label_pitch_value.setText(pitch_value_string)

    def yaw_changed(self):
        yaw_value_string = str(self.slider_yaw.value())
        self.label_yaw_value.setText(yaw_value_string)

    def transfreq_changed(self):
        transfreq_value_string = str(self.slider_transfreq.value())
        self.label_transfreq_value.setText(transfreq_value_string)

    def rotfreq_changed(self):
        rotfreq_value_string = str(self.slider_rotfreq.value())
        self.label_rotfreq_value.setText(rotfreq_value_string)

    # start or stop selected program

    def startbutton_advanced_clicked(self):
        print("startbuttonAdvanced is clicked")
        self.var_program = 0
        self.start_worker()

    def stopbutton_advanced_clicked(self):
        print("stopbuttonAdvanced is clicked")
        self.stop_thread()

    def startbutton_easy_clicked(self):
        print("startbuttonEasy is clicked")
        self.start_worker()

    def stopbutton_easy_clicked(self):
        print("stopbuttonEasy is clicked")
        self.stop_thread()

    # predefined programs

    def program1(self):
        self.textBrowser_progselected.setText("Custom wave")
        print("=================Program 1 loaded=================")
        self.var_program = 0

        self.slider_surge.setValue(0)
        self.slider_sway.setValue(0)
        self.slider_heave.setValue(10)
        self.slider_roll.setValue(0)
        self.slider_pitch.setValue(0)
        self.slider_yaw.setValue(0)
        self.slider_rotfreq.setValue(1)
        self.slider_transfreq.setValue(6)

    def program2(self):
        self.textBrowser_progselected.setText("Program 2")
        print("=================Program 2 loaded=================")
        self.var_program = 0

        self.slider_surge.setValue(0)
        self.slider_sway.setValue(0)
        self.slider_heave.setValue(10)
        self.slider_roll.setValue(0)
        self.slider_pitch.setValue(0)
        self.slider_yaw.setValue(0)
        self.slider_rotfreq.setValue(1)
        self.slider_transfreq.setValue(6)

    def program3(self):
        self.textBrowser_progselected.setText("Program 3")
        print("=================Program 3 loaded=================")
        self.var_program = 2

    def program4(self):
        self.textBrowser_progselected.setText("Reset")
        print("=================Reset program loaded=================")
        self.var_program = 3


class Worker(QtCore.QObject):
    def __init__(self, *args):
        super(Worker, self).__init__()

        self.args = args
        self.isRunning = True

    def runVar(self):
        print('Input arguments', *self.args)
        print('=================Worker.runVar()=================')
        ck.forceReset()
        ck.waitForStart()
        data = ck.oscillator(*self.args)
        time_0 = time.time()
        for count in range(0, ck.no_sample):
            if self.isRunning:
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
        print(time.time() - time_0)
        print('=================Thread done=================')

    def runReset(self):
        ck.forceReset()
        ck.waitForStart()
        print('=================Thread done=================')

    def runFixed(self):
        ck.forceReset()
        ck.waitForStart()
        output = ck.calc_kinematics(0, 0, 90, 0, 0, 0)
        for i in range(0, 6):
            send = str('<') + str(output[i]) + str('>')
            ck.sendToArduino(send)
        time.sleep(1)
        print('======================================')
        output = ck.calc_kinematics(0, 0, 10, 0, 0, 0)
        for i in range(0, 6):
            send = str('<') + str(output[i]) + str('>')
            ck.sendToArduino(send)
        time.sleep(1.5)
        print('======================================')
        output = ck.calc_kinematics(0, 0, 42, 0, 0, 0)
        for i in range(0, 6):
            send = str('<') + str(output[i]) + str('>')
            ck.sendToArduino(send)
        time.sleep(1)
        print('======================================')
        output = ck.calc_kinematics(30, 0, 42, 0, 0, 0)
        for i in range(0, 6):
            send = str('<') + str(output[i]) + str('>')
            ck.sendToArduino(send)
        time.sleep(1)
        print('======================================')
        output = ck.calc_kinematics(-30, 0, 42, 0, 0, 0)
        for i in range(0, 6):
            send = str('<') + str(output[i]) + str('>')
            ck.sendToArduino(send)
        time.sleep(1)
        print('======================================')
        output = ck.calc_kinematics(0, 0, 42, 0, 0, 0)
        for i in range(0, 6):
            send = str('<') + str(output[i]) + str('>')
            ck.sendToArduino(send)
        time.sleep(1)
        print('======================================')
        output = ck.calc_kinematics(0, 0, 42, 8 * (3.1415 / 180), 0, 0)
        for i in range(0, 6):
            send = str('<') + str(output[i]) + str('>')
            ck.sendToArduino(send)
        time.sleep(1)
        print('======================================')
        output = ck.calc_kinematics(0, 0, 42, -8 * (3.1415 / 180), 0, 0)
        for i in range(0, 6):
            send = str('<') + str(output[i]) + str('>')
            ck.sendToArduino(send)
        time.sleep(1)
        print('======================================')
        output = ck.calc_kinematics(0, 0, 42, 0, 0, 0)
        for i in range(0, 6):
            send = str('<') + str(output[i]) + str('>')
            ck.sendToArduino(send)
        time.sleep(1)
        print('=================Thread done=================')

    def runHome(self):
        ck.forceReset()
        ck.waitForStart()
        time.sleep(2)
        output = ck.calc_kinematics(0, 0, 45, 0, 0, 0)
        for i in range(0, 6):
            send = str('<') + str(output[i]) + str('>')
            ck.sendToArduino(send)
        time.sleep(2)
        output = ck.calc_kinematics(0, 0, 45, 0, 0, 0)
        for i in range(0, 6):
            send = str('<') + str(output[i]) + str('>')
            ck.sendToArduino(send)
        time.sleep(1)
        output = ck.calc_kinematics(0, 0, 0, 0, 0, 0)
        for i in range(0, 6):
            send = str('<') + str(output[i]) + str('>')
            ck.sendToArduino(send)
        time.sleep(2)
        print('=================Thread done=================')

    def stop(self):
        self.isRunning = False
        print('=================Worker.Stop()=================')


def main():
    app = QApplication(sys.argv)
    form = MyWindow()
    form.show()
    app.exec_()


if __name__ == '__main__':
    ck.waitForArduino()
    main()
