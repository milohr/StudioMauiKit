# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
#
# License: GNU Lesser General Public License v3.0 (LGPLv3)
from PySide2 import QtGui
from PySide2.QtCore import QObject, Slot
from PySide2.QtCore import QSettings
from PySide2.QtQml import QQmlContext, QQmlExpression
from PySide2.QtCharts import QtCharts
from src.controlers.charts import SeriesType
from src.controlers.util import get_data_path, get_data
from src.controlers.custom_pdf import CustomPDF


class Process(QObject):
    
    def __init__(self, engine):
        QObject.__init__(self)
        self.m_engine = engine
        self.project_name = ''
        self.process_name = list()
        self.process_description = list()
        self.action_name = list()
        self.settings = QSettings("Nebula")
        self.dat = dict()
    
    @Slot(str, str, result = 'QString')
    def process_settings(self, project_name, action_name):
        self.project_name = project_name
        self.action_name.append(action_name)
        self.settings = QSettings("Nebula", self.project_name)
        self.settings.beginGroup("ProcessInfo")
        self.settings.beginWriteArray(action_name)
        s = [str(i) for i in self.dat[project_name]]
        res = ",".join(s)
        for i in range(len(self.process_name)):
            self.settings.setArrayIndex(i)
            self.settings.setValue("Name", self.process_name[i])
            self.settings.setValue("Description", self.process_description[i])
            self.settings.setValue("Value", res)
        self.settings.endArray()
        self.settings.endGroup()
        print(self.settings.fileName())
        return self.settings.fileName()
    
    def process_info(self, name = "", description = ""):
        self.process_name.append(name)
        self.process_description.append(description)
        
    @Slot(str, result = bool)
    def generate_pdf(self, project_name):
        self.settings = QSettings("Nebula", project_name)
        
        pdf = CustomPDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Times', 'B', 15)
        pdf.cell(0, 5, 'Project details', ln = 1)
        pdf.set_font('Times', '', 10)
        self.settings.beginGroup("Project")
        pdf.cell(0, 10, txt = "Name: {}".format(self.settings.value("Name")), ln = 1)
        pdf.cell(0, 10, txt = "Project creation date: {}".format(self.settings.value("Date")), ln = 1)
        pdf.cell(0, 10, txt = "Inform creation date: {}".format(self.settings.value("LastEdit")), ln = 1)
        pdf.cell(0, 10, txt = " ", ln = 1)
        self.settings.endGroup()
        pdf.set_font('Times', 'B', 15)
        pdf.cell(0, 5, 'Signals', ln = 1)
        pdf.set_font('Times', '', 10)
        self.settings.beginGroup("SignalFiles")
        pdf.cell(0, 10, txt = "Signals path: {}".format(self.settings.value("Path")), ln = 1)
        path = self.settings.value("Path")
        pdf.cell(0, 10, txt = " ", ln = 1)
        self.settings.endGroup()
        pdf.set_font('Times', 'B', 15)
        pdf.cell(0, 5, 'Information', ln = 1)
        pdf.set_font('Times', '', 10)
        self.settings.beginGroup("Info")
        size = self.settings.beginReadArray("sfreq")
        for i in range(size):
            self.settings.setArrayIndex(i)
            pdf.cell(0, 10, txt = "{}. sfreq: {}".format(i, self.settings.value("sfreq")), ln = 1)
        self.settings.endArray()
        size = self.settings.beginReadArray("SubjectInfo")
        for i in range(size):
            self.settings.setArrayIndex(i)
            pdf.cell(0, 10, txt = "{}. id: {}".format(i, self.settings.value("id")), ln = 1)
            pdf.cell(0, 10, txt = "{}. First name: {}".format(i, self.settings.value("first_name")), ln = 1)
            pdf.cell(0, 10, txt = "{}. Last name: {}".format(i, self.settings.value("last_name")), ln = 1)
            pdf.cell(0, 10, txt = "{}. Hand: {}".format(i, self.settings.value("hand")), ln = 1)
            pdf.cell(0, 10, txt = "{}. Sex: {}".format(i, self.settings.value("sex")), ln = 1)
        self.settings.endArray()
        self.settings.endGroup()
        pdf.cell(0, 10, txt = " ", ln = 1)
        pdf.set_font('Times', 'B', 15)
        pdf.cell(0, 5, 'Process', ln = 1)
        pdf.set_font('Times', '', 10)
        self.settings.beginGroup("ProcessInfo")
        for action_name in self.action_name:
            size = self.settings.beginReadArray(action_name)
            for i in range(size):
                self.settings.setArrayIndex(i)
                pdf.cell(0, 10, txt = "{}. Name: {}".format(i, self.settings.value("Name")), ln = 1)
                pdf.cell(0, 10, txt = "{}. Description: {}".format(i, self.settings.value("Description")), ln = 1)
                pdf.cell(0, 10, txt = "{}. Value: {}".format(i, self.settings.value("Value")), ln = 1)
            self.settings.endArray()
        self.settings.endGroup()
        pdf.cell(0, 10, txt = " ", ln = 1)
        print(path)
        pdf.output('{}_report.pdf'.format(project_name))
        print(f'PDF: {project_name}')
        return True
    
    @Slot(QObject, result = "QVariantList")
    def add_chart_bar(self, chart_view):
        # https://stackoverflow.com/questions/57536401/how-to-add-qml-scatterseries-to-existing-qml-defined-chartview
        context = QQmlContext(self.m_engine.rootContext())
        context.setContextProperty("chart_view", chart_view)
        # context.setContextProperty("type", SeriesType.SeriesTypeBar.value)
        context.setContextProperty("type", SeriesType.SeriesTypePie.value)
        
        script = """chart_view.createSeries(type, "Pie series");"""
        expression = QQmlExpression(context, chart_view, script)
        serie = expression.evaluate()[0]
        if expression.hasError():
            print(expression.error())
            return
        print(serie, expression)
        data = self.dat[self.project_name]
        print(f'FROM ADD PIE CHART {data} and type {type(data)}')
        serie.append("a", 10.0)
        serie.append("b", 80.0)
        # serie.append("a", data[0] * 1000)
        # serie.append("b", data[1] * 1000)
        # serie.append("c", data[2] * 1000)
        # serie.append("b", data)
        return data
    
    @Slot(QtCharts.QAbstractSeries)
    def fill_serie(self, serie):
        import random
        mx, Mx = 0, 10
        my, My = -100, 100
        data = self.dat[self.project_name]
        serie.append(1, data[0]*1000)
        serie.append(2, data[1]*1000)
        serie.append(3, data[2]*1000)
        # for _ in range(100):
        #     x = random.uniform(mx, Mx)
        #     y = random.uniform(my, My)
        #     serie.append(x, y)
        # https://doc.qt.io/qt-5/qml-qtcharts-scatterseries.html#borderColor-prop
        serie.setProperty("borderColor", QtGui.QColor("salmon"))
        # https://doc.qt.io/qt-5/qml-qtcharts-scatterseries.html#brush-prop
        serie.setProperty("brush", QtGui.QBrush(QtGui.QColor("green")))
        # https://doc.qt.io/qt-5/qml-qtcharts-scatterseries.html#borderColor-prop
        serie.setProperty("borderWidth", 4.0)
    
    
    # Process Example
    @Slot(str, result = "QVariantList")
    def my_process_1(self, project_name):
        import statistics
        self.process_info("process_1", "std, variance and mean from channel 0")
        data = get_data_path(project_name)
        print(data, data[0])
        data = get_data(data[0])
        print(data.shape)
        var = statistics.variance(data[0, :])
        mean = statistics.mean(data[0, :])
        std = statistics.stdev(data[0, :])
        value = [std * 1000, float(var) * 1000, float(mean) * 1000]
        self.dat[project_name] = value
        print(value)
        return value

