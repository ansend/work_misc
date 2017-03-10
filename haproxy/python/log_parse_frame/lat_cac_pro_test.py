import re
import sys
from pprint import pprint
from datetime import datetime

p = re.compile(r'.* nsms:([0-9]+) .*')

lat_stat = {}

#all interface stat the latency
if_list = ['copy', 'download', "upload_pro", "download_pro"]


def dump(obj):
    '''return a printable representation of an object for debugging'''
    newobj=obj
    if '__dict__' in dir(obj):
        newobj=obj.__dict__
        if ' object at ' in str(obj) and not newobj.has_key('__type__'):
            newobj['__type__']=str(obj)
        for attr in newobj:
            newobj[attr]=dump(newobj[attr])
    return newobj

def init_stat_store(ifs_list,stat_list):
    for m in range(len(ifs_list)):
        ifname = ifs_list[m]
        stat_list[ifname] = {}
        stat_list[ifname]['list'] = []
        stat_list[ifname]['total'] = 0
        stat_list[ifname]['max'] = 0

def sort_stat_store(ifs_list,stat_list):
    for m in range(len(ifs_list)):
        ifname = ifs_list[m]
        stat_list[ifname]['list'].sort()

def parse_general(line, ifname):
    total = lat_stat[ifname]['total']
    m_list = lat_stat[ifname]['list']
    m_max = lat_stat[ifname]['max']

    p_nsms = re.compile(r'.* nsms:([0-9]+) .*')  
    p_ot = re.compile(r'.*\smetrics=([0-9]+)\..*')
    r_nsms = p_nsms.match(line)
    if r_nsms:
        lat_stat[ifname]['total'] += 1
        i = int(r_nsms.group(1))
        m_list.append(i)  
        return True

    r_ot = p_ot.match(line)
    if r_ot:
        lat_stat[ifname]['total'] += 1
        i = int(r_ot.group(1))     
        m_list.append(i)                                                        
        return True

    return False


def parse_upload(line, ifname):
    total = lat_stat[ifname]['total']
    m_list = lat_stat[ifname]['list']
    m_max = lat_stat[ifname]['max']

    p_nsms = re.compile(r'.* nsms:([0-9]+) .*')  
    p_ot = re.compile(r'.*\smetrics=([0-9]+)\..*')
    r_nsms = p_nsms.match(line)
    if r_nsms:
        lat_stat[ifname]['total'] += 1
        i = int(r_nsms.group(1))
        m_list.append(i)  
        return True

    r_ot = p_ot.match(line)
    if r_ot:
        lat_stat[ifname]['total'] += 1
        i = int(r_ot.group(1))     
        m_list.append(i)                                                        
        return True

    return False

def parse_upload_pro(line, ifname): 
    total = lat_stat[ifname]['total'] 
    m_list = lat_stat[ifname]['list']
    m_max = lat_stat[ifname]['max']    
                                                                                
    p_nsms = re.compile(r'.* nsms:([0-9]+) .*')                                 
    p_ot = re.compile(r'.*\smetrics=([0-9]+)\..*')                              
    r_nsms = p_nsms.match(line)                                                 
    if r_nsms:                                                                  
        lat_stat[ifname]['total'] += 1                                        
        i = int(r_nsms.group(1))                                                
        m_list.append(i)                                                        
        return True                                                             
                                                                                
    r_ot = p_ot.match(line)                                                     
    if r_ot:                                                                    
        lat_stat[ifname]['total'] += 1                                        
        i = int(r_ot.group(1))                                                  
        m_list.append(i)                                                        
        return True                                                             
                                                                                
    return False  

def parse_download():
    print "pasrse download"
    return 0

def parse_download_pro(line, ifname):                                                         
    total = lat_stat[ifname]['total']                                         
    m_list = lat_stat[ifname]['list']                                         
    m_max = lat_stat[ifname]['max']                                           
                                                                                
    p_nsms = re.compile(r'.* nsms:([0-9]+) .*')                                 
    p_ot = re.compile(r'.*\smetrics=([0-9]+)\..*')                              
    r_nsms = p_nsms.match(line)                                                 
    if r_nsms:                                                                  
        lat_stat[ifname]['total'] += 1                                        
        i = int(r_nsms.group(1))                                                
        m_list.append(i)                                                        
        return True                                                             
    r_ot = p_ot.match(line)                                                     
    if r_ot:                                                                    
        lat_stat[ifname]['total'] += 1                                        
        i = int(r_ot.group(1))                                                  
        m_list.append(i)                                                        
        return True                                                             
                                                                                
    return False

def parse_place_copy():

    return 0


handle_list = [#{'if':'upload','url':'.*videos_snapshot_upload_once_complete3.*','handle':parse_upload},
               {'if':'upload_pro','url':'.*videos_.*upload_once_complete3.*','handle':parse_upload_pro},
               {'if':'download_pro','url':'.*locationwithsort.*','handle':parse_download_pro},   
               {'if':'copy','url':'.*videos_add_copy2.*','handle':parse_general},
              ]

def avrge(inx, lat_list):
    sumlat = 0
    for i in range(0, inx):
        sumlat = sumlat + lat_list[i]
    return int(sumlat/inx)

def showstat(per,lat_list):
    lat_total = len(lat_list)
    inx=int(lat_total*per)
    print"percentile",per*100,  "  max:",\
    lat_list[inx], "  average:",avrge(inx,lat_list)

def show_lat_stat(lat_list):
    lat_total = len(lat_list)
    c_10 = 0
    c_20 = 0
    c_50 = 0
    c_100= 0
    c_200= 0
    c_other = 0

    for i in range(0, lat_total):
        if lat_list[i] <= 10:
            c_10 += 1
        elif lat_list[i] <= 20:
            c_20 += 1
        elif lat_list[i] <= 50:
            c_50 += 1
        elif lat_list[i] <= 100:
            c_100 += 1
        elif lat_list[i] <= 200:
            c_200 += 1
        else:
            c_other += 1
    
    print "\n"
    print "percentage according to latency in ms"
    print ("0  -- 10 : %.2f"%(float(c_10)*100/float(lat_total)))
    print ("10 -- 20 : %.2f"%(float(c_20)*100/float(lat_total)))
    print ("20 -- 50 : %.2f"%(float(c_50)*100/float(lat_total)))
    print ("50 -- 100: %.2f"%(float(c_100)*100/float(lat_total)))
    print ("100-- 200: %.2f"%(float(c_200)*100/float(lat_total)))
    print ("200-- ~  : %.2f"%(float(c_other)*100/float(lat_total)))

def show_lat_percent(lat_list):
    
    per_list = [0.5, 0.9, 0.99, 0.999, 0.9999]
    for i in range(0, len(per_list)):
        showstat(per_list[i], lat_list)

def show_all_lat_stat(ifs_list,stat_list):
    for m in range(len(ifs_list)):        
        ifname = ifs_list[m]  
        total = stat_list[ifname]['total']
        lat_list = stat_list[ifname]['list'] 
        if total > 0 :
            print ("***************latency stat for %s************"%(ifname))
            print "total:", total 
            print "min:", lat_list[0]                   
            print "max:", lat_list[total-1]            
            print "\n" 
            show_lat_percent(lat_list)
            show_lat_stat(lat_list)
            print ("****************************************************")


def main():
    start = datetime(2016, 12, 13, 12, 00)
    end = datetime.now()
    
    pprint(dump(handle_list)) 
    init_stat_store(if_list,lat_stat)
    
    for line in sys.stdin:
        #print line
        #if not line.startswith('2016'):
        #    continue
        #make sure a it can parse a date time object.
        pt = re.compile(r'.*(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s')
        res = pt.match(line)
        if not res:
            print "can not get the time info"
            print line
            continue
        t = datetime.strptime(res.group(1), "%Y-%m-%d %H:%M:%S")
        if (t is None) or ( t < start):
            print "time is less than the expected time", t 
            continue
        else:
            pass
    
        for hinx in range(0, len(handle_list)):
            pat= re.compile(handle_list[hinx]['url'])
            #print handle_list[hinx]['url']
            #pat= re.compile('.*videos_upload_once_complete3.*')
            ifname = handle_list[hinx]['if']
            pat_res=pat.match(line)
            #print hinx
            if pat_res:
                #print hinx
                #print handle_list[hinx]['url']
                handle_list[hinx]['handle'](line, ifname)
                #handle = parse_upload
                #handle()
                break
    sort_stat_store(if_list,lat_stat)

    print "TimeLine:", start , "----", end , "\n"
    show_all_lat_stat(if_list,lat_stat)


if __name__ == "__main__":
    main()
