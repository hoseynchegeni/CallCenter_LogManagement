from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import sqlite3
from datetime import datetime
import time
a = 0



#--------sqlite connection---------
con = sqlite3.connect('b2c_wall(5).sqlite3')
con.cursor()
cur= con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS  avg_minute(all_agents text ,Input_agent text,Talking text,Idle text,Pause text,Output_agent text,All_calls text,Waitings text,Holdtime text,time text)')
cur.execute('CREATE TABLE IF NOT EXISTS  avg_quarter(all_agents text ,Input_agent text,Talking text,Idle text,Pause text,Output_agent text,All_calls text,Waitings text,Holdtime text,Start text,End text)')
cur.execute('CREATE TABLE IF NOT EXISTS  avg_hour(all_agents text ,Input_agent text,Talking text,Idle text,Pause text,Output_agent text,All_calls text,Waitings text,Holdtime text,Start text,End text)')

#---------selenium driver----------
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://q1-panel.asiatech.ir/admin/SystemStatus/wall/")
username = driver.find_element_by_id("UserUsername")
username.send_keys("********")#Enter username
password = driver.find_element_by_id("UserP")
password.send_keys("@********")#Enter Password
password.send_keys(Keys.ENTER)


#----------Processing  data----------
talking_minute = [] 
idle_minute = []
inputing_agents_minute = []
output_agents_minutes = []
all_agents_minutes = []
wating_minutes =[]
all_calls_minutes = []
holdtime_sec = []
holdtime_min = []
pause_minute = []

#----------------------
talkin_quarter =[]
idle_quarter = []
inputing_agents_quarter =[]
output_agents_quarter = []
all_agents_quarter =[]
wating_quarter = []
all_calls_quarter = []
holdtime_min_quarter = []
holdtime_sec_quarter = []
pause_quarter = []




while True:
    a +=1
    print(a)
    wall = driver.find_elements_by_class_name("tablesorter")


    search_list =[]
    idle = []
    talking = []
    pausee = []
    outputing_agents = []  
    inputing_agents = []
    all_agents = []
    waiting = []
    holdtime = []
    pause = []
    b2c =[]
    b2c_q = []
    b2c_h = []
    timing_withiut_second = 0



    #-----------------Data extraction with regax
    for i in wall:
      search_list.append(i.text)
    for i in search_list:
      resualt = re.findall(r'Idle .(\d+)',i)
      if resualt:
          idle.append(int(resualt[0]))
    for i in search_list:
      resualt = re.findall(r'Talking .(\d+)',i)
      if resualt:
        talking.append(int(resualt[0]))
    for i in search_list:
        resualt =re.findall(r'\d+:\d+:\d+ (\d+)',i)
        if resualt:
          inputing_agents.append(int(resualt[0]))
          outputing_agents.append(int(resualt[1]))
          all_agents.append(int(resualt[2]))
    for i in search_list:
        resualt = re.findall(r'B2C (\d+) \d+:\d+:\d+',i)
        if resualt:
          waiting.append(int(resualt[0]))
    for i in search_list:
       resualt = re.findall(r'B2C \d+ (\d+:\d+:\d+)',i)
       if resualt:
         holdtime.append(resualt[0])
    for i in search_list:
      resualt = re.findall(r'B2C \d+ \d+:\d+:\d+ \d+ (\d+)',i)
      if resualt:
        pause.append(int(resualt[0]))
        print('waitings:',waiting[0])
        print('talking:',talking[0])
    all_calls = waiting[0]+talking[0]


    #------------- Calculate time  --------
    timing = datetime.now().time()
    timing_withiut_second = timing.strftime("%H:%M")
    if len(idle_minute) == 0 :
      start_q = timing_withiut_second
    if len(idle_minute)==0 and len(idle_quarter) == 0:
      start_h = timing_withiut_second


    #---------Insert the extracted data   list for insert to db-------------
    b2c.append(all_agents[0])
    b2c.append(inputing_agents[0])
    b2c.append(talking[0])
    b2c.append(idle[0])
    b2c.append(pause[0])
    b2c.append(outputing_agents[0])
    b2c.append(all_calls)
    b2c.append(waiting[0])
    b2c.append(holdtime[0])
    b2c.append(timing_withiut_second)
    

    #-----------To calculate the average--------------
    idle_minute.append(idle[0])
    talking_minute.append(talking[0])
    inputing_agents_minute.append(inputing_agents[0])
    output_agents_minutes.append(outputing_agents[0])
    all_agents_minutes.append(all_agents[0])
    wating_minutes.append(waiting[0])
    all_calls_minutes.append(all_calls) 
    pause_minute.append(pause[0])
    #---------------Dedicate seconds from holdtime to calculate the average------------
    hold= re.findall(r'\d+:\d+:(\d+)',holdtime[0])
    holdtime_sec.append(int(hold[0]))

    hold = re.findall(r'\d+:(\d+):\d+',holdtime[0])
    holdtime_min.append(int(hold[0]))    


    print(b2c)
    cur.execute('insert into avg_minute(all_agents,Input_agent,Talking,Idle,Pause,Output_agent,All_calls,Waitings,Holdtime,time) values (?,?,?,?,?,?,?,?,?,?)',b2c)
    con.commit()


    #-----------------calculate the average of quarter (15min) and insert to db-----------
    if len(idle_minute) == 15 and len(talking_minute)==15:
      avg_idle_quarter =round(sum(idle_minute)/len(idle_minute))
      avg_talking_quarter = round(sum(talking_minute)/len(talking_minute))
      avg_inputing_agents_quarter = round(sum(inputing_agents_minute)/len(inputing_agents_minute))
      avg_output_agents_quarter = round(sum(output_agents_minutes)/len(output_agents_minutes))
      avg_all_agents_quarter = round(sum(all_agents_minutes)/len(all_agents_minutes))
      avg_waiting_quarter = round(sum(wating_minutes)/len(wating_minutes))
      avg_all_calls_quarter = round(sum(all_calls_minutes)/len(all_calls_minutes))
      avg_pause_quarter = round(sum(pause_minute)/len(pause_minute))
      avg_holdtime_sec = round(sum(holdtime_sec)/len(holdtime_sec))
      avg_holdtime_min = round(sum(holdtime_min)/len(holdtime_min))



      idle_quarter.append(avg_idle_quarter)
      talkin_quarter.append(avg_talking_quarter)
      inputing_agents_quarter.append(avg_inputing_agents_quarter)
      output_agents_quarter.append(avg_output_agents_quarter)
      all_agents_quarter.append(avg_all_agents_quarter)
      wating_quarter.append(avg_waiting_quarter)
      all_calls_quarter.append(avg_all_calls_quarter)
      holdtime_min_quarter.append(avg_holdtime_min)
      holdtime_sec_quarter.append(avg_holdtime_sec)
      pause_quarter.append(avg_pause_quarter)



      idle_minute.clear()
      talking_minute.clear()
      inputing_agents_minute.clear()
      output_agents_minutes.clear()
      all_agents_minutes.clear()
      wating_minutes.clear()
      all_calls_minutes.clear()
      holdtime_sec.clear()
      holdtime_min.clear()
      pause_minute.clear()

      

      b2c_q.append(avg_all_agents_quarter)
      b2c_q.append(avg_inputing_agents_quarter)
      b2c_q.append(avg_talking_quarter)
      b2c_q.append(avg_idle_quarter)
      b2c_q.append(avg_pause_quarter)
      b2c_q.append(avg_output_agents_quarter)
      b2c_q.append(avg_all_calls_quarter)
      b2c_q.append(avg_waiting_quarter)
      minute = (f"{str(avg_holdtime_min)}:{str(avg_holdtime_sec)}")
      b2c_q.append(minute)     
      b2c_q.append(start_q)
      b2c_q.append(timing_withiut_second)

      
    


      cur.execute('insert into avg_quarter(all_agents,Input_agent,Talking,Idle,Pause,Output_agent,All_calls,Waitings,Holdtime,Start,End) values (?,?,?,?,?,?,?,?,?,?,?)',b2c_q)
      con.commit()


      #------------- calculate the average of one hour and  insert to db
      if len(talkin_quarter) == 4 and len(idle_quarter) == 4:
        avg_idle_hour =round( sum(idle_quarter)/len(idle_quarter))
        avg_talking_hour = round(sum(talkin_quarter)/len(talkin_quarter))
        avg_inputing_agents_hour = round(sum(inputing_agents_quarter)/len(inputing_agents_quarter))
        avg_output_agents_hour =round(sum(output_agents_quarter)/len(output_agents_quarter))
        avg_all_agents_hour = round(sum(all_agents_quarter)/len(all_agents_quarter))
        avg_waiting_hour = round(sum(wating_quarter)/len(wating_quarter))
        avg_all_calls_hour = round(sum(all_calls_quarter)/len(all_calls_quarter))
        avg_pause_hour = round(sum(pause_quarter)/len(pause_quarter))
        holdtime_sec_for_avg_hour = round(sum(holdtime_sec_quarter)/len(holdtime_sec_quarter))
        holdtime_min_for_avg_hour = round(sum(holdtime_min_quarter)/len(holdtime_min_quarter))
        avg_pause_hour = round(sum(pause_quarter)/len(pause_quarter))




        b2c_h.append(avg_all_agents_hour)
        b2c_h.append(avg_inputing_agents_hour)
        b2c_h.append(avg_talking_hour)
        b2c_h.append(avg_idle_hour)
        b2c_h.append(avg_pause_hour)
        b2c_h.append(avg_output_agents_hour)
        b2c_h.append(avg_all_calls_hour)
        b2c_h.append(avg_waiting_hour)
        hour = (f"{str(holdtime_min_for_avg_hour)}:{str(holdtime_sec_for_avg_hour)}")
        b2c_h.append(hour)
        b2c_h.append(start_h)
        b2c_h.append(timing_withiut_second)

        
        


        idle_quarter.clear()
        talkin_quarter.clear()
        inputing_agents_quarter.clear()
        output_agents_quarter.clear()
        all_agents_quarter.clear()
        wating_quarter.clear()
        all_calls_quarter.clear()
        holdtime_sec_quarter.clear()
        holdtime_min_quarter.clear()
        pause_quarter.clear()
        


        cur.execute('insert into avg_hour (all_agents,Input_agent,Talking,Idle,Pause,Output_agent,All_calls,Waitings,Holdtime,Start,End) values (?,?,?,?,?,?,?,?,?,?,?)',b2c_h)
        con.commit()
    print(timing_withiut_second)
    time.sleep(59)
    driver.refresh()