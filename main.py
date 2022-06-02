from src.modules.mobile.mobile import Test
from src.modules.api.my_api import run
from threading import Thread

if __name__ == "__main__":
    try:
        Thread(target=run).start()
        Thread(target=Test().run()).start()
    except KeyboardInterrupt:
        exit()
