import subprocess



class Out:
    def __init__(self):
        print("xxxxx")
        self.file = open("std_out","a")
        self.fileno = self.file.fileno
        print(self.fileno)

    def append(self, txt):
        print(txt,"----")
        self.file.append(txt)
    
    def close(self):
        print("+++++")
        self.file.close()


std_out = Out()

subprocess.call(["ls", "-l"],stdout=std_out)

std_out.close()
