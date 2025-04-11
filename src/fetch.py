import psutil, platform, socket, uuid, subprocess
import json, time, os, re, getpass, wmi
from colorist import BgColorRGB

#region VEDRETCH
json_path = os.path.join(os.path.dirname(__file__), '..', 'json', 'logo.json') #read json file
with open(json_path, "r") as fileJ:
    settings = json.load(fileJ)

uptime = time.strftime("%H:%M:%S")

#work with WMI (like info about CPU, GPU Motherboard)
UUID = wmi.WMI().Win32_ComputerSystemProduct()[0].UUID
INFO = wmi.WMI()

CPU = INFO.Win32_Processor()[0]
GPU = INFO.Win32_VideoController()[0]
MOTHERBOARD = INFO.Win32_BaseBoard()[0]

#ASCII colors
class foreground:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    CYAN = "\033[0;36m"
    YELLOW = "\033[1;33m"
    RESET = "\033[39m"
fg = foreground()

#translate CYAN color into a variable
ON_COLOR = fg.CYAN
OFF_COLOR = fg.RESET

#background colors for last
class Background:
    GREEN = BgColorRGB(0, 255, 0)
    GREEN1 = BgColorRGB(0, 128, 43)

    RED = BgColorRGB(255, 0, 0)
    RED1 = BgColorRGB(128, 0, 0)

    ORANGE = BgColorRGB(255, 153, 51)
    ORANGE1 = BgColorRGB(128, 64, 0)

    YELLOW = BgColorRGB(255, 255, 0)
    YELLOW1 = BgColorRGB(128, 128, 0)

    BROWN = BgColorRGB(191, 128, 64)
    BROWN1 = BgColorRGB(96, 64, 32)

    CYAN = BgColorRGB(0, 255, 255)
    CYAN1 = BgColorRGB(0, 128, 128)

    BLUE = BgColorRGB(0, 0, 255)
    BLUE1 = BgColorRGB(0, 0, 128)

    PINK = BgColorRGB(255, 77, 106)
    PINK1 = BgColorRGB(153, 0, 26)

    PURPLE = BgColorRGB(230, 0, 230)
    PURPLE1 = BgColorRGB(128, 0, 128)
bg = Background()

#rainbow cubes output
bright_background = f"{str(' '):<5}{bg.GREEN}   {bg.GREEN.OFF}{bg.RED}   {bg.RED.OFF}{bg.ORANGE}   {bg.ORANGE.OFF}{bg.YELLOW}   {bg.YELLOW.OFF}{bg.CYAN}   {bg.CYAN.OFF}{bg.BLUE}   {bg.BLUE.OFF}{bg.PINK}   {bg.PINK.OFF}{bg.PURPLE}   {bg.PURPLE.OFF}{bg.BROWN}   {bg.BROWN.OFF}"
dark_background = f"{str(' '):<5}{bg.GREEN1}   {bg.GREEN1.OFF}{bg.RED1}   {bg.RED1.OFF}{bg.ORANGE1}   {bg.ORANGE1.OFF}{bg.YELLOW1}   {bg.YELLOW1.OFF}{bg.CYAN1}   {bg.CYAN1.OFF}{bg.BLUE1}   {bg.BLUE1.OFF}{bg.PINK1}   {bg.PINK1.OFF}{bg.PURPLE1}   {bg.PURPLE1.OFF}{bg.BROWN1}   {bg.BROWN1.OFF}"


partitions = psutil.disk_partitions()
DiskС = partitions[0] #information about disk C
usageInC = psutil.disk_usage(DiskС.mountpoint)

def check_precent_of_diskC():
    if usageInC.percent<45:
        return f"{usageInC.used / (1024 ** 3):.2f} / {usageInC.total / (1024 ** 3):.2f} GB ({fg.GREEN}{usageInC.percent}{fg.RESET}%)"
    elif usageInC.percent<65:
        return f"{usageInC.used / (1024 ** 3):.2f} / {usageInC.total / (1024 ** 3):.2f} GB ({fg.YELLOW}{usageInC.percent}{fg.RESET}%)"
    elif usageInC.percent<=100:
        return f"{usageInC.used / (1024 ** 3):.2f} / {usageInC.total / (1024 ** 3):.2f} GB ({fg.RED}{usageInC.percent}{fg.RESET}%)"


def pc_myNames():
    pc_name = subprocess.getoutput("hostname")
    return pc_name

def what_the_sigma_windows():
    systm, rlse = platform.system(), platform.release()
    return "{0} {1}".format(systm, rlse)

def os_system():
    win_vers = platform.version()
    return win_vers

def my_host():
    host_name = socket.gethostname()
    return host_name

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 10000))
        get_ip = s.getsockname()[0]
        return get_ip
    
    except Exception:
        return "..."
    
def MAC_ip():
    mac_ip = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    return mac_ip

def battery_info():
    battery = psutil.sensors_battery()

    battery = psutil.sensors_battery()
    if not battery:
        return "  Battery information not available."

    status = "charging" if battery.power_plugged else "not charging" #подключена ли зарядка, или нет
    color = fg.GREEN if battery.percent >= 50 else fg.YELLOW
    return f"  Battery{OFF_COLOR}: {battery.percent}% ({color}{status}{OFF_COLOR})"
        
def RAM_info():
    memory_prc = psutil.virtual_memory()
    used = f"{memory_prc.used / (1024.0 ** 3):.2f} GB"
    total = f"{memory_prc.total / (1024.0 ** 3):.2f} GB"
    percent = memory_prc.percent

    if percent <= 50:
        color = fg.GREEN
    elif percent <= 75:
        color = fg.YELLOW
    else:
        color = fg.RED

    return f"{ON_COLOR}RAM{OFF_COLOR}: {used} / {total} ({color}{percent}{OFF_COLOR}%)"

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    PCname = pc_myNames() 
    dict_information_output = {
            f"{ON_COLOR}{settings['logo'][0]}{OFF_COLOR}": f"{getpass.getuser()}{ON_COLOR}@{OFF_COLOR}{PCname}",
            f"{ON_COLOR}{settings['logo'][1]}{OFF_COLOR}": f"╭{str():╶<30}╮",
            f"{ON_COLOR}{settings['logo'][2]}": f" OS{OFF_COLOR}: {what_the_sigma_windows()}",
            f"{ON_COLOR}{settings['logo'][3]}": f" OS version{OFF_COLOR}: {os_system()}",
            f"{ON_COLOR}{settings['logo'][4]}": f" Host name{OFF_COLOR}: {my_host()}",
            f"{ON_COLOR}{settings['logo'][5]}{OFF_COLOR}": f" ╰{str():╶<30}╯", 
            f"{ON_COLOR}{settings['logo'][6]}{OFF_COLOR}": f"╭{str():╶<33}╮",
            f"{ON_COLOR}{settings['logo'][7]}": f" Local IP{OFF_COLOR}: {get_local_ip()}",
            f"{ON_COLOR}{settings['logo'][8]}": f" MAC-address{OFF_COLOR}: {MAC_ip()}",
            f"{ON_COLOR}{settings['logo'][9]}": f"  Uptime{OFF_COLOR}: {uptime}",
            f"{ON_COLOR}{settings['logo'][10]}{OFF_COLOR}": f"╰{str():╶<33}╯",
            f"{ON_COLOR}{settings['logo'][11]}{OFF_COLOR}": f"╭{str():╶<43}╮",
            f"{ON_COLOR}{settings['logo'][12]}": f" CPU{OFF_COLOR}: {CPU.Name}",
            f"{ON_COLOR}{settings['logo'][13]}": f" GPU{OFF_COLOR}: {GPU.Caption}",
            f"{ON_COLOR}{settings['logo'][14]}": f" Motherboard{OFF_COLOR}: {MOTHERBOARD.Caption}",
            f"{ON_COLOR}{settings['logo'][15]}": f"  UUID{OFF_COLOR}: {UUID}",
            f"{ON_COLOR}{settings['logo'][16]}": battery_info(),
            f"{ON_COLOR}{settings['logo'][17]}{OFF_COLOR}": f"╰{str():╶<43}╯",
            f"{ON_COLOR}{settings['logo'][18]}{OFF_COLOR}": f"╭{str():╶<44}╮",
            f"{str(' '):<47} {ON_COLOR}Disk{OFF_COLOR}:": DiskС.device,
            f"{bright_background} {str(' '):<17}{ON_COLOR}Memory{OFF_COLOR}:": check_precent_of_diskC(),
            f"{dark_background}{ON_COLOR} {str(' '):<17}Memory free{OFF_COLOR}:": f"{usageInC.free / (1024 ** 3):.2f} GB",
            f"{str(' '):<46}": RAM_info(),
            f"{str(' '):<44}": f"╰{str():╶<44}╯"
        }

    for key,value in dict_information_output.items():
        print("{0}  {1}".format(key,value))

if __name__ == "__main__":
    main()