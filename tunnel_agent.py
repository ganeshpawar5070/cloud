import json
import time
import subprocess
import re
import os


FILE = "control.json"

cloudflared_process = None
last_url = ""


def git_pull():
    try:
        subprocess.run(
            ["git", "pull"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print("Git pull error:", e)


def git_push():

    try:
        subprocess.run(
            ["git", "add", "control.json"]
        )

        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                "update tunnel url"
            ]
        )

        subprocess.run(
            ["git", "push"]
        )

        print("Git push complete")

    except Exception as e:
        print("Git push error:", e)



def read_file():

    with open(FILE, "r") as f:
        return json.load(f)



def write_file(data):

    with open(FILE, "w") as f:
        json.dump(
            data,
            f,
            indent=4
        )



def start_cloudflared():

    global cloudflared_process

    print("Starting cloudflared...")


    cloudflared_process = subprocess.Popen(
        [
            "cloudflared",
            "tunnel",
            "--no-autoupdate",
            "--url",
            "http://localhost:8090"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )


    while True:

        line = cloudflared_process.stdout.readline()

        if line:

            print(line.strip())


            match = re.search(
                r"https://[a-zA-Z0-9-]+\.trycloudflare\.com",
                line
            )


            if match:

                return match.group(0)


        if cloudflared_process.poll() is not None:
            break


    return None




def main():

    global last_url

    print("Git Tunnel Agent Running")


    while True:

        try:

            # latest control.json lena
            git_pull()


            data = read_file()


            request = data.get("request")


            if request == "start":


                print("Start request received")


                url = start_cloudflared()


                if url:


                    data["request"] = "stop"
                    data["url"] = url


                    write_file(data)


                    last_url = url


                    git_push()


                    print(
                        "Tunnel URL:",
                        url
                    )


                else:

                    print(
                        "Tunnel failed"
                    )


            time.sleep(10)



        except Exception as e:

            print(
                "Error:",
                e
            )

            time.sleep(10)




if __name__ == "__main__":
    main()