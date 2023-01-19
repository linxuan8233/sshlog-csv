from collections import Counter
import geoip2.database
import geoip2.errors
import datetime,sys
def searchByIPASNStr(ip):
    with geoip2.database.Reader("GeoLite2-ASN.mmdb") as reader:
        return reader.asn(ip)
def searchByIPCounterStr(ip):
    with geoip2.database.Reader("GeoLite2-Country.mmdb") as reader:
        return reader.country(ip)
def tiqvsshd(text:str):
    data_list=[]
    for i in text.split('\n'):
        if "sshd" in i:
            data_list.append(i+"\n")
        if "Accepted publickey" in i:
            ...
        else:
            pass
    return data_list
def splitstr(text:str):
    data_list=[]
    for i in text.split("\n"):
        data_list.append(' '.join(i.split(" ")[0:3:])+" "+i.split(" ",4)[::-1][0]+"\n")
    return data_list
def jxfeng(text:str):
    data_list=[]
    for i in text.split("\n"):
        data_list.append("".join(i.split("]: ")[0].split("sshd[")[0])+" "+i.split("]: ")[::-1][0]+"\n")
    return data_list
def tiqvyhm(text):
    data={}
    ip=text.split("port")[0].split(" ")[::-1][1].strip()

    data["ip"]=f"{ip}",f"{searchByIPCounterStr(ip).country.names.get('zh-CN',None)}",f"{searchByIPASNStr(ip).autonomous_system_organization}"
    if "user" in text:
        data["username"]=text.split("user")[1].split(" ")[1::][0].strip()
    else:
        data["username"]="其他原因"

    return data
def sformattime(time):
    x = datetime.datetime.strptime(time,"%b %d %H:%M:%S")
    return x.strftime("%m月/%d日 %H:%M:%S")
def jxfb(dat,dic):
    try:
        d=tiqvyhm(dat)
    except Exception:
        d=""
    if d != "":
        if d["username"] in dic:
            dic.update({d["username"]:dic[d["username"]]+[d["ip"]]})
        else:
            dic.update({d["username"]:[d["ip"]]})
def jx(text):
    data1={}
    for i in text.split("\n"):
        jxfb(i,data1)
    return data1
def tissh(file:str):
    with open(file,"r",encoding="utf8") as f:
        data=tiqvsshd(f.read())
    with open("sshd.log","w",encoding="utf8") as f:
        f.writelines(data)#过滤掉不是sshd的
    with open("sshd.log","r",encoding="utf8") as f:
        data=splitstr(f.read())
    with open("sshd.log","w",encoding="utf8") as f:
        f.writelines(data)
    with open("sshd.log","r",encoding="utf8") as f:
        data=jxfeng(f.read())
    with open("sshd.log","w",encoding="utf8") as f:
        f.writelines(data)
def js(text):
    ok_l=[]
    def fglb(dic):
        d_l=[]
        for key in dic:
            d_l.append({key:dic[key]})
        return d_l
    b=jx(text)
    for i in (b):
        c=Counter(b[i])
        da=fglb(dict(c))
        for i1 in da:
            a=i1.copy()
            a.update({"username":i})
            ok_l.append(a)
    return ok_l
def save_csv(dat):
    ds="IP,归属地,运营商,用户名,次数"
    hc_l=[]
    for i in dat:
        ip,gsd,yys=list(i.keys())[0]
        um,c=i["username"],i[list(i.keys())[0]]
        hc_l.append(",".join((ip,gsd,yys.replace(",","，"),um,str(c))))
    return ds+"\n"+"\n".join(hc_l)

def index(file,save):
    tissh(file)
    with open("sshd.log","r",encoding="utf8") as f:
        with open(save, "w",encoding="utf_8_sig") as f1:
            f1.write(save_csv(js(f.read())))
a=sys.argv
if len(a)<3:
    pass
else:
    #print(a[1],a[2])
    index(a[1],a[2])