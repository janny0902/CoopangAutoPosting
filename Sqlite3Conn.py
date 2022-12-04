import sqlite3
import time

class SQL_CONNECT:
    def __init__(self):
        self.db_path = ""  #DB경로
        self.nowdate = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    ##--------------------조회 기능--------------------------
    def SQL_UserSelect(self,tableNm):
        #회원 조회하기
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + tableNm )
        rows = cur.fetchall()
        user=[]

        for row in rows:
            print(row)
            user = row
        conn.close()
        return user
    def SQL_Count(self,tableNm):
        #회원 조회하기
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM " + tableNm )
        rows = cur.fetchall()

        conn.close()
        return rows

    def SQL_ListSelect(self,tableNm):
        #테이블 조회하기
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + tableNm )
        rows = cur.fetchall()
        item = []
        count=0
        for row in rows:
            item.insert(count,row[0])
            count+=1
        conn.close()

    def SQL_ListSeach(self,tableNm):
        #테이블 조회하기
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + tableNm )
        rows = cur.fetchall()
        item = []
        count=0
        for row in rows:
            item.insert(count,row)
            count+=1
        conn.close()
        return(item)

    def SQL_ListReport(self,tableNm):
        #테이블 조회하기
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + tableNm+" WHERE S_DT = ?", [self.nowdate])
        rows = cur.fetchall()
        item = []
        count=0
        for row in rows:
            item.insert(count,row)
            count+=1
        conn.close()
        return(item)


    def SQL_ItemSelect(self,tableNm):
        #테이블 조회하기
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + tableNm +" WHERE USE_YN = 'Y'")
        rows = cur.fetchall()

        count=0
        return rows

    def SQL_ItemList(self,tableNm):
        #테이블 조회하기
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + tableNm +" WHERE USE_YN = 'N'")
        rows = cur.fetchall()
        count=0
        conn.close()

        return(rows)
    def SQL_ItemListO(self,tableNm):
        #테이블 조회하기
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + tableNm +" WHERE USE_YN = 'O'")
        rows = cur.fetchall()
        count=0
        conn.close()

        return(rows)

    def SQL_MsgSelect(self,tableNm):
        #테이블 조회하기
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + tableNm )
        rows = cur.fetchall()
        print(rows)

        item = []
        count=0
        for row in rows:
            item.insert(count,row[0])
            count+=1
        conn.close()

        return item


    def Sql_Distinct(self,tableNm,data):
        #데이터 중복값 있는지 조회
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + tableNm +' WHERE S_NUM = ?' , data )
        rows = cur.fetchall()

        return rows


    ## ---------------------- 삽입기능(INSERT)----------------------------
    def SQL_Insert_f(self,SqlString,s_tuple,useYn,n_Name,d_Date):
        #데이터 삽입하기
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(SqlString,(s_tuple,useYn,n_Name,d_Date))
        conn.commit()
        conn.close()

    def SQL_Insert(self,SqlString,s_tuple):
        #데이터 삽입하기
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(SqlString,(s_tuple) )
        conn.commit()
        conn.close()


    ## ---------------------- 수정기능(UPDATE) ---------------------------
    def SQL_Update(self,SqlString,data):
        #데이터 업데이트
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(SqlString,data)
        conn.commit()
        conn.close()


    ## ---------------------- 삭제기능(DELETE) ---------------------------
    def SQL_Delete(self,tableName):
        #데이터 업데이트
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM " + tableName)
        conn.commit()
        conn.close()

    def SQL_DeleteW(self,sqlString,data):
        #데이터 업데이트
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(sqlString,data)
        conn.commit()
        conn.close()

    def SQL_DeleteB(self,sqlString):
        #데이터 업데이트
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(sqlString)
        conn.commit()
        conn.close()

    def SQL_DeleteWD(self,sqlString):
        #데이터 업데이트
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(sqlString)
        conn.commit()
        conn.close()


