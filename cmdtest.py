import cmd

class MyCmd(cmd.Cmd):
    def do_send(self, line):
        pass

    def do_xD(self, line):
        pass

if __name__ == '__main__':
    my_cmd = MyCmd()
    my_cmd.cmdloop()

