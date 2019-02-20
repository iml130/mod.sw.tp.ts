from antlr4 import *
from TaskLexer import TaskLexer
from TaskParserListener import TaskParserListener
from TaskParser import TaskParser
import sys
import urllib

from TaskSupervisor.task import Task
from TaskSupervisor.taskInfo import TaskInfo

class PythonListener(TaskParserListener):
    def __init__(self):
        # Key, Value -> TemplateStr, [List of set Attr]
        self.templateDict = dict()
        # defined instances
        self.instances = []
        # defined tasks
        self.tasks = []
        self.taskInfoList = {}
        
        # last visited template
        self.lastVisitedTemplate = None

        self.latstVistedTask = None

    def enterTemplate(self, ctx):
        # Get Templatename and removing Template prefix
        tempStr =  ctx.TemplateStart().getText()[9:] 
        self.templateDict[tempStr] = []
        self.lastVisitedTemplate = tempStr

    def enterInnerTemplate(self, ctx):
        for ele in ctx.AttributeInTemplate():
            self.templateDict[self.lastVisitedTemplate].append(ele.getText())

    def enterInstance(self, ctx):
        instanceStart =  ctx.InstanceStart().getText().split()
        self.lastVisitedTemplate = instanceStart[0]
        self.instances.append(instanceStart[1])

    def enterInnerInstance(self, ctx):
        attrCount = 0
        for ele in ctx.AttributeInInstance():
            
            #Check if Template is already defined!
            if self.lastVisitedTemplate not in self.templateDict:
                raise Exception( "Template: " + self.lastVisitedTemplate + " was never declared!")

            # Check if all attrs are set within 
            if ele.getText() not in self.templateDict[self.lastVisitedTemplate]:
                raise Exception("Attribute: " + ele.getText() + " is not defined in template for instance: " + self.instances[-1])

            # Count set attributes
            attrCount += 1

        # Check if only necessary number of attrs are set
        if len(self.templateDict[self.lastVisitedTemplate]) > attrCount:
            raise Exception("One or more attributes are missing or set multiple times in: " + self.instances[-1])


    def enterTask(self, ctx): 
        t = TaskInfo(ctx.TaskStart().getText()[5:])

        self.tasks.append(ctx.TaskStart().getText()[5:])
        self.taskInfoList[t.name] = t
        self.latstVistedTask = self.taskInfoList[t.name]

    def exitTask(self, ctx):
        #print ctx.getText()
        pass

    def enterInnerTask(self, ctx):
       
        for ele in ctx.NewInstance():
            if ele.getText() not in self.instances:
                raise Exception("Instance: " + ele.getText() + " was not previosuly defined!")
            print ele.getText()

        for ele in ctx.NewTask():
            if ele.getText() not in self.tasks:
                raise Exception("Task: " + ele.getText() + " was not previosuly defined!")
            else:
                self.latstVistedTask.addChild(ele.getText())
        pass

    
    def enterTransportOrder(self, ctx):

        for ele in ctx.NewInstance():
            print ele.getText()
            if ele.getText() not in self.instances:
                raise Exception("Instance: " + ele.getText() + " was not previosuly defined!")
            self.latstVistedTask.transportFrom.append(ele.getText())
        self.latstVistedTask.transportTo.append(self.latstVistedTask.transportFrom[-1])
        self.latstVistedTask.transportFrom = self.latstVistedTask.transportFrom[:-1]
     


def checkTaskLanguage(_taskLanguage):
    try:
        lexer = TaskLexer(InputStream(_taskLanguage))
        stream = CommonTokenStream(lexer)
    
        parser = TaskParser(stream)
        tree = parser.program() 
     
        printer = PythonListener() 
        walker = ParseTreeWalker()
        walker.walk(printer, tree)
    except Exception as expression:
        print expression
        return -1, expression.message
    return 0, "Success"


def main():
    defText = "####v1\ntemplate Position\n       position\n      type\nend\n\ntemplate Sensor\n  sensorId\n      type  \nend\n\n####\n\nPosition moldingPallet\ntype %3D %22pallet%22\n      position %3D %22moldingArea_palletPlace%22\nend\n\nPosition warehouse_pos1\n        type %3D %22pallet%22\n position %3D %22warehouse_destination_pos%22\nend\n\nSensor buttonPalletIsReady\n       sensorId %3D %22buttonMoldingArea%22\n      type %3D %22Boolean%22 \nend\n\n####\n\ntask Transport_moldingPallet\n  Transport \n        from moldingPallet \n   to warehouse_pos1\nend"
    defText = decode(defText)
    print repr(defText)
    print "__________"
    print repr(open("examples.txt").read())
    #lexer = TaskLexer(InputStream(defText))
    lexer = TaskLexer(InputStream(open("simpleTask.txt").read()))
    stream = CommonTokenStream(lexer)
    parser = TaskParser(stream)
    tree = parser.program() 
    
    try:
        printer = PythonListener() 
        walker = ParseTreeWalker()
        walker.walk(printer, tree)
    except Exception:
        print expression
    

if __name__ == '__main__':
    main() 

