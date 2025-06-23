"""
此文件包含ETS2LA的运行程序。
如果你正在寻找实际的入口点，
请查看ETS2LA文件夹中的core.py文件。
"""

import os
import sys
import subprocess

# 这个try/except块将以成功导入、更新或错误结束
try: from ETS2LA.Utils.translator import Translate, UpdateFrontendTranslations
except: # 确保当前PATH包含安装目录
    sys.path.append(os.path.dirname(__file__))
    try: # 这里应该可以工作
        from ETS2LA.Utils.translator import Translate, UpdateFrontendTranslations
    except ModuleNotFoundError: # 如果缺少模块，这将触发（通常是tqdm）
        print("ETS2LA/Utils/translator.py中的导入错误，这通常是缺少模块的迹象。将触发更新以安装这些模块。")
        subprocess.run("update.bat", shell=True, env=os.environ.copy())
        from ETS2LA.Utils.translator import Translate, UpdateFrontendTranslations
    except Exception as e: # 未知错误
        try: # 尝试获取回溯信息以便于调试
            import traceback
            print(traceback.format_exc())
        except: # 如果失败，只打印异常信息
            print(str(e))
        input("按回车键退出...")
        sys.exit()

# 允许pygame在后台获取控制事件
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
# 隐藏pygame的支持提示
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    
from ETS2LA.Utils.Console.logs import CountErrorsAndWarnings, ClearLogFiles
from ETS2LA.Utils.submodules import EnsureSubmoduleExists
from ETS2LA.Utils.shell import ExecuteCommand
from ETS2LA.Utils.Console.colors import *
import ETS2LA.Networking.cloud as cloud

import multiprocessing
import traceback
import importlib
import requests
import queue
import time
import git

LOG_FILE_FOLDER = "logs"
FRONTEND_MIRRORS = [
    "https://app.ets2la.com",
    "https://app.ets2la.cn",
]

def close_node() -> None:
    if os.name == "nt":
        ExecuteCommand("taskkill /F /IM node.exe > nul 2>&1")
    else:
        ExecuteCommand("pkill -f node > /dev/null 2>&1")

def reset(clear_logs=True) -> None:
    close_node()
    CountErrorsAndWarnings()
    if clear_logs:
        ClearLogFiles()
        
def get_commit_url(repo: git.Repo, commit_hash: str) -> str:
    try:
        remote_url = repo.remotes.origin.url
        remote_url = remote_url.replace('.git', '')
        
        return remote_url + "/commit/" + commit_hash
    except:
        return ""
        
def get_current_version_information() -> dict:
    try:
        repo = git.Repo()
        current_hash = repo.head.object.hexsha
        current_branch = repo.active_branch.name
        return {
            "name": current_branch,
            "link": get_commit_url(repo, current_hash),
            "time": time.ctime(repo.head.object.committed_date)
        }
    except:
        return {
            "name": "Unknown",
            "link": "Unknown",
            "time": "Unknown"
        }

def get_fastest_mirror() -> str:
    print(f"Testing mirrors...")
    response_times = {}
    for mirror in FRONTEND_MIRRORS:
        try:
            start = time.perf_counter()
            requests.get(mirror, timeout=5)
            end = time.perf_counter()
            response_times[mirror] = end - start
            print(f"- Reached {YELLOW}{mirror}{END} in {response_times[mirror] * 1000:.0f}ms")
        except requests.RequestException:
            response_times[mirror] = float('inf')
            print(f" - Reached {YELLOW}{mirror}{END} in (TIMEOUT)")
        
    fastest_mirror = min(response_times, key=response_times.get)
    return fastest_mirror

def update_frontend() -> bool:
    did_update = EnsureSubmoduleExists(
        "Interface", 
        "https://github.com/ETS2LA/frontend.git", 
        download_updates=False if "--dev" in sys.argv else True,
        cdn_url="http://cdn.ets2la.com/frontend", 
        cdn_path="frontend-main"
    )
    
    if did_update:
        print(f"{GREEN} -- Running post download action for submodule: {YELLOW} Interface {GREEN} -- {END}")
        UpdateFrontendTranslations()
        ExecuteCommand("cd Interface && npm install && npm run build-local")
    
    return did_update

def ets2la_process(exception_queue: multiprocessing.Queue) -> None:
    """
    主要的ETS2LA进程。
    - 此函数将使用给定的参数运行ETS2LA。
    - 它还将处理异常和子模块的更新。
    
    `exception_queue`用于将异常发送回主进程
    以便处理（在此文件底部）。
    """
    try:
        import ETS2LA.variables
        
        if "--dev" in sys.argv:
            print(f"{PURPLE}{Translate('main.development_mode')}{END}\n")
        
        if "--local" in sys.argv:
            update_frontend()
            print(f"{PURPLE}{'本地运行UI'}{END}\n")
        
        elif "--frontend-url" not in sys.argv:
            url = get_fastest_mirror()
            if not url:
                print(f"{RED}{'无法连接到远程UI镜像。本地运行。'}{END}\n")
                update_frontend()
                    
                if not "--local" in sys.argv:
                    sys.argv.append("--local")
                ETS2LA.variables.LOCAL_MODE = True
                
            elif ".cn" in url:
                if not "--china" in sys.argv:
                    sys.argv.append("--china")
                ETS2LA.variables.CHINA_MODE = True
                print(f"{PURPLE}{'以中国模式运行UI'}{END}\n")
                
            print(f"\n> 使用镜像 {YELLOW}{url}{END} 运行UI。\n")
            sys.argv.append("--frontend-url")
            sys.argv.append(url)
        
        if "--no-console" in sys.argv:
            if "--no-ui" in sys.argv:
                print(f"{RED}{'--no-console不能与--no-ui一起使用。控制台将不会关闭。'}{END}\n")
            else:
                print(f"{PURPLE}{'UI启动后关闭控制台。'}{END}\n")
            
        if "--no-ui" in sys.argv:
            print(f"{PURPLE}{'不使用UI运行。'}{END}\n")
        
        close_node()
        ClearLogFiles()
        ETS2LA = importlib.import_module("ETS2LA.core")
        ETS2LA.run()
        
    except Exception as e:
        # 分别捕获退出和重启
        if str(e) != "exit" and str(e) != "restart":
            trace = traceback.format_exc()
            exception_queue.put((e, trace))
        else:
            exception_queue.put((e, None))


if __name__ == "__main__":
    exception_queue = multiprocessing.Queue()
    print(f"{BLUE}{Translate('main.overseer_started')}{END}\n")
    
    while True:
        process = multiprocessing.Process(target=ets2la_process, args=(exception_queue,))
        process.start()
        process.join() # 这将阻塞直到ETS2LA关闭。
        
        try:
            e, trace = exception_queue.get_nowait()

            if e.args[0] == "exit":
                reset(clear_logs=False)
                sys.exit(0)

            if e.args[0] == "restart":
                reset()
                print(YELLOW + Translate("main.restarting") + END)
                continue
            
            if e.args[0] == "Update":
                # 检查是否使用--dev标志运行，以防止意外覆盖更改
                if "--dev" in sys.argv:
                    print(YELLOW + "由于开发模式跳过更新。" + END)
                    continue
                
                print(YELLOW + Translate("main.updating") + END)
                ExecuteCommand("update.bat")
                
                print("\n" + GREEN + Translate("main.update_done") + END + "\n")
                reset()
                continue
            
            # 此时我们确定这是一个崩溃
            print(Translate("main.crashed"))
            print(trace)
            
            # 崩溃报告目前不起作用，已禁用以节省带宽
            '''
            try: cloud.SendCrashReport("ETS2LA 2.0 - Main", trace, additional=get_current_version_information)
            except: pass
            '''
            
            print(Translate("main.send_report"))
            reset()
            print(RED + Translate("main.closed") + END)
            input(Translate("main.press_enter"))
            sys.exit(0)
        
        except queue.Empty:
            pass
        
# 忽略：此注释仅用于触发更新并清除
#       应用程序缓存，用于不一定在此存储库内
#       发生的更改（如前端）。
# 
# 计数器: 18