import requests
from config import DOMAIN, PLTA, LOCATION_ID, EGG_ID, NEST_ID, DOCKER_IMAGE

HEADERS = {
    "Authorization": f"Bearer {PLTA}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def create_ptero_user(username, email, password):
    url = f"{DOMAIN}/api/application/users"
    payload = {
        "email": email,
        "username": username,
        "first_name": username,
        "last_name": "NodeJS",
        "password": password
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 201:
        return True, response.json()["attributes"]["id"]
    
    error_msg = response.json().get("errors", [{"detail": "Unknown error"}])[0]["detail"]
    return False, error_msg

def create_ptero_server(name, user_id, ram, disk, cpu):
    url = f"{DOMAIN}/api/application/servers"
    
    # Gunakan triple double-quotes (""") di awal dan akhir teks agar aman
    startup_cmd = """CPU_M=$(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2 | sed 's/^ *//'); CORE_C=$(nproc); RAM_K=$(grep MemTotal /proc/meminfo | awk '{print $2}'); RAM_M=$((RAM_K/1024)); OS_N=$(grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '\"'); ARCH_N=$(uname -m); KERN_V=$(uname -r); NODE_V=$(node -v); NPM_V=$(npm -v); TIME_D=$(date '+%Y-%m-%d %H:%M:%S'); TIME_Z=$(date +%Z); DISK_U=$(df -h /home/container | awk 'NR==2 {print $3 " / " $2 " ("$5" Used)"}'); UPTIME_S=$(awk '{print int($1/86400)"d "int(($1%86400)/3600)"h "int(($1%3600)/60)"m"}' /proc/uptime); INT_IP=$(hostname -I | awk '{print $1}'); LOAD_A=$(cat /proc/loadavg | awk '{print $1", "$2", "$3}'); USR_N=$(whoami); CONT_ID=$(hostname); echo -e "\033[1;36m ╔══════════════════════════════════════════════════════════╗"; echo -e "\033[1;36m ║              KELVIN HOSTING | PREMIUM SERVER             ║"; echo -e "\033[1;36m ╠══════════════════════════════════════════════════════════╝"; echo -e "\033[1;36m ║ \033[1;33m[ HARDWARE MONITOR ]\033[0m"; echo -e "\033[1;36m ║  \033[1;37m■ \033[1;32mCPU       :\033[0m ${CPU_M}"; echo -e "\033[1;36m ║  \033[1;37m■ \033[1;32mCORES     :\033[0m ${CORE_C} vCores"; echo -e "\033[1;36m ║  \033[1;37m■ \033[1;32mRAM       :\033[0m ${RAM_M} MB Total (Limit: ${SERVER_MEMORY} MB)"; echo -e "\033[1;36m ║  \033[1;37m■ \033[1;32mDISK      :\033[0m ${DISK_U}"; echo -e "\033[1;36m ║  \033[1;37m■ \033[1;32mLOAD      :\033[0m ${LOAD_A} (1m, 5m, 15m)"; echo -e "\033[1;36m ║"; echo -e "\033[1;36m ║ \033[1;33m[ SYSTEM & NETWORK ]\033[0m"; echo -e "\033[1;36m ║  \033[1;37m■ \033[1;32mOS        :\033[0m ${OS_N}"; echo -e "\033[1;36m ║  \033[1;37m■ \033[1;32mKERNEL    :\033[0m ${KERN_V}"; echo -e "\033[1;36m ║  \033[1;37m■ \033[1;32mARCH      :\033[0m ${ARCH_N}"; echo -e "\033[1;36m ║  \033[1;37m■ \033[1;32mUPTIME    :\033[0m ${UPTIME_S}"; echo -e "\033[1;36m ║  \033[1;37m■ \033[1;32mENDPOINT  :\033[0m tcp://${INT_IP}:${SERVER_PORT}"; echo -e "\033[1;36m ║  \033[1;37m■ \033[1;32mTIME      :\033[0m ${TIME_D} [${TIME_Z}]"; echo -e "\033[1;36m ║"; echo -e "\033[1;36m ║ \033[1;33m[ APP ENVIRONMENT ]\033[0m"; echo -e "\033[1;36m ║  \033[1;37m■ \033[1;32mNODEJS    :\033[0m ${NODE_V}"; echo -e "\033[1;36m ║  \033[1;37m■ \033[1;32mNPM       :\033[0m v${NPM_V}"; echo -e "\033[1;36m ║  \033[1;37m■ \033[1;32mUSER      :\033[0m ${USR_N}"; echo -e "\033[1;36m ║  \033[1;37m■ \033[1;32mDOCKER ID :\033[0m ${CONT_ID}"; echo -e "\033[1;36m ║  \033[1;37m■ \033[1;32mSERVER ID :\033[0m ${P_SERVER_UUID:0:8}"; echo -e "\033[1;36m ╚═══════════════════════════════════════════════════════════\033[0m"; echo -e "\033[1;32m [SYSTEM] \033[0mInitializing Core Kernel..."; echo -e "\033[1;32m [STATUS] \033[0mIndonesia Data Center: \033[1;32mONLINE\033[0m"; echo -e "\033[1;36m [READY]  \033[0mSystem initialized successfully.\n"; if [[ -d .git ]] && [[ {{AUTO_UPDATE}} == "1" ]]; then git pull; fi; if [[ ! -z ${NODE_PACKAGES} ]]; then /usr/local/bin/npm install ${NODE_PACKAGES}; fi; if [[ ! -z ${UNNODE_PACKAGES} ]]; then /usr/local/bin/npm uninstall ${UNNODE_PACKAGES}; fi; if [ -f /home/container/package.json ]; then /usr/local/bin/npm install; fi; if [[ ! -z ${CUSTOM_ENVIRONMENT_VARIABLES} ]]; then vars=$(echo ${CUSTOM_ENVIRONMENT_VARIABLES} | tr ";" "\n"); for line in $vars; do export $line; done; fi; /usr/local/bin/${CMD_RUN};"""
    
    payload = {
        "name": name,
        "user": user_id,
        "egg": EGG_ID,
        "docker_image": DOCKER_IMAGE,
        "startup": startup_cmd,
        "environment": {
            "MAIN_FILE": "index.js",
            "AUTO_UPDATE": "0",
            "USER_UPLOAD": "0",
            "CMD_RUN": "npm start"
        },
        "limits": {
            "memory": ram,
            "swap": 0, # Diset 0 untuk meminimalisir lag
            "disk": disk,
            "io": 500,
            "cpu": cpu
        },
        "feature_limits": {
            "databases": 1, 
            "backups": 1, 
            "allocations": 1
        },
        "deploy": {
            "locations": [LOCATION_ID],
            "dedicated_ip": False,
            "port_range": []
        }
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 201:
        return True, "Server berhasil dibuat."
    
    error_msg = response.json().get("errors", [{"detail": "Unknown error"}])[0]["detail"]
    return False, error_msg
