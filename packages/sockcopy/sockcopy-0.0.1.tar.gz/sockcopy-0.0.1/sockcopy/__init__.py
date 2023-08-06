import os
import os.path as path
import subprocess as sp

__all__ = ['Send',  'Receive']

COMMAND_WAITING = ':-waiting-:'
COMMAND_COMPLETED = ':-completed-:'
COMMAND_RECEIVED = ':-received-:'


SEPERATOR = ' :%-seperator-%: '
SEP = ' :-sep-: '
CHUNK = ' :-chunk-: '
NOTAVAILABLE = ':-NotAvailable-:'
START = ':-START-:'


def init_data(byte):
    kilobyte = byte / 1024
    megabyte = kilobyte / 1024
    gigabyte = megabyte / 1024

    values = [[gigabyte, 'GB'], [megabyte, 'MB'], [kilobyte, 'KB'], [byte, 'B']]

    for value, unit in values:
        check_value = int(value)
        if check_value != 0:
            return f'{round(value, 2)} {unit}'
    else:
        return f'{round(value, 2)} {unit}'


def attributes(filename):
    check = path.isfile(filename)
    
    if check == True:
        file_path = path.abspath(filename)

        with open(file_path, 'r') as file:
            filename = file.name

        status = os.stat(file_path)
        file_size = status.st_size

        return file_path, filename, file_size


#############################################################################
#                                                                           #
#                                 :- SEND -:                                #
#                                                                           #
#############################################################################


class Send:
    def __init__(self, conn, source):
        self.conn = conn
        self.folders = []
        self.files = []

        self.command = None

        self.pwd = path.abspath('.')

        self.new_source = path.abspath(source)

        self.directory(source)

        if len(self.folders) > 0:
            for folder in self.folders:
                self.directory(folder)
            else:
                self.main_folder = self.new_source.split('\\')[-1]
                send_attributes = self.init_attributes([self.main_folder, self.files, self.folders]).encode()
        else:
            if path.isfile(source):
                abs_path = path.abspath(source)

                self.main_folder = NOTAVAILABLE
                self.files.append(f'{attributes(abs_path)[2]}{SEP}{abs_path}')
                send_attributes = self.init_attributes([self.main_folder, self.files, self.folders]).encode()
            else:
                self.main_folder = self.new_source.split('\\')[-1]
                send_attributes = self.init_attributes([self.main_folder, self.files, self.folders]).encode()
        

        # sends size of attributes it is about to send and waits for receiver to reply it has received it
        self.send(str(len(send_attributes)).encode())

        self.command = self.receive_command()

        while self.command != COMMAND_RECEIVED:
            self.command = self.receive_command()

        self.send(send_attributes) # sends the attributes

        while self.command != COMMAND_WAITING:
            self.command = self.receive_command()
        else:
            for index in range(len(self.files)):
                self.files[index] = self.files[index].split(SEP)
                data = self.binary(self.files[index][1])
                self.send(data)

                self.command = self.receive_command()
                while self.command != COMMAND_RECEIVED:
                    self.command = self.receive_command()
            else:
                self.send(COMMAND_COMPLETED.encode())
                self.clean()



    def directory(self, _path):
        if path.exists(_path) and path.isdir(_path):

            for item in os.scandir(_path):
                abs_path = path.abspath(item.path)

                if item.is_file():
                    self.files.append(f'{attributes(abs_path)[2]}{SEP}{abs_path}')
                elif item.is_dir():
                    self.folders.append(abs_path)


    def send(self, package):
        self.conn.send(package)

    def binary(self, file):
        if path.isfile(file):
            with open(file, 'rb') as send_file:
                data = send_file.read()
                _byte = bytes(data)
                return _byte
    
    def init_attributes(self, items):
        send_attributes = []
        for item in items:
            item = SEPERATOR.join(item)    
            send_attributes.append(item)
        else:
            return CHUNK.join(send_attributes)
        
    def receive_command(self):
        return self.conn.recv(1023).decode()
    
    def clean(self):
        self.folders.clear()
        self.files.clear()
        self.main_folder = None
        os.chdir(self.pwd)


#############################################################################
#                                                                           #
#                                :- RECEIVE -:                              #
#                                                                           #
#############################################################################


class Receive:
    def __init__(self, conn, destination):
        self.folders = []
        self.files = []

        self.conn = conn
        

        self.pwd = path.abspath('.')
        self.destination = path.abspath(destination)

        attributes_size = int(self.conn.recv(1024).decode())
        self.send_command(COMMAND_RECEIVED)

        receive_attributes = self.conn.recv(attributes_size * 2).decode()
        
        self.init_attributes(receive_attributes)
        if self.main_folder != None:
            self.make_folder()
            
        self.send_command(COMMAND_WAITING)

        #receive file binary and tag it
        data_received = 0
        total_data = len(self.files)
        received = START.encode()

        while received != COMMAND_COMPLETED.encode():
            if data_received != total_data:
                file = self.files[data_received]
                file_size = int(file[0]) * 2
                file_name = file[1]

                received = self.receive_files(file_size)
                data_received += 1

                self.save_files(received, file_name)

                self.send_command(COMMAND_RECEIVED)
            else:
                received = self.receive_files(1024)
        else:
            self.clean()
            
    def make_folder(self):
        if path.exists(self.destination) and path.isdir(self.destination):
            os.chdir(self.destination)
            sp.run(f'mkdir "{self.main_folder}"', shell=True)
            os.chdir(self.main_folder)

            for folder in self.folders:
                folder = folder.split(self.main_folder)[1][1:]
                sp.run(f'mkdir {folder}', shell=True)
        

    def receive_files(self, size):
        return self.conn.recv(size)
    
    def send_command(self, command):
        self.conn.send(command.encode())

    def save_files(self, _byte, filename):
        receive_file = filename

        if self.main_folder != None:
            file = receive_file.split(self.main_folder)[1]
            receive_file = f'{self.destination}\\{self.main_folder}{file}'
        else:
            file = receive_file.split('\\')[-1]
            receive_file = f'{self.destination}\\{file}'


        with open(receive_file, 'wb') as receive_file:
            data = bytearray()

            for index, value in enumerate(_byte):
                data.append(0)
                data[index] = value
            else:
                receive_file.write(data)

                #REMOVE PRINT
                # print('[+]', init_data(len(data)), 'received')

    def clean(self):
        self.folders.clear()
        self.files.clear()
        self.main_folder = None
        os.chdir(self.pwd)

    def init_attributes(self, items):
        items = items.split(CHUNK)

        main_folder = items[0].split(SEPERATOR)
        main_folder = ''.join(main_folder)
        if main_folder == NOTAVAILABLE:
            main_folder = None

        files = items[1].split(SEPERATOR)

        for index in range(len(files)):
            files[index] = files[index].split(SEP)

        folders = items[2].split(SEPERATOR)

        if len(folders) <= 1 and folders[0] == '':
            # folders = ':-NotAvailable-:'
            folders = []

        self.main_folder, self.files,  self.folders = main_folder, files, folders
