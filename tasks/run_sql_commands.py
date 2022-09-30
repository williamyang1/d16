import pymysql
def run_sqlcmd(cmd):
    # conn=pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="111111",charset="utf8")
    conn=pymysql.connect(host="dlswqa-nas.nvidia.com",port=13306,user="cudnn_qa",passwd="123456",charset="utf8")
    #conn=pymysql.connect(host="10.19.172.245",port=3306,user="root",passwd="111111",charset="utf8")
    cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql_cmd=cmd
    data_list=[]
    if cmd.find("SELECT")!=-1:
        cursor.execute(sql_cmd)
        data_list=cursor.fetchall()

    else:
        print("Run commit")
        print(sql_cmd)
        cursor.execute(sql_cmd)
        conn.commit()
        data_list=["Run commands"]
    cursor.close()
    conn.close()
    return data_list

if __name__ == '__main__':
    #run_sqlcmd("UPDATE `qx_day16`.`app01_task` SET `title` = 'sdfaaa' WHERE (`id` = '1');")
    cmd="SELECT * FROM cudnn_auto_triage.TriageData as a join cudnn_auto_triage.Changelist as b  where a.CL_id = b.id and b.CL = '31825127'  and a.nvbug_id like '%not%' order by a.error_msg;"
    res=run_sqlcmd(cmd)
    for i in res:
        print("LLLLLLL",i)


