import argparse
import json
import sys
import os
from shutil import copytree, ignore_patterns, make_archive, rmtree
import requests
import tkinter as tk
import re
import datetime
import traceback


# serverUrl = "http://localhost:8080/api/v1/"
serverUrl = "https://test.api.codelock.ai/api/v1/"


class CliApplication():

    def __init__(self) -> None:
        os.environ['TK_SILENCE_DEPRECATION'] = "1"
        homePath = os.path.expanduser("~")
        credFilePath = os.path.join(homePath, "cred")
        isFileAvailable = os.path.exists(credFilePath)
        # print(isFileAvailable, os.path.join(homePath, "cred"), os.getcwd())

        if isFileAvailable:
            data = open(credFilePath, "r")
            userData = json.load(data)
            data.close()
            self.token = userData.get("token")
            self.token_expiry = userData.get("token_expiry")
            self.refresh_token = userData.get("refresh_token")
            self.refresh_token_expiry = userData.get("refresh_token_expiry")
            self.pat = userData.get("pat")
            date_now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
            # print(date_now, self.token_expiry)
            # print(date_now > self.token_expiry)

            if date_now > self.token_expiry:
                if date_now > self.refresh_token_expiry:
                    self.__dict__.pop("token", None)
                    self.loginModal()
                else:
                    self.getFreshTokens()

            # sys.exit()
        else:
            self.loginModal()

    def getFreshTokens(self):
        # print("I am here", self.refresh_token)
        response = requests.post(
            serverUrl + "cli-refresh-token",
            data={"refreshToken": self.refresh_token})
        if response.status_code == 200:
            data = response.json()

            date1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            date2 = datetime.datetime.strptime(date1, "%Y-%m-%d %H:%M:%S.%f")
            token_expiry_time = date2 + \
                datetime.timedelta(
                    minutes=data["tokens"]["access"]["duration"])
            refresh_token_expiry_time = date2 + \
                datetime.timedelta(
                    minutes=data["tokens"]["refresh"]["duration"])

            tokenData = {"token": data["tokens"]["access"]["token"],
                         "token_expiry": token_expiry_time.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                         "refresh_token": data["tokens"]["refresh"]["token"],
                         "refresh_token_expiry": refresh_token_expiry_time.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                         "pat": self.pat}
            userData = json.dumps(tokenData, indent=2)
            credFile = open(os.path.join(os.path.expanduser("~"), "cred"), "w")
            credFile.write(userData)
            credFile.close()
            self.token = data["tokens"]["access"]["token"]
        else:
            self.loginModal()

    def loginModal(self):
        self.credentials = tk.Tk()
        self.credentials.title("Login")
        self.loginOption = "admin"
        self.credentials.geometry("225x150")

        rowIndex = 0

        # Organization Account Id.
        ocmd = (self.credentials.register(self.checkOrg), "%P")
        org = tk.Label(self.credentials, text="Account Id.").grid(
            row=rowIndex, column=0)
        self.org_input = tk.Entry(self.credentials)
        self.org_input.config(validate="focusout", validatecommand=ocmd)
        self.org_input.grid(row=rowIndex, column=1)
        org_validation = tk.Label(self.credentials, text="")
        org_validation.grid(row=(rowIndex + 1), column=1)
        self.wdgOrgLst = org_validation

        # Email
        vcmd = (self.credentials.register(self.checkEmail), "%P")
        email = tk.Label(self.credentials, text="Email")
        email.grid(row=(rowIndex + 2), column=0)
        self.email_input = tk.Entry(self.credentials)
        self.email_input.config(
            validate="focusout", validatecommand=vcmd)
        self.email_input.grid(row=(rowIndex + 2), column=1)
        email_validation = tk.Label(self.credentials, text="")
        email_validation.grid(row=(rowIndex + 3), column=1)
        self.wdgLst = email_validation

        # Password
        pwd = tk.Label(self.credentials, text="Password").grid(
            row=(rowIndex + 4), column=0)
        self.pwd_input = tk.Entry(self.credentials, show="*")
        self.pwd_input.grid(row=(rowIndex + 4), column=1)
        pat = tk.Label(self.credentials, text="PAT").grid(
            row=(rowIndex + 5), column=0)
        self.pat_input = tk.Entry(self.credentials)
        self.pat_input.grid(row=(rowIndex + 5), column=1)
        self.submit = tk.Button(self.credentials, text="Login",
                                command=self.closeLoginScreen, state="disabled")
        self.submit.grid(row=(rowIndex + 7), column=0)

        self.credentials.mainloop()

    def checkOrg(self, val):
        regex = '^[0-9]{1,6}$'
        if re.search(regex, val):
            self.wdgOrgLst.configure(
                text='Organization Id. is valid!', foreground="GREEN")
            return True
        else:
            self.wdgOrgLst.configure(
                text='Organization Id. is Invalid!', foreground="RED")
            return False

    def checkEmail(self, val):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not val:
            self.wdgLst.configure(text='Email is required!', foreground="RED")
        elif re.search(regex, val):
            self.wdgLst.configure(text='Email is valid!', foreground="GREEN")
            self.submit.config(state="normal")
            return True
        else:
            self.wdgLst.configure(text='Email is Invalid!', foreground="RED")
            return False

    # def getSelection(self, widget):
    #     self.loginOption = widget["value"]
    #     print(widget["text"], self.loginOption, type(self.loginOption))

    def splitme(self, s):
        if (s[:1] == "/"):
            return s[1:]
        else:
            return(s)

    def getAvailableRepos(self):
        response = requests.get(
            serverUrl + "cli-get-all-repository-list",
            headers={"authorization": "Bearer " + self.token})
        # print("Server status code: ", response.status_code)
        # print("I am here", len(data["result"]))
        if response.status_code == 200:
            data = response.json()
            return data["result"]["repositorys"]
        else:
            # print(response.json())
            data = response.json()
            if data["error"]:
                print(data["error"])
                sys.exit()
            else:
                return []

    def pushCodeInRepo(self, commit, repo, branch, codefile):
        # print(commit, repo)
        response = requests.post(
            serverUrl + "cli-push-code/"+repo,
            headers={"authorization": "Bearer " + self.token},
            data={"commit": commit, "branch": branch,
                  "personalAccessToken": self.pat},
            files={"code": ("code.zip", codefile)})
        print("Server response: ", response.status_code)
        if response.status_code == 200:
            # data = response.json()
            print("Code successfully pushed")
        else:
            try:
                codefile.close()
                print("Server error!", response.json())
            except ValueError:
                print("Server response have not data in it.")
                sys.exit()
            except:
                traceback.print_exc()
                sys.exit()

    def validateUser(self, org, email, password):
        response = requests.post(
            serverUrl + "cli-login",
            data=(({"email": email, "password": password}, {"accountId": int(org), "email": email, "password": password})[int(org) > 0]))
        # print("Login status code: ", response.text)
        if response.status_code == 200:
            data = response.json()
            # print(data["tokens"]["refresh"]["token"])
            date1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            date2 = datetime.datetime.strptime(date1, "%Y-%m-%d %H:%M:%S.%f")
            token_expiry_time = date2 + \
                datetime.timedelta(
                    minutes=data["tokens"]["access"]["duration"])
            refresh_token_expiry_time = date2 + \
                datetime.timedelta(
                    minutes=data["tokens"]["refresh"]["duration"])
            tokenData = {"token": data["tokens"]["access"]["token"],
                         "token_expiry": token_expiry_time.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                         "refresh_token": data["tokens"]["refresh"]["token"],
                         "refresh_token_expiry": refresh_token_expiry_time.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                         "pat": self.pat, }
            userData = json.dumps(tokenData, indent=2)
            credFile = open(os.path.join(os.path.expanduser("~"), "cred"), "w")
            credFile.write(userData)
            credFile.close()
            self.token = data["tokens"]["access"]["token"]
            return True
        else:
            print("Error")
            return False
        # if email != "abc":
        #     sys.exit(0)

    def closeLoginScreen(self):
        self.org = self.org_input.get()
        self.email = self.email_input.get()
        self.pwd = self.pwd_input.get()
        self.pat = self.pat_input.get()
        self.credentials.destroy()

    def onerror(self, func, path, exc_info):
        import stat
        # Is the error an access error?
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise

    def deleteTemps(self):
        if os.path.isdir(os.path.join(os.getcwd(), "code_zip")):
            rmtree(os.path.join(os.getcwd(), "code_zip"),
                   ignore_errors=False, onerror=self.onerror)
            if os.path.exists(os.path.join(os.getcwd(), "code.zip")):
                os.remove(os.path.join(os.getcwd(), "code.zip"))

    def codepush(self):

        cd_parser = argparse.ArgumentParser(description="Codelock")
        cd_parser.add_argument("action", metavar="action", type=str,
                               help="Action to perform", choices=["push"])
        cd_parser.add_argument("remote", metavar="remote", type=str,
                               help="Path to upload the code", choices=["origin"])
        cd_parser.add_argument("branch", metavar="branch", type=str,
                               help="Branch to perform action on")

        args = cd_parser.parse_args()

        dest_action = args.action
        dest_remote = args.remote
        dest_branch = args.branch

        try:
            validatedUser = True
            # print("Here: ", self.org, self.email, self.pwd)

            if not hasattr(self, "token"):
                if not hasattr(self, "org"):
                    validatedUser = self.validateUser(
                        0, self.email, self.pwd)
                else:
                    validatedUser = self.validateUser(
                        self.org or 0, self.email, self.pwd)

            if not validatedUser:
                print("User validation failed!")
                sys.exit(0)

            repos = self.getAvailableRepos()
            # print("Repos length: ", len(repos))

            if len(repos) > 0:
                optionNo = 0
                for repo in repos:
                    optionNo += 1
                    print(optionNo, ":", repo["repository_name"])
                option = int(input("Select the repo: "))
                while option < 1 or option > len(repos):
                    print("Please select an option number from the list above!")
                    option = int(input("Select the repo: "))

                commitMsg = input("Please enter commit message: ")
                # print("Selected option: ",
                #       repos[option]["listener_branch"], repos[option]["_id"])
                # print("Commit message: ", commitMsg)

                exculde_array = ["*.zip", "code_zip"]
                if os.path.exists(".gitignore"):
                    for line in open(".gitignore"):
                        li = line.strip()
                        if not li.startswith("#"):
                            exline = self.splitme(line.strip())
                            if exline != "":
                                exculde_array.append(exline)

                # if os.path.isdir(os.path.join(os.getcwd(), "code_zip")):
                #     rmtree(os.path.join(os.getcwd(), "code_zip"),
                #            ignore_errors=False, onerror=self.onerror)

                self.deleteTemps()

                copytree(os.getcwd(), os.path.join(os.getcwd(), "code_zip"),
                         ignore=ignore_patterns(*exculde_array))
                make_archive("code", "zip", os.path.join(
                    os.getcwd(), "code_zip"))

                # print("test: ", option)
                codefile = open(os.path.join(os.getcwd(), "code.zip"), "rb")
                self.pushCodeInRepo(
                    commitMsg, repos[option-1]["_id"], dest_branch, codefile)

                codefile.close()

                self.deleteTemps()

                sys.exit()
            else:
                # val = input("Enter you choice: ")
                print("You have no assigned repos!")
                sys.exit()
        except AttributeError:
            print("Error occured while verifying user!")
        except SystemExit:
            self.deleteTemps()
            print("Done!")
        except:
            traceback.print_exc()


def run():
    CliApplication().codepush()


if __name__ == '__main__':
    run()
