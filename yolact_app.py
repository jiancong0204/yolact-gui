import sys
import gui
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap, QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QThread, pyqtSignal, QEventLoop, QTimer
import os
import time
import eval as eval_script
import train as train_script

class MainDialog(QDialog):

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)

        self.ui = gui.Ui_Dialog()

        self.ui.setupUi(self)
        flag = QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint
        self.setWindowFlags(flag)
        self.setWindowTitle('YOLACT - GUI')
        self.validationFile = str()
        self.validationModel = str()
        self.benchmarkModel = str()
        self.trainConfig = 'yolact_base_config'
        self.batchSize = '1'
        self.validationScoreThreshold = 0.15
        self.benchmarkNumImage = 1000
        self.ui.pushButton_evaluate.setEnabled(False)
        self.ui.pushButton_benchmark.setEnabled(False)
        self.ui.radioButton_batchEvaluation.setChecked(False)
        float_validator = QDoubleValidator(float("-inf"), float("inf"), 2, self)
        self.ui.lineEdit_scoreThreshold.setValidator(float_validator)

        int_validator = QIntValidator(1, 10000, self)
        self.ui.lineEdit_numImage.setValidator(int_validator)

        # Training
        self.t = TrainingThread()
        self.t.signalForText.connect(self.updateTextBrowser)
        self.ui.pushButton_train.clicked.connect(self.triggerTraining)
        sys.stdout = self.t
        self.ui.lineEdit_batchSize.editingFinished.connect(self.updateBatchSize)
        self.ui.lineEdit_batchSize.setValidator(int_validator)
        self.ui.lineEdit_trainConfig.editingFinished.connect(self.updateTrainConfig)

        # Benchmark
        self.b = BenchmarkThread()
        self.b.signalForText.connect(self.updateTextBrowser)
        self.ui.pushButton_benchmark.clicked.connect(self.triggerBenchmark)
        self.ui.pushButton_selectModel_2.clicked.connect(self.chooseBenchmarkModel)
        sys.stdout = self.b
        self.ui.lineEdit_numImage.editingFinished.connect(self.lineEditMoveSliderBenchmark)
        self.ui.horizontalSlider_numImage.valueChanged.connect(self.sliderEditLineEditBenchmark)

        # Evaluation
        self.e = BenchmarkThread()
        self.e.signalForText.connect(self.updateTextBrowser)
        sys.stdout = self.e
        self.ui.pushButton_selectImage.clicked.connect(self.chooseValidateFile)
        self.ui.pushButton_selectModel.clicked.connect(self.chooseTrainedModel)
        self.ui.pushButton_evaluate.clicked.connect(self.triggerEvaluation)
        self.ui.lineEdit_scoreThreshold.editingFinished.connect(self.lineEditMoveSlider)
        self.ui.horizontalSlider_scoreThreshold.valueChanged.connect(self.sliderEditLineEdit)

        # Online Test
        ## Video test
        self.d = DisplayThread()
        self.d.signalForDisplay.connect(self.displayImage)
        self.ui.pushButton_onlineTest.clicked.connect(self.triggerOnlineTest)

        # Clear
        self.ui.pushButton_reset.clicked.connect(self.clearWindow)
        self.ui.pushButton_clearTerminal.clicked.connect(self.clearTerminal)
        self.ui.pushButton_terminateThread.clicked.connect(self.terminateThread)
        self.ui.pushButton_terminateThread.setEnabled(False)

    def displayImage(self):
        curr_path = os.getcwd()
        res_path = curr_path + '/results/tmp_res.jpg'
        pixmap = QPixmap(res_path)
        self.ui.display.setPixmap(pixmap)

    def terminateThread(self):
        self.b.terminate()
        self.t.terminate()
        self.e.terminate()
        self.ui.pushButton_terminateThread.setEnabled(False)

    def updateTextBrowser(self, text):
        cursor = self.ui.textBrowser_terminal.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.ui.textBrowser_terminal.setTextCursor(cursor)
        self.ui.textBrowser_terminal.ensureCursorVisible()

    def updateBatchSize(self):
        num = self.ui.lineEdit_batchSize.text()
        num = int(num)
        self.batchSize = str(num)

    def updateTrainConfig(self):
        self.trainConfig = self.ui.lineEdit_trainConfig.text()

    def triggerTraining(self):
        # python train.py --config=yolact_base_config --batch_size=1
        config = self.trainConfig
        batch_size = self.batchSize
        args = train_script.parse_args(['--config=' + config, '--batch_size=' + batch_size])
        self.t = TrainingThread(args)
        self.ui.pushButton_terminateThread.setEnabled(True)
        self.t.start()
        loop = QEventLoop()
        QTimer.singleShot(2000, loop.quit)
        loop.exec_()

    def triggerBenchmark(self):
        # print(self.benchmarkModel)
        self.b = BenchmarkThread(self.benchmarkModel, self.benchmarkNumImage)
        self.clearWindow()
        self.ui.pushButton_terminateThread.setEnabled(True)
        self.b.start()
        loop = QEventLoop()
        QTimer.singleShot(2000, loop.quit)

    def triggerEvaluation(self):
        image = self.validationFile
        model = self.validationModel
        score_threshold = self.validationScoreThreshold


        # Setup Evaluation
        if not self.ui.radioButton_batchEvaluation.isChecked():
            eval_script.parse_args(['--trained_model=' + model, '--score_threshold=' + str(score_threshold),
                                    '--top_k=20', '--image=' + image + ':results/tmp_res.jpg'])
            eval_script.perform()
            curr_path = os.getcwd()
            res_path = curr_path + '/results/tmp_res.jpg'
            pixmap = QPixmap(res_path)
            self.ui.display.setPixmap(pixmap)
            return

        self.clearWindow()

        eval_script.parse_args(['--trained_model=' + model])
        self.e = EvaluationThread()
        self.ui.pushButton_terminateThread.setEnabled(True)
        self.e.start()
        loop = QEventLoop()
        QTimer.singleShot(2000, loop.quit)

    def chooseTrainedModel(self, FilePath):
        model = QtWidgets.QFileDialog.getOpenFileName(self,  "Select your model", "./weights")[0]
        if model == '':
            self.ui.pushButton_selectModel.setText('Select model')
            self.ui.pushButton_evaluate.setEnabled(False)
            return

        pos = model.find('yolact-gui')
        model = model[pos + 11:]
        pos = len(model)
        for ch in model[::-1]:
            if ch == '/':
                break
            pos = pos - 1

        post = str()
        for ch in model[::-1]:
            if ch == '.':
                break
            post += ch

        if post != 'htp':
            self.ui.display.setText('Selected file is not valid model file (.pth)!')
            self.ui.pushButton_evaluate.setEnabled(False)
            return

        self.ui.pushButton_selectModel.setText(model[pos:])
        self.validationModel = model
        if self.validationModel != '' and self.validationFile != '':
            self.ui.pushButton_evaluate.setEnabled(True)

    def chooseBenchmarkModel(self, FilePath):
        model = QtWidgets.QFileDialog.getOpenFileName(self,  "Select your model", "./weights")[0]
        if model == '':
            self.ui.pushButton_selectModel_2.setText('Select model')
            self.ui.pushButton_benchmark.setEnabled(False)
            return

        pos = model.find('yolact-gui')
        model = model[pos + 11:]
        pos = len(model)
        for ch in model[::-1]:
            if ch == '/':
                break
            pos = pos - 1

        post = str()
        for ch in model[::-1]:
            if ch == '.':
                break
            post += ch

        if post != 'htp':
            self.ui.display.setText('Selected file is not a valid model file (.pth)!')
            self.ui.pushButton_benchmark.setEnabled(False)
            return

        self.ui.pushButton_selectModel_2.setText(model[pos:])
        self.benchmarkModel = model
        if self.benchmarkModel != '':
            self.ui.pushButton_benchmark.setEnabled(True)

    def chooseValidateFile(self, FilePath):
        image = QtWidgets.QFileDialog.getOpenFileName(self,  "Select your image", "./img")[0]
        if image == '':
            self.ui.pushButton_selectImage.setText('Select image')
            self.ui.pushButton_evaluate.setEnabled(False)
            return
        pos = image.find('yolact-gui')
        image = image[pos + 11:]

        pos = len(image)
        for ch in image[::-1]:
            if ch == '/':
                break
            pos = pos - 1

        post = str()
        for ch in image[::-1]:
            if ch == '.':
                break
            post += ch

        if post != 'gpj' and post != 'gnp':
            self.ui.display.setText('Selected file is not a valid image (.jpg or .png)!')
            self.ui.pushButton_evaluate.setEnabled(False)
            return
        self.ui.pushButton_selectImage.setText(image[pos:])
        self.validationFile = image
        if self.validationModel != '' and self.validationFile != '':
            self.ui.pushButton_evaluate.setEnabled(True)

    def triggerOnlineTest(self):
        '''
        python eval.py --trained_model=weights/yolact_base_54_800000.pth --score_threshold=0.25 --top_k=15 --video_multiframe=4 --video=video/demo.mp4
        '''
        model = 'weights/yolact_base_54_800000.pth'
        score_threshold = 0.25
        video_multiframe = 4
        video = 'video/demo.mp4'  # :results/tmp_video.mp4

        eval_script.parse_args(['--trained_model=' + model, '--score_threshold=' + str(score_threshold),
                                '--top_k=15', '--video_multiframe=' + str(video_multiframe), '--video=' + video])
        self.e = EvaluationThread()
        self.e.start()
        self.d.start()


        loop = QEventLoop()
        QTimer.singleShot(2000, loop.quit)


    def clearWindow(self):
        self.ui.display.clear()
        self.ui.textBrowser_terminal.clear()

        self.validationFile = str()
        self.validationModel = str()
        self.benchmarkModel = str()
        self.ui.pushButton_selectModel.setText('Select model')
        self.ui.pushButton_selectImage.setText('Select image')
        self.ui.pushButton_evaluate.setEnabled(False)
        self.ui.horizontalSlider_scoreThreshold.setValue(15)
        self.ui.lineEdit_scoreThreshold.setText('0.15')
        self.ui.radioButton_batchEvaluation.setChecked(False)

        self.ui.pushButton_selectModel_2.setText('Select model')
        self.benchmarkNumImage = 1000
        self.ui.pushButton_benchmark.setEnabled(False)
        self.ui.lineEdit_numImage.setText('1000')
        self.ui.horizontalSlider_numImage.setValue(1000)

        self.trainConfig = 'yolact_base_config'
        self.batchSize = '1'
        self.ui.lineEdit_batchSize.setText('1')
        self.ui.lineEdit_trainConfig.setText('yolact_base_config')

        # delete tmp result
        curr_path = os.getcwd()
        delete_file = curr_path + '/results/tmp_res.jpg'
        if os.path.exists(delete_file):
            os.remove(delete_file)

    def clearTerminal(self):
        self.ui.textBrowser_terminal.clear()

    def lineEditMoveSlider(self):
        value = self.ui.lineEdit_scoreThreshold.text()
        value = float(value)
        if value < 0:
            value = 0
        if value > 0.99:
            value = 0.99

        value = format(value, '.2f')

        self.ui.lineEdit_scoreThreshold.setText(value)
        self.ui.horizontalSlider_scoreThreshold.setValue(float(value) * 100)
        self.validationScoreThreshold = float(value)

    def lineEditMoveSliderBenchmark(self):
        value = self.ui.lineEdit_numImage.text()
        value = int(value)
        if value < 100:
            value = 100
        if value > 10000:
            value = 10000

        self.ui.lineEdit_numImage.setText(str(value))
        self.ui.horizontalSlider_numImage.setValue(value)
        self.benchmarkNumImage = float(value)

    def sliderEditLineEdit(self):
        value = self.ui.horizontalSlider_scoreThreshold.value() / 100
        self.validationScoreThreshold = value
        value = format(value, '.2f')
        self.ui.lineEdit_scoreThreshold.setText(value)

    def sliderEditLineEditBenchmark(self):
        value = self.ui.horizontalSlider_numImage.value()
        self.benchmarkNumImage = value
        self.ui.lineEdit_numImage.setText(str(value))


class TrainingThread(QThread):
    signalForText = pyqtSignal(str)

    def __init__(self, args=None, data=None, parent=None):
        super(TrainingThread, self).__init__(parent)
        self.data = data
        self.args = args

    def write(self, text):
        self.signalForText.emit(str(text))

    def run(self):
        print(str(self.args))
        train_script.perform(self.args)


class BenchmarkThread(QThread):
    signalForText = pyqtSignal(str)

    def __init__(self, model=None, num=1000, data=None, parent=None):
        super(BenchmarkThread, self).__init__(parent)
        self.data = data
        self.model = model
        self.num = num

    def write(self, text):
        self.signalForText.emit(str(text))

    def run(self):
        eval_script.parse_args(['--trained_model=' + self.model, '--benchmark', '--max_images=' + str(self.num)])
        eval_script.perform(eval_script.args)


class EvaluationThread(QThread):
    signalForText = pyqtSignal(str)

    def __init__(self, data=None, parent=None):
        super(EvaluationThread, self).__init__(parent)
        self.data = data

    def write(self, text):
        self.signalForText.emit(str(text))

    def run(self):
        if eval_script.args.video is None:
            eval_script.perform()

        eval_script.perform()

class DisplayThread(QThread):
    signalForDisplay = pyqtSignal(str)

    def __int__(self):
        super(DisplayThread, self).__init__()

    def run(self):
        while True:
            self.signalForDisplay.emit('')
            time.sleep(0.33)


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    sys.exit(myapp.exec_())