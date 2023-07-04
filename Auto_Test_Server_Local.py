from time import sleep
from threading import Thread, current_thread
import os
import datetime
import random
from FileReadWrite import *
import socket
import json
import signal
import sys


def openFileForReading(file_path):
    fileHandle = open(file_path, 'r')
    return fileHandle


def readALine(fileHandle):
    line = fileHandle.readline().strip()
    return line


def closeFile(fileHandle):
    fileHandle.close()

def write_to_file(studentNumber,studentName,client_info, answers, score):
    with open('ClientsInfo.txt', 'a') as file:
        file.write("Student Information:\t")
        file.write("IP: " + client_info[0] + "\t")
        file.write("Port: " + str(client_info[1]) + "\t")
        file.write("Number: " + str(studentNumber) + "\t")
        file.write("Name: " + studentName + "\n\n")
        
        file.write("Answers:")
        for index, answer in enumerate(answers):
            file.write("Question " + str(index+1) + ": " + answer + "\t")
        file.write("\nScore:\n")
        file.write(str(score )+ "% \n")
        file.write("***********************************\n\n")

    with open('results.csv', 'a') as resfile:
        
        resfile.write( str(studentNumber) + ", ")
        resfile.write(studentName + ", ")
        resfile.write(str(score) + '%'"\n")

        

def Aotu_Test_F(csocket, ip, port):
    strlist = []
    print("In function: current_thread", current_thread().name)
    f = open('users.txt', 'r').read()
    while True:
        print('Server is waiting for Student Number:')
        csocket.send('Enter Your Number pls:'.encode())
        u_num = csocket.recv(1024).decode()
        print("s_num", u_num)

        print('Server is waiting for Student Name:')
        csocket.send('Enter Your full Name pls:'.encode())
        u_name = csocket.recv(1024).decode()
        print("s_name", u_name)

        if u_num in f:
            break

    FILE_PATH = 'Quiz.txt'
    LETTERS_LIST = ['a', 'b', 'c', 'd']
    fileHandle = openFileForReading(FILE_PATH)
    titleText = readALine(fileHandle)
    nQuestions = readALine(fileHandle)
    nQuestions = int(nQuestions)

    s = 'Test Info: '
    strlist.append(s)
    strlist.append(titleText)
    s = '-' + str(nQuestions) + ' Quiz'
    strlist.append(s)
    s = "Start Test....."
    strlist.append(s)

    score = 0
    for questionNumber in range(0, nQuestions):
        questionText = readALine(fileHandle)
        answers = []
        for i in range(0, 4):
            thisAnswer = readALine(fileHandle)
            answers.append(thisAnswer)

        correctAnswer = answers[0]
        random.shuffle(answers)
        indexOfCorrectAnswer = answers.index(correctAnswer)

        s = str(questionNumber + 1) + '. ' + questionText
        strlist.append(s)

        for index in range(0, 4):
            thisLetter = LETTERS_LIST[index]
            thisAnswer = answers[index]
            thisAnswerLine = "" + str(thisLetter) + ") " + str(thisAnswer)
            strlist.append(thisAnswerLine)

        while True:
            s = "Please answer with (a, b, c, d): "
            strlist.append(s)
            s = "\n".join(strlist)
            csocket.sendall(s.encode())
            strlist = []
            userAnswer = csocket.recv(1024).decode()
            userAnswer = userAnswer.lower()
            if not userAnswer:
                break
            print('User reply is:', userAnswer)
            if userAnswer in LETTERS_LIST:
                break
            else:
                csocket.send('Please enter a, b, c, or d'.encode())

        indexOfUsersAnswer = LETTERS_LIST.index(userAnswer)
        if indexOfCorrectAnswer == indexOfUsersAnswer:
            score = score + 1
            print(str(u_num)+':'+u_name+':Correct! Answered Question count:', score)
        else:
            print(str(u_num)+':'+u_name+":Wrong Answer.")
            correctLetter = LETTERS_LIST[indexOfCorrectAnswer]
            print('The correct answer was:', correctLetter + ') ' + correctAnswer)
            print(str(u_num)+':'+u_name+':Number of Answered Questions:', score)

    pctCorrect = (score * 100.0) / nQuestions
    print()
    currentdate = datetime.datetime.now()
    sres = str(u_num) + ';' + str(pctCorrect) + '% ' + ';' + str(currentdate.date()) + ';' + str(
        csocket.getpeername())  + '\n'
    s = '>>>'+'datetime:' + str(currentdate) +' >> '+str(u_num)+':'+u_name+ ', Your Score is: ' + str(pctCorrect) + '%'
    print(s)
    write_to_file(u_num,u_name,(ip, port), LETTERS_LIST, pctCorrect)

    csocket.send(s.encode())
    csocket.recv(1024).decode()
    csocket.send('done'.encode())
  
    closeFile(fileHandle)
    csocket.close()


class ClientThread(Thread):
    def __init__(self, ip, port, csocket):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = csocket
        print("New server socket thread started for: " + ip + ":" + str(port))

    def run(self):
        Aotu_Test_F(self.csocket, self.ip, self.port)


ssocket = socket.socket()
addr = ('0.0.0.0', 5555)
ssocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ssocket.bind(addr)
ssocket.listen(5)
clients = []
threads = []


def signal_handler(signal, frame):
    print("Stopping server...")
    ssocket.close()
    for t in threads:
        t.join()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

while True:
    try:
        print("Multithreaded Python server: Waiting for connections...port=5555")
        (csocket, (ip, port)) = ssocket.accept()
        newthread = ClientThread(ip, port, csocket)
        newthread.start()
        threads.append(newthread)
        print('clients', clients)
    except Exception as e:
        print("An error occurred while accepting a connection:", str(e))

        print('Working with', (ip, port))
        write_to_file((ip, port), [], "")

