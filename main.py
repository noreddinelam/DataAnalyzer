from src.modules.mobile.mobile import Test
from src.modules.api.my_api import run_api_server
from threading import Thread

if __name__ == "__main__":
    try:
        Thread(target=run_api_server).start()
        Thread(target=Test().run()).start()
    except KeyboardInterrupt:
        exit()
