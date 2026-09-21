# scheduler.py
import schedule
import time
from digest import main

# 【测试模式】先每分钟跑一次，验证机制生效
# schedule.every(1).minutes.do(main)

# 【正式模式】测好后注释掉上面，改用这行：
schedule.every().day.at("08:00").do(main)

print("定时器已启动，等待触发...（Ctrl+C 退出）")
while True:
    schedule.run_pending()
    time.sleep(30)
