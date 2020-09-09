import copy
import os
import pathlib
import sqlite3

unknown_mac = 'ffffffffffff'
primaryTbl = None
not_null = 'NOT NULL'
primary_key = 'PRIMARY KEY'
auto_increment = 'AUTOINCREMENT'
uniaue = 'UNIQUE'
default = 'DEFAULT'
null = 'NULL'
foreign_key = 'FOREIGN KEY'
referances = 'REFERENCES'
insert = 'INSERT INTO'
select = 'SELECT'
update = 'UPDATE'
delete = 'DELETE'

HorseNameTbl = 'HorseNameTbl'
HorseBloodTbl = 'HorseBloodTbl'
RequestTbl = 'RequestTbl'

class class_SQLite():
    def __init__(self):
        path = os.getcwd()
        path = path + '\\data'
        path = os.path.split(path)
        path = path[0]
        ret = pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        self.database_name = path + '\\HorseBlood.db'
        self.link_dict_after = dict()
        return

    def set_link_dict(self,link_dict):
        self.link_dict_after = copy.deepcopy(link_dict)

    def connect_DB(self):
        self.DBconnect = sqlite3.connect(self.database_name)
        self.DBcursor = self.DBconnect.cursor()
        return

    def disconnect_DB(self):
        self.DBconnect.close()

    def commit_DB(self):
        self.DBconnect.commit()

    def create_Horse_Tbl(self):
        sql_cmd = f'CREATE TABLE IF NOT EXISTS "{HorseNameTbl}" '
        sql_cmd = sql_cmd + \
            f'("pkey" INTEGER {not_null} {primary_key} {auto_increment} {uniaue}'
        sql_cmd = sql_cmd + f',"Name" TEXT {not_null}'
        sql_cmd = sql_cmd + f',"Birthday" TEXT {not_null}'
        sql_cmd = sql_cmd + f',"URL" TEXT )'

        self.DBcursor.execute(sql_cmd)

        return

    def create_HorseBlood_Tbl(self):
        sql_cmd = f'CREATE TABLE IF NOT EXISTS "{HorseBloodTbl}" '
        sql_cmd = sql_cmd + \
            f'("pkey" INTEGER {not_null} {primary_key} {auto_increment} {uniaue}'
        sql_cmd = sql_cmd + f',"horse_pkey" INTEGER {not_null}'
        sql_cmd = sql_cmd + f',"f" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"m" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"ff" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"fm" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"mf" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"mm" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"fff" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"ffm" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"fmf" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"fmm" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"mff" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"mfm" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"mmf" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"mmm" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"ffff" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"fffm" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"ffmf" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"ffmm" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"fmff" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"fmfm" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"fmmf" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"fmmm" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"mfff" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"mffm" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"mfmf" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"mfmm" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"mmff" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"mmfm" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"mmmf" INTEGER {default} {null}'
        sql_cmd = sql_cmd + f',"mmmm" INTEGER {default} {null})'

        self.DBcursor.execute(sql_cmd)

        return

    def create_Request_Tbl(self):
        sql_cmd = f'CREATE TABLE IF NOT EXISTS "{RequestTbl}" '
        sql_cmd = sql_cmd + \
            f'("pkey" INTEGER {not_null} {primary_key} {auto_increment} {uniaue}'
        sql_cmd = sql_cmd + f',"Name" TEXT {not_null}'
        sql_cmd = sql_cmd + f',"URL" TEXT '
        sql_cmd = sql_cmd + f',"horse_pkey" INTEGER {default} {null})'

        self.DBcursor.execute(sql_cmd)

    def replace_Horse_Tbl(self,HorseName,Birthday,url,horse_pkey):
        if Birthday is None:
            Birthday = f'{null}'
        if url is None:
            url = f'{null}'

        if horse_pkey is None:
            sql_cmd = f'{select} * FROM {HorseNameTbl} WHERE Name = "{HorseName}" AND URL = "{url}"'
        else:
            sql_cmd = f'{select} * FROM {HorseNameTbl} WHERE pkey = "{horse_pkey}"'
        self.DBcursor.execute(sql_cmd)
        TblInfo = self.DBcursor.fetchall()

        if TblInfo:
            pkey = TblInfo[0][0]
            if TblInfo[0][2] != 'NULL' and TblInfo[0][2]:
                Birthday = TblInfo[0][2]
            sql_cmd = f'{update} {HorseNameTbl} SET (Name,Birthday,URL) = ("{HorseName}","{Birthday}","{url}") WHERE pkey={pkey}'
            self.DBcursor.execute(sql_cmd)
        else:
            sql_cmd = f'{insert} {HorseNameTbl} (Name,Birthday,URL) VALUES ("{HorseName}","{Birthday}","{url}")'
            self.DBcursor.execute(sql_cmd)

            sql_cmd = f'{select} pkey FROM {HorseNameTbl} WHERE rowid = last_insert_rowid()'
            self.DBcursor.execute(sql_cmd)

            TblInfo = self.DBcursor.fetchall()
            if TblInfo:
                pkey = TblInfo[0][0]

        return pkey

    def replace_HorseBoold_Tbl(self,HorseName,Birthday,horse_blood,link_dict,url,horse_pkey):

        if horse_pkey is None:
            sql_cmd = f'{select} * FROM {HorseNameTbl} WHERE Name = "{HorseName}" AND URL = "{url}"'
        else:
            sql_cmd = f'{select} * FROM {HorseNameTbl} WHERE pkey = "{horse_pkey}" '

        self.DBcursor.execute(sql_cmd)
        TblInfo = self.DBcursor.fetchall()

        if TblInfo:
            horse_pkey = TblInfo[0][0]

            set_param = ''

            for horse_name in horse_blood:
                if horse_name is not None:
                    horse_name = horse_name.replace(' ','_')
                    URL, hPkey = link_dict[horse_name]
                    set_param += f'{hPkey},'
                else:
                    set_param += f'{null},'
            else:
                set_param = set_param.rstrip(',')

            sql_cmd = f'{select} pkey FROM {HorseBloodTbl} WHERE horse_pkey = {horse_pkey}'
            self.DBcursor.execute(sql_cmd)
            TblInfo = self.DBcursor.fetchall()
            if TblInfo:
                pkey = TblInfo[0][0]
                sql_cmd = f'{update} {HorseBloodTbl} SET '\
                    + f'(f,m,ff,fm,mf,mm)=({set_param}) WHERE horse_pkey={horse_pkey}'
            else:
                sql_cmd = f'{insert} {HorseBloodTbl} '\
                    + f'(horse_pkey,f,m,ff,fm,mf,mm) VALUES ({horse_pkey},{set_param})'

            self.DBcursor.execute(sql_cmd)

        return

    def replace_request_Tbl(self,link_dict):

        add_dict = dict()
        remove_dict = dict()

        for k, v in link_dict.items():
            if k not in self.link_dict_after:
                add_dict.setdefault(k, v)

        for k, v in self.link_dict_after.items():
            if k not in link_dict:
                remove_dict.setdefault(k, v)

        self.link_dict_after = copy.deepcopy(link_dict)

        tbl_name = 'RequestTbl'

        for k, v in add_dict.items():
            url, key = v
            #sql_cmd = f'{select} * FROM {tbl_name} WHERE Name = "{k}" AND URL = "{v}"'
            sql_cmd = f'{select} * FROM {tbl_name} WHERE Name = "{k}" AND horse_pkey = {key}'
            self.DBcursor.execute(sql_cmd)
            TblInfo = self.DBcursor.fetchall()
            if TblInfo:
                pkey = TblInfo[0][0]
                sql_cmd = f'{update} {tbl_name} SET (Name,URL,horse_pkey) = ("{k}","{url}",{key}) WHERE pkey={pkey}'
            else:
                sql_cmd = f'{insert} {tbl_name} (Name,URL,horse_pkey) VALUES ("{k}","{url}",{key})'

            self.DBcursor.execute(sql_cmd)

        for k, v in remove_dict.items():
            url, key = v
            sql_cmd = f'{delete} FROM {tbl_name} WHERE Name = "{k}" AND horse_pkey = {key}'
            self.DBcursor.execute(sql_cmd)

        return

    def get_request_Tbl(self):
        self.connect_DB()

        tbl_name = 'RequestTbl'
        sql_cmd = f'{select} Name,URL,horse_pkey FROM {tbl_name}'
        self.DBcursor.execute(sql_cmd)
        TblInfo = self.DBcursor.fetchall()
        if TblInfo:
            for Name,URL,horse_pkey in TblInfo:
                self.link_dict_after.setdefault(Name,[URL,horse_pkey])

        self.disconnect_DB()

        return self.link_dict_after

    def get_HorseURL_Tbl(self,url):
        self.connect_DB()

        sql_cmd = f'{select} * FROM {HorseNameTbl} WHERE URL = "{url}" AND NOT Birthday = "{null}"'
        self.DBcursor.execute(sql_cmd)
        TblInfo = self.DBcursor.fetchall()

        self.disconnect_DB()

        if TblInfo:
            return True
        else:
            return False
