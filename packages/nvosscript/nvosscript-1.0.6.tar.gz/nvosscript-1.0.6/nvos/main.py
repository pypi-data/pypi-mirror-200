# This is a sample Python script.
import os.path
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import logging
import getpass
from nvos import login, run, remote, utils


# 创建全局记录器
# 配置日志格式化信息
logging.basicConfig(filename=os.path.expanduser(os.path.join("~", "logger.log")), level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def main():
    command = sys.argv[1]
    if command.lower() == "login":
        username = input("email：")
        password = getpass.getpass("password：")
        status = login.login_user_check(username, password)
        print(status)
    elif command.lower() == "init":
        run.command_init()
    elif command.lower() == "async":
        run.command_async()
    elif command.lower() == "pull":
        run.command_pull()
    elif command.lower() == "push":
        run.command_push()
    elif command.lower() == "-v" or command.lower() == "--v" or command.lower() == "version":
        print("1.0.6")
    elif command.lower() == "-h" or command.lower() == "--h" or command.lower() == "help":
        print(
            "\t login \t\t\t The login command is the first command that must be executed.\n")
        print(
            "\t init \t\t\t The Init command is used to initialize the workspace. Please execute the command in your workspace directory\n")
        print("\t pull \t\t\t The pull command pulls the data you modify from the cloud\n")
        print("\t push \t\t\t The push command is used upload local new files or folders to the cloud\n")
        print("\t async \t\t\t The async command automatically synchronizes the data you modify from the cloud\n")
        print("\t version \t\t\t The version command will tell you this script really version\n")
        print("\t if you still have many things you don't understand,you can take a look as https://nio.feishu.cn/wiki/wikcn9L7Di4ILQKaNmDDTrmpLqg ")

if __name__ == '__main__':
    main()
    # flag = utils.check_subdirectory_workspace_exist("/Users/andre.zhao/Documents/test")
    # print(flag)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
