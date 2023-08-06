#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright 2023 Wael Hojak

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

###########################################################

Created on Sat Nov 26 20:29:30 2022
@author: Wael Hojak

provides the classes: 'FaRoC_Reader', 'FaRoC_Writer' and 'FaRoC_Mover'.

'FaRoC_Reader':
    can ONLY communictate with the KAREL program 'FAROC_SERVER' 
    can read data fron robot.
'FaRoC_Writer':
    can ONLY communictate with the KAREL program 'FAROC_SERVER'.
    extends the 'FaRoC_Reader' class with the writing option.
'FaRoC_Mover':
    can ONLY communictate with the KAREL program 'FAROC_MOVER'.
    extends the 'FaRoC_Writer' class with the writing option.
    
'FaRoC_Mover' inherits from 'FaRoC_Writer' inherits from 'FaRoC_Reader'.

"""

from faroc.fanuc_alarm_codes.fanuc_error_tools import DF_FACILITY_CODES, error_detail, error_detail_api, error_detail_online
import socket
import struct
from time import sleep

VERSION = '0.7.5'

KTYPE_2_DTYPE = {'REAL':'R', 'INTEGER':'I', 'SHORT':'I', 'BYTE':'I', 'BOOLEAN':'B', 'STRING':'S'}
PYTHON_2_KTYPE = {float:'REAL', int:'INTEGER', bool:'BOOLEAN', str:'STRING' }
# BOOLEAN must unpack as long (4 Byte)
DTYPE_2_CTYPE = {'R':'f', 'I':'l', 'B':'l', 'S':'s'}
SUCCESS_CODE = 0
ERROR_CODE = 1


# Attributes that can be retrieved with "get_task_info"
TASK_ATTRIBUTE = {'TSK_PARENT': 119, 'TSK_PRIORITY': 102, 'TSK_TIMESLIC': 103,
                  'TSK_PROGTYPE': 105, 'TSK_STATUS': 107, 'TSK_PROGNAME': 131,
                  'TSK_ROUTNAME':132, 'TSK_STACK': 109, 'TSK_NOPAUSE': 111, 
                  'TSK_NOABORT': 110,'TSK_MCTL': 127, 'TSK_HOLDCOND': 108,
                  'TSK_LINENUM':106, 'TSK_LOCKGRP':126, 'TSK_NOBUSY':112,
                  'TSK_PAUSESFT':123, 'TSK_STEP':113, 'TSK_TPMOTION':115,
                  'TSK_TRACE':114, 'TSK_TRACELEN':118}



#%%        
class FaRoC_Reader():
    def __init__(
        self,
        robot_ip :str = '127.0.0.1',         # ip address of fanuc controller
        port :int = 24087,                       # the port of KAREL program "FAROC_SERVER"
        byte_order = '<',                         # byte order to unpack binary data
        socket_timeout : int = 5,
        debug_mode : bool = False,
    ):
        """
        Parameters
        ----------
        socket_timeout : int, optional
            Socket timeout in seconds. The default is 5.
        debug_mode : bool, optional
            to print more infos. The default is False.
        """
        self.mode = "FaRoC_Reader"
        self.robot_ip = robot_ip
        self.port = port 
        self.byte_order = byte_order
        self.sock_buff_sz = 1024
        self.socket_timeout = socket_timeout
        self.comm_sock = None
        # to get long Strings that can be longer than 128 byte we have to wait 
        # until push data is finish.
        self.wait_for_resp = 1  # ONLY for methose get_var_list
        self.wait_time = 0.1    # [s] wait time in case of 'wait_for_resp == True'
        self.debug_mode = debug_mode
        self.connected = False          # socket connect status
        self.error_table = DF_FACILITY_CODES


    def status(self)->None:
        """ Prints version and status infos of FaRoC (Fanuc Robot Control).""" 
        print("Fanuc Robot Control 'FaRoC'")
        print(f"Version          : {VERSION}")
        print(f'Python class     : {self.mode}')
        print(f"KARREL server    : {'FAROC_MOVER' if self.mode=='FaRoC_Mover' else 'FAROC_SERVER'}")
        print(f"Used socket      : {self.comm_sock}")
        print(f"Already connected: {'Yes' if self.connected else 'No'}")
        if self.connected:
            code, msg, data = self.ping()
            if code == SUCCESS_CODE:    
                print(f"Still connected  : {'Yes' if data[0]=='pong' else 'No'}")
            else:
                print(f"ERROR MESSAGE    : {msg}")


    def connect(self) -> (int, str):
        """Connects the PC (Client) to the robot (Server) via TCP protocol.
        Socket Messaging uses the TCP/IP protocol to transfer raw data, or data 
        that is in its original, unformatted form across the network."""
        # create socket and connect
        self.comm_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comm_sock.settimeout(self.socket_timeout)
        try:
            self.comm_sock.connect((self.robot_ip, self.port))
        except socket.error as err:
            print( f"{self.mode}: {err}")
            print(f"{self.mode}: Please run the KAREL programm"\
                  f" '{'FAROC_MOVER' if self.mode=='FaRoC_Mover' else 'FAROC_SERVER'}' "\
                  "on Robot! e.g. RUN the TP Program 'FAROC'.")
            return -1, err

        resp = self.comm_sock.recv(self.sock_buff_sz)
        code, msg, _ = self.handle_response(resp)
        
        if code == SUCCESS_CODE:
            print(f'{self.mode} connect status: {msg}') 
            self.connected = True
        return code, msg
    
    
    def disconnect(self) -> (int, str):
        """Dissconnects the communication with the server (robot)."""
        try:
            self.comm_sock.shutdown(socket.SHUT_RDWR)
            self.comm_sock.close()
        except OSError as err:
                print(f"{self.mode}: {err}")
                return -1, str(err)
        print(f"{self.mode} disconnect status: success")
        self.connected = False
        return SUCCESS_CODE, 'success'
        
        
    def send_cmd(self, cmd:str, d_type:str=None)->(int, str, list):
        """
        Sends commands to a robot and receives data back from it.
        Parameters
        ----------
        cmd : str
            Command string to send. length of cmd must be <= 127.
        d_type : str, optional
            Type of KAREL data to receive. The default is None.
            valid values: 'R', 'I', 'B' and 'S' for KAREL data types:
                REAL, INTEGER, BOOLEAN and STRING respectively.
        Returns
        -------
        (int, str, list)
            code : int
                0 if the operation was performed correctly, otherwise error code (status),
            msg : str
                string with 'success' or info about the error,
            data : list (or None if no data required or in case of an error)
                a list with the requested data.
        """
        cmd = cmd.strip()
        if self.debug_mode: print(f'cmd|{len(cmd)}|{cmd}|')
        assert len(cmd)<128, f'length of command (cmd) must be <= 127, got: {len(cmd)}'
        # extend 'cmd' with blanks until the length reaches 127.
        cmd +=  ' ' *(127-len(cmd))     # KAREL SERVER receives 127 bytes from socket at a time
        
        # 1. send command
        self.comm_sock.sendall(cmd.encode())
        # 2. wait a bit if you want to get many STRINGs from robot controller
        if self.wait_for_resp: sleep(self.wait_time)
        # 3. receive the response
        resp = self.comm_sock.recv(self.sock_buff_sz)
        self.resp = resp
        # 4. handle received response 
        return self.handle_response(resp, d_type)
        
    
    def handle_response(self, resp:bytes, d_type:str=None)->(int, str, list):
        """
        Handles response from socket communication.
        Parameters
        ----------
        resp : bytes
            Response bytes returned from socket.
        d_type : str, optional
            Type of KAREL data to receive. The default is None.
            valid values: 'R', 'I', 'B' and 'S' for KAREL data types:
                REAL, INTEGER, BOOLEAN and STRING respectively.
        Returns
        -------
        (int, str, list)
            code : int
                0 if the operation was performed correctly, otherwise error code (status),
            msg : str
                string with 'success' or info about the error,
            data : list (or None if no data required or in case of an error)
                a list with the requested data.
        """
        if self.debug_mode: print(f'resp|{len(resp)}[{resp}]')
        
        len_str = resp[0]   # frist byte ist the length of received string 
        format_ = f'{self.byte_order}{len_str}s' 
        if self.debug_mode: print(f'format String: [{format_}]')
        # the first string in the response byte contains code and msg
        code, msg = struct.unpack(format_, resp[1:1+len_str])[0].decode().split(':', maxsplit=1)
        code = int(code)
        # after the 1st string come the interesting data 
        data_byte = resp[1+len_str:]
        
        self.data_byte = data_byte
        
        if code == ERROR_CODE:
            # in this case KAREL sends only one INTERGER (4 bytes): "status" 
            status = struct.unpack(f'{self.byte_order}l', data_byte[:4])[0]
            print(f'msg: {msg}')
            print(f"Fanuc Error status: '{status}'")
            if status > 0:
                self.error_detail(status)
            code = status       # code contain NOW the status code
            
        data = None
        if d_type and code == SUCCESS_CODE:
            data = []
            if d_type == 'S':   # the interesting data are STRINGs
                while len(data_byte) > 0:
                    len_str = data_byte[0]      # 1st byte contains the length
                    st = data_byte[1:1+len_str].decode()
                    data.append(st)
                    data_byte = data_byte[1+len_str:]
            else:
                nr_data = int(len(data_byte)/4) # our server send ONLY 4-bytes-DATA
                if nr_data > 0:
                    c_type = DTYPE_2_CTYPE[d_type]
                    format_ = f'{self.byte_order}{nr_data}{c_type}'
                    if self.debug_mode: print(f'format non String: [{format_}]')
                    data =  list(struct.unpack(format_, data_byte))
                    
        return code, msg, data
        
    
    def ping(self)-> (int, str, list):
        """
        Ping the robot to check connectivity.
        Returns
        -------
        (int, str, list)
            code, msg: see function send_cmd.
            data: list with str 'pong'.
        """
        return self.send_cmd('ping___', d_type='S')
    
    
    def error_detail(self, status, source:str='manual') -> str:
        """
        Fetching details about the status from FANUC Manual:
            "OPERATOR'S MANUAL (Alarm Code List)
             R-30+B CONTROLLER / B-83284EN-1/02"
        However, there are three sources for this data, which can be entered as opional parameters.
        Parameters
        ----------
        status : int or str
            int: error status received from FANUC, e.g: 12311
            str: alarm code as displayed on TP, e.g.:'INTP-311'.
        soure: str, optional
            The source of the error information. 
            manual: Data has been extracted from the manual mentioned above.
            api:Data is fetched online via the API available at 'http://linuxsand.info/fanuc/'.
                It provides details to Alarm codes of FANUC Robotics, supports R-30iB controller (8.0 series).
            api_offline:Data was previously fetched and stored from the mentioned API.
            The default is 'manual'.
        Returns
        -------
        (str)
            message with the details about the error.
        """
        assert source in ['manual','api','api_offline'],  f"source must be 'manual','api' or'api_offline', got: {source}"
        if source == 'manual':
            return error_detail(status)
        elif source == 'api':
            return error_detail_online(status)
        else:
            return error_detail_api(status)
        
    
#%%############################################################################
##########                  ROBOT JOINTS & POSE                      ##########
# get
###############################################################################
    def get_curpos(self)-> (int, str, list):
        """
        Returns the current Cartesian position ( incl. configuration ) of the tool centre point. 
        Returns
        -------
        (int, str, list) 
            code: see function send_cmd.
            msg: 'success' and 'configuration' like 'N U T, 0, 0, 0' separated by '|' 
            data: list with 7 elements: configuration (as string) and the xyzwpr values.
        """
        cmd = "cur_pos"
        code, msg, data = self.send_cmd(cmd, d_type='R')
        if code == SUCCESS_CODE:
            data = [msg.split('|')[1]] + data
        return code, msg, data


    def get_curjpos(self, max_j:int=6)-> (int, str, list):
        """
        Gets current joint values. From J(1) to J(max_j).
        Parameters
        ----------
        max_j : int, optional
            The max. joint number to get. The default is 6. The default is 6.
        Returns
        -------
        (int, str, list)
            code, msg: see function send_cmd.
            data: list with the desired joint values.
        """
        assert max_j in range(1, 10), f'max_j must be in range [1-9], got: {max_j}'
        cmd = f"curjpos:{max_j:01d}"
        return self.send_cmd(cmd, d_type='R')


#%%############################################################################
##########             Robot In & Out (I/O: RI & RO)                 ##########
# get & set (setter for RO in FaRoC_Writer)
###############################################################################
    def get_rdo(self, rdo_nr:int) -> (int, str, list):
        """
        Get the value of a robot out (RO). TP -> MENU -> I/O -> Robot (OUT).
        Parameters
        ----------
        rdo_nr : int
            Number of the robot out.
        Returns
        -------
        (int, str, list) see function send_cmd.
        """
        assert rdo_nr in range(1,9), f'rdo_nr must be in range [1-8], got: {rdo_nr}'
        cmd = f'get_rdo:{rdo_nr}'
        return self.send_cmd(cmd, d_type='B')


    def get_rdi(self, rdi_nr:int) -> (int, str, list):
        """
        Get the value of a robot In (RI). TP -> MENU -> I/O -> Robot (IN).
        Parameters
        ----------
        rdi_nr : int
            Number of the robot in.
        Returns
        -------
        (int, str, list) see function send_cmd.
        """
        assert rdi_nr in range(1,9), f'rdi_nr must be in range [1-8], got: {rdi_nr}'
        cmd = f'get_rdi:{rdi_nr}'
        return self.send_cmd(cmd, d_type='B')
    
    
#%%############################################################################
##########               FLAG Registers (I/O: Flag)               #############
# get & set (setter in FaRoC_Writer)
###############################################################################
    def get_flag(self, flag_nr:int) -> (int, str, list):
        """
        Get the value of a flag register (F). TP -> MENU -> I/O -> Flag.
        Parameters
        ----------
        flag_nr : int
            Number of the robot flag.
        Returns
        -------
        (int, str, list) 
            code, msg: see function send_cmd.
            data: list with the value in FLAG[flag_nr].
        """
        assert flag_nr in range(1,1025), f'flag_nr must be in range [1-1024], got: {flag_nr}'
        cmd = f'gt_flag:{flag_nr:4}'
        return self.send_cmd(cmd, d_type='B')
        
    
#%%############################################################################
##########        Robot Variables incl. System Variables (SV)        ##########
# get & set variable from Type [REAL, INTEGER, SHORT, BYTE, BOOLEN, STRING]
# check KAREL TYPE of a variable       (setter in FaRoC_Writer)
###############################################################################
    def get_var(self, var_name:str, k_type:str='REAL', prog_name:str='*SYSTEM*')->(int, str, list):
        """
        Gets the value of a (system) variable. If prog_name='*SYSTEM*' get system variable.
        Parameters
        ----------
        var_name : str
            the full Name of system variable(s). e.g.: '$AP_PRC_DSBM[1]', '$PRO_CFG.$INS_PWR',
            or use '*' to get more variables, e.g.:'$AP_PRC_DSBM[*]', '$DPM_SCH[2].$GRP[1].$OFS[*].$INI_OFS'
            in this case you have to specify the start keyword.
        k_type : str, optional
            KAREL type of the system variable(s), REAL, INTEGER, BOOLEAN or STRING. The default is 'REAL'.
        prog_name : str, optional
            the name of the program to get its variable value. The default is '*SYSTEM*'.
        Returns
        -------
        (int, str, list)
            code, msg: see function send_cmd.
            data: list with the required value.
        """
        d_type = KTYPE_2_DTYPE[k_type.upper()]
        # Only one System Variable is retrieved
        cmd = f'get_var:{d_type}:{len(var_name):03d}:{var_name}:{len(prog_name):02}:{prog_name}' 
        return self.send_cmd(cmd, d_type)
    
    
    def get_var_list(self, var_name:str, start:int, end:int, k_type:str='REAL', 
                prog_name:str='*SYSTEM*')->(int, str, list):
        """
        Gets the values of a list of (system) variables. If prog_name='*SYSTEM*' get system variable.
        Parameters
        ----------
        var_name : str
            the full Name of system variable(s). e.g.: '$AP_PRC_DSBM[1]', '$PRO_CFG.$INS_PWR',
            or use '*' to get more variables, e.g.:'$AP_PRC_DSBM[*]', '$DPM_SCH[2].$GRP[1].$OFS[*].$INI_OFS'
            in this case you have to specify the start keyword.
        start : int
            get variables from this index, e.g.: from '$AP_PRC_DSBM[start]'
        end : int
            get variables until this index, e.g.: '$AP_PRC_DSBM[end]'.
        d_type : str, optional
            the type of the system variable(s), REAL, INTEGER, BOOLEAN or STRING. The default is 'REAL'.
        prog_name : str, optional
            the name of the program to get its variable value. The default is '*SYSTEM*'.
        Returns
        -------
        (int, str, list) 
            code: int, see function send_cmd.
            msg : str, string with 'HIT' or info about the error,
            data: list of the required data
        """
        d_type = KTYPE_2_DTYPE[k_type.upper()]
        lst = var_name.split('*')
        assert len(lst) <= 2, f'var_name must contain ONE "*" if "start" is defined, got: {var_name}'
        
        # An array of SystemVariables is retrieved with length >= 1
        var_name_pref = lst[0]
        var_name_suf = lst[1]
        
        assert end >= start and end <= 999, \
            f'end ({end}) must be greater or equal to start ({start}) and max. 999'

        nr_data = end - start + 1   # number system variables to get
        
        if nr_data == 1:            # only one variable
            var_name = var_name_pref + str(start) + var_name_suf
            return self.get_var(var_name, k_type, prog_name)
        
        # command for more than one variable
        cmd = f'gt_vr_l:{d_type}:{start:03d}:{end:03d}:{len(var_name_pref):02d}:{var_name_pref}'\
            f':{len(var_name_suf):02d}:{var_name_suf}:{len(prog_name):02}:{prog_name}' 
        
        # to get long Strings that can be longer than 128 byte we have to 
        # wait until push data is finish & to increase buffer size
        if d_type == 'S':
            self.wait_for_resp = True
            tmp_buff_sz = self.sock_buff_sz
            self.sock_buff_sz = 1024*8      # ADJUST if necessary!!!
            
        if nr_data > 30:    # In this case we send many requests
            data = []
            s = start
            e = min(end, start+29)
            while s <= end:
                cmd = f'gt_vr_l:{d_type}:{s:03d}:{e:03d}:{len(var_name_pref):02d}:{var_name_pref}'\
                    f':{len(var_name_suf):02d}:{var_name_suf}:{len(prog_name):02}:{prog_name}' 
                code, msg, data_ = self.send_cmd(cmd, d_type)
                s += 30 
                e = min(e+30, end)
                data += data_
        else:
            code, msg, data = self.send_cmd(cmd, d_type)
                    
        if d_type == 'S':             # Restore the default values 
            self.wait_for_resp = False
            self.sock_buff_sz = tmp_buff_sz
                
        return code, msg, data
        
    
    def get_ins_power(self) -> (int, str, list):
        """ 
        Gets instantaneous power consumption in watt. 
        """
        code, msg, data = self.get_var('$PRO_CFG.$INS_PWR', k_type='REAL')
        # Fanuc returns in kW. Should be adjusted to other robots.
        ins_pwr =  [_*1000 for _ in data] if code == SUCCESS_CODE else None
        return code, msg, ins_pwr
    
    
    def get_mch_pos(self):
        """ Get the Value of a System Variable. '$SCR_GRP[1].$MCH_POS_*' for * in 'XYZWPR'. """
        return self.send_cmd('mch_pos', d_type='R')


    def get_rem_ofs(self):
        var_name = '$DPM_SCH[1].$GRP[1].$OFS[*].$REM_OFS'
        return self.get_var_list(var_name, k_type='REAL', start=1, end=6)
                                              

    def get_app_ofs(self)->(int, str, list):
        var_name = '$DPM_SCH[1].$GRP[1].$OFS[*].$APP_OFS'
        return self.get_var_list(var_name, k_type='REAL', start=1, end=6)
    
    
    def get_var_type(self, var_name:str, prog_name:str='*SYSTEM*')->(int, str, list):
        """
        Get the KAREL data type of a variable. The types SHORT & BYTE are treated 
        as INTEGER. KAREL type are: [REAL, INTEGER, BOOLEAN, STRING].
        Parameters
        ----------
        var_name : str
            the name of the system variable
        prog_name : str, optional
            the name of the program to get its variable value. The default is '*SYSTEM*'.
        Returns
        -------
        (int, str, list)
            code, msg: see function send_cmd.
            data contain 2 strings: karel type and value of the variable.
        """
        cmd = f'gt_vr_t:{len(var_name):03d}:{var_name}:{len(prog_name):02}:{prog_name}' 
        return self.send_cmd(cmd, d_type='S')
        
    
    def sort_var_list(self, sv_list:list, prog_name:str='*SYSTEM*')->(int, str, list):
        """
        Sort a list of system variables (SV) in 4 Lists: 
        1st for REAL SV, 2nd for INTEGER, SHORT and BYTE SV, 3rd for BOOLEAN SV
        and 4th for STRING SV.
        Parameters
        ----------
        sv_list : list
            The list of system variables to sort.
        prog_name : str, optional
            the name of the program to sort its variable by type. The default is '*SYSTEM*'.
        Returns
        -------
        (int, str, list)
            code, msg: see function send_cmd.
            data: list of the 4 lists with the sorted SV.
        """
        sys_var_real, sys_var_int = [], []
        sys_var_bool, sys_var_str = [], []
        
        for sv in sv_list:
            code, msg, data = self.get_var_type(sv)
            if code != 0: 
                return code, msg, None
            d_type = data[0]
            if d_type == 'REAL': sys_var_real.append(sv)
            elif d_type == 'INTEGER': sys_var_int.append(sv)
            elif d_type == 'BOOLEAN': sys_var_bool.append(sv)
            elif d_type == 'STRING': sys_var_str.append(sv)
        data = [sys_var_real, sys_var_int, sys_var_bool, sys_var_str]
        return code, msg, data


    def check_sys_var_lst(self, sys_var_lst:list, k_type:str='REAL', show_detail:bool=False)->(int, str):
        """
        Checks if a list of system variables can be retrieved.
        Parameters
        ----------
        sys_var_lst : list
            A list with the names of the system variables as strings.
        k_type : str, optional
            KAREL type of the system variable(s), REAL, INTEGER, BOOLEAN and STRING. The default is 'REAL'.
        show_detail : bool, optional
            Specifies whether to show datails on the console. The default is False.
        Returns
        -------
        (int, str) code, msg: see function send_cmd.
        """
        # m: (just for print) the length of the longest name of the system variable 
        if len(sys_var_lst) > 0:
            m = max([len(sv) for sv in sys_var_lst])
        for sv in sys_var_lst:
            code, msg, data = self.get_var(sv, k_type)
            if code != 0: return code, msg
            if show_detail: print(f'{sv:{m}} = {data if code == SUCCESS_CODE else msg}')
        return 0, 'success'


    def get_user_fram(self)->(int, str, list):
        return self.get_var('$MNUFRAMENUM[1]', k_type='BYTE')
    
    
    def get_tool_fram(self)->(int, str, list):
        return self.get_var('$MNUTOOLNUM[1]', k_type='BYTE')
    
    
#%%############################################################################
##########                 USER FRAMES & TOOL FRAMES               ############
# get & set (setter in FaRoC_Writer)
###############################################################################
    def get_frame(self, frame_type:str, frame_nr:int) -> (int, str, list):
        """
        Get the pose and configuration of a given user or tool frame.
        ----------
        frame_type : str
            'user' to set user framem 'tool' to set tool frame
        frame_nr : int
            number of the position register to set.
        Returns
        -------
        (int, str, list) 
            code, msg -> see function send_cmd.
            data:  LIST with the values just set, i.e.:
                'UTOOL' or 'UFRAME', configuration and xyzwpr.
        """
        assert frame_type in ['user', 'tool'], f"frame_type must be 'user' or 'tool', got: {frame_type}"        
        if frame_type == 'user':
            assert frame_nr in range(1,10), f"frame_nr must be in range [1-9], got: {frame_nr}"
        if frame_type == 'tool':
            assert frame_nr in range(1,11), f"frame_nr must be in range [1-10], got: {frame_nr}"

        cmd = f"gt_fram:{frame_type[0]}:{frame_nr:02}"

        code, msg, data =  self.send_cmd(cmd, d_type='R')
        if code == SUCCESS_CODE:
            msg_data = msg.split('|') 
            data = [msg_data[1]] + [msg_data[2]] + data
            msg = msg_data[0]
        return code, msg, data


#%%############################################################################
##########               DATA Registers                           #############
# reset, set & get (for value & comment)    (setter in FaRoC_Writer)
###############################################################################
    def get_reg(self, reg_nr:int)->(int, str, list):
        """ Get the value of the DATA register number 'reg_nr'. IF value is an INTEGER,
        it will be muliplied with 1.0 and send as REAL. """
        assert reg_nr > 0, f'Error: reg_nr must be postiv, got: {reg_nr}.'
        cmd = f'get_reg:{reg_nr:03d}' 
        return self.send_cmd(cmd, d_type='R')


    def get_reg_comment(self, reg_nr:int)->(int, str, list):
        """ Get the COMMENT of the DATA register number 'reg_nr'. """
        assert reg_nr > 0, f'Error: reg_nr must be postiv, got: {reg_nr}.'
        cmd = f'gt_rcmt:{reg_nr:03d}' 
        return self.send_cmd(cmd, d_type='S')
    
    
#%%############################################################################
##########                  Robot String Registers (SR)              ##########
# get, set & reset (value & comment)    (setter in FaRoC_Writer)
###############################################################################
    def get_str_reg(self, str_reg_nr:int)->(int, str, list):
        """
        Get the value of a string register (SR).
        Parameters
        ----------
        str_reg_nr : int
            Number of string register to get its value.
        Returns
        -------
        (int, str, list) see function send_cmd.
        """
        cmd_val = f'gt_sreg:{str_reg_nr:02d}'
        return self.send_cmd(cmd_val, d_type='S')

    def get_str_reg_cmt(self, str_reg_nr:int)->(int, str, list):
        """
        Get the comment of a string register (SR).
        Parameters
        ----------
        str_reg_nr : int
            Number of string register to get its value.
        Returns
        -------
        (int, str, list) see function send_cmd.
        """
        cmd_val = f'gt_scmt:{str_reg_nr:02d}'
        return self.send_cmd(cmd_val, d_type='S')


#%%############################################################################
##########               Robot Date & Time                           ##########
# get & set     (setter in FaRoC_Writer)
###############################################################################
    def get_time(self)->(int, str, str):
        """
        Get the current time of the robot.
        Returns
        -------
        (int, str, str)
            code: see function send_cmd.
            msg: string with the converted time in the robot
            data: list the INTEGER represnting TIME and string with the time
            claculated by __cnv_time_str (incl. second)
        """
        code, msg, data = self.send_cmd('gt_time', d_type='I')
        if code != SUCCESS_CODE: return code, msg, data
        time_int = data[0]
        time_str = self.__cnv_time_str(time_int)
        return code, msg, [time_int, time_str]
        
    
    def __cnv_time_str(self, time_int:int)-> str:
        """
        Convert the INTEGER obtained from robot (GET_TIME) in Date-Time-Format incl. second
        Parameters
        ----------
        time_int : int
            The INTEGER obtained from robot, e.g.: 1433692473
        Returns
        -------
        str
            time_str: The reprasention of time in the format:
                YYYY:MM:DD hh:mm:ss , e.g.: '2022:11:20 13:09:25'
        """
        t_b = bin(time_int)[2:]
        year = int(t_b[:6], 2) + 1980
        month = int(t_b[6:10], 2)
        day = int(t_b[10:15], 2)
        hour = int(t_b[15:20], 2)
        minute = int(t_b[20:26], 2)
        second = int(t_b[26:31], 2)
        time_str = f'{year:02d}.{month:02d}.{day:02d} {hour:02d}:{minute:02d}:{second:02d}'
        return time_str
    
      
#%%############################################################################
##########           ROBOT TASK Status  & Program Type             ############
# run & stop Data client (KAREL program)
# get task status & program type
###############################################################################
    def run_data_client(self, client_nr:int)->(int, str):
        """ Run the task 'FaRoC_dClnt*' number 'client_nr'. """
        task_name = f'FaRoC_dClnt{client_nr}'
        code, msg, _ = self.send_cmd(f'run_tsk:0:{len(task_name):02d}:{task_name}')
        return code, msg
    
    
    def stop_data_client(self, client_nr:int)->(int, str):
        """ Stop the task 'FaRoC_dClnt*' number 'client_nr'. """
        task_name = f'FaRoC_dClnt{client_nr}'
        code, msg, _ =  self.send_cmd(f'stp_tsk:{len(task_name):02d}:{task_name}')
        return code, msg
    
    
    def get_client_status(self, client_nr:int)->(int, str, list):
        """ Get the status of the task 'FaRoC_dClnt*' number 'client_nr'. """
        task_name = f'FaRoC_dClnt{client_nr}'
        return self.get_task_status(task_name)
    
    
    def check_attributes(self)->(int, str):
        """
        Check tha value in TASK_ATTRIBUTE (see header) for the KAREL ROUTINE: GET_TSK_INFO.
        UNSURE: on a different controller the values could be different!.
        Returns
        -------
        (int, str) see function send_cmd.
        """
        code, msg, _ = self.send_cmd('chk_att')
        return code, msg

    
    def get_task_info(self, task_name:str, attribute:str)->(int, str, list):
        """
        Get the value attribute of a running or paused Task 'task_name'. If the 
        specified task is not running, paused or aborted methode will return error code 3016.
        Parameters
        ----------
        task_name : str
            Name of Task.
        attribute : str
            Name of the task attribute to get its value. see TASK_ATTRIBUTE above.
        Returns
        -------
        (int, str, list) code, msg: see function send_cmd.
            data: list with the task status as int and the description as string.
        """
        attr_int = TASK_ATTRIBUTE[attribute.upper()]
        cmd = f'tsk_inf:{attr_int:03}:{len(task_name):02d}:{task_name}'
        code, msg, data = self.send_cmd(cmd, d_type='S')
        if code == SUCCESS_CODE:
            data_str = data[0].split('|')
            data = [int(data_str[0]), data_str[1]]
        return code, msg, data
    
    
    def get_task_status(self, task_name:str)->(int, str, list):
        """
        Get the status of the Task 'task_name'. Returns one of 5 ans.:
        "running", "aborted", "paused", "Run request has been accepted" or 
        "Abort has been accepted". If the specified task is not running, paused
        or aborted methode will return error code 3016.
        Parameters
        ----------
        task_name : str
            Name of Task.
        Returns
        -------
        (int, str, list) code, msg: see function send_cmd.
            data: list with the task status as int and the description as string.
        """
        code, msg, data = self.send_cmd(f'tsk_sta:{len(task_name):02d}:{task_name}', d_type='S')
        if code == SUCCESS_CODE:
            data_str = data[0].split('|')
            data = [int(data_str[0]), data_str[1]]
        return code, msg, data
    
    
    def get_prog_type(self, task_name:str)->(int, str, list):
        """
        Get the program type of the Task 'task_name'. Returns one of 3 ans.:
            "TP-prog", "KAREL-prog", or "Program has not been executed yet".
        Parameters
        ----------
        task_name : str
            Name of Task.
        Returns
        -------
        (int, str, list) code, msg: see function send_cmd.
            status: list with the program type as string
        """
        return self.send_cmd(f'tsk_pty:{len(task_name):02d}:{task_name}', d_type='S')
    
    
#%%############################################################################
##########               POSITION REGISTER PR[*]                  #############
# get_type, is_reachable, joint_to_pos, pos_to_joint, get & set (setter in FaRoC_Writer)
###############################################################################
    def get_pos_reg_type(self, pos_reg_nr:int) -> (int, str, list):
        """
        Returns the position representation of the specified position register.
        pos_reg_types: (1 : POSITION), (2 : XYZWPR), (6 : XYZWPREXT), (9 : JOINTPOS).
        Parameters
        ----------
        pos_reg_nr : int
            number of the position register (3 digits).
        Returns
        -------
        (int, str, list) see function send_cmd.
            data: list of 3 elements: 1. posn_type: (int) representation as int (see KAREL manual)
                                      2. num_axes: (int) number of axis (only for JOINTPOS, XYZWPREXT)
                                      3. (str) representation as string.
        """
        assert pos_reg_nr in range(1,101), f"position register number must be in range [1-100], got: {pos_reg_nr}"
        pos_reg_types = {1:'POSITION', 2:'XYZWPR', 6:'XYZWPREXT', 9:'JOINTPOS'}
        code, msg, data = self.send_cmd(f'gt_pr_t:{pos_reg_nr:3}', d_type='I')
        if code == SUCCESS_CODE:
            data.append( pos_reg_types[data[0]] )
        return code, msg, data
    
    
    def get_pos_reg(self, pos_reg_nr:int) -> (int, str, list):
        """
        Returns the position representation of the specified position register.
        pos_reg_types: (1 : POSITION), (2 : XYZWPR), (6 : XYZWPREXT), (9 : XYZWPREXT).
        Parameters
        ----------
        pos_reg_nr : int
            number of the position register (3 digits).
        Returns
        -------
        (int, str, list) code, msg: see function send_cmd.
            msg: also contains the type and, except for JOINTPOS, the configuration string of the pose.
            data: 
                POSITION: list of 12 elements. 4 VECTORS: NORMAL, ORIENT, APPROACH,LOCATION.
                XYZWPR: list of 6 elements. x,y,z,w,p,r.
                XYZWPREXT: list of 9 elements. x,y,z,w,p,r,ext1,ext2,ext3.
                JOINTPOS: list of 6 or 9 elements, J1-J6 or J1-J9.
        """ 
        assert pos_reg_nr in range(1,101), f"position register number must be in range [1-100], got: {pos_reg_nr}"
        code, msg, data = self.send_cmd(f'gt_preg:{pos_reg_nr:03}', d_type='R')
        if code == SUCCESS_CODE:
            msg_data = msg.split('|') 
            if 'JOINTPOS' in msg_data[1]:
                data = [msg_data[1]] + data
            else:
                data = [msg_data[1]] + [msg_data[2]] + data
            msg = msg_data[0]
        return code, msg, data
    
    
    def set_check_pos_reg(self, pos_reg_nr:int, point_type:str, vals:list, ext_ang:list=None, config:str=None) -> (int, str, list):
        """
        Set position values POSJOINT or XYZWPR in a position register (PR).
        Parameters
        ----------
        pos_reg_nr : int
            number of the position register to set.
        point_type : str
            type of point representation, "joint" or "pose".
        vals : list
            point representation as list of [j1-j6] or [xyzwpr].            
        ext_ang : list, optional
            Extended Joint values, when available. The default is None.
        config : str (only for pose)
            the configuration of pose, e.g.: 'FUT,0,0,0'
        Returns
        -------
        (int, str, list) 
            code, msg -> see function send_cmd.
            data:  LIST with is_reachable and 2 Lists.
                is_reachable:   bool (True or False) is the first element in data.
                1.st List:      list with the given data to check or set in PR.
                2.nd list:      list with data converted from the given data. joint <-> pose.
        """
        assert point_type in ['joint', 'pose'], f"point_type must be 'joint' or 'pose', got: {point_type}"
        assert len(vals) == 6, f"length of vals must be 6, got: {len(vals)}"
        assert ext_ang == None or len(ext_ang)==3, f"ext_ang must have the length 3 or be None, got: {ext_ang}"
        assert (point_type == "joint")or(point_type == "pose" and config), f"...{config}"
        
        num_axes = 6 # default value
        if point_type == "joint":
            num_axes = 9 if ext_ang else 6
            cmd = f"st_pr_j:{pos_reg_nr:03}:{num_axes}"
        elif point_type == "pose":
            cmd = f"st_pr_p:{pos_reg_nr:03}:{config:25}"

        # prepare joint values
        for val in vals:
            val_str = f"{abs(val):09.4f}"
            sign = "+" if val >= 0 else "-"
            cmd += f":{sign}{val_str}"
        
        if point_type == "joint" and ext_ang != None:
                for val in ext_ang:
                    val_str = f"{abs(val):09.4f}"
                    sign = "+" if val >= 0 else "-"
                    cmd += f":{sign}{val_str}"
            
        code, msg, data =  self.send_cmd(cmd, d_type='R')
        if code == SUCCESS_CODE:
            msg_data = msg.split('|')
            data[0] = True if data[0]==1.0 else False
            if point_type == "joint":
                data = [data[0]] + [data[1:num_axes+1]] + [[msg_data[-1]] + data[1+num_axes:]]
            else:
                data = [data[0]] + [[msg_data[-1]] + data[1:num_axes+1]] + [data[1+num_axes:]]
            msg = msg_data[0]
        return code, msg, data
    
    
    def is_reachable(self, point_type:str, vals:list, ext_ang:list=None, config:str=None) -> (int, str, list):
        """
        Checks the reachability of position values POSJOINT or XYZWPR. if one value in vals is None, 
        the current value of this joint/coordinate is adopted. In case of 'pose'
        xyzwpr is included in val, but CONFIG will be adopted from the current pose.
        Parameters
        ----------
        point_type : str
            type of point representation, "joint" or "pose".
        vals : list
            point representation as list of [j1-j6] or [xyzwpr].            
        ext_ang : list, optional
            Extended Joint values, when available. The default is None.
        config : str (only for pose)
            the configuration of pose, e.g.: 'FUT,0,0,0'
        Returns
        -------
        (int, str, list) code, msg -> see function send_cmd.
                         data: LIST of one element, is_reachable: bool (True or False)
        """
        return self.set_check_pos_reg(0, point_type, vals, ext_ang, config)
    
    
    def pos_to_joint(self, vals:list, config:str) -> (int, str, list):
        """
        Checks the reachability of position values POSJOINT or XYZWPR. if one value in vals is None, 
        the current value of this joint/coordinate is adopted. In case of 'pose'
        xyzwpr is included in val, but CONFIG will be adopted from the current pose.
        Parameters
        ----------
        vals : list
            point representation as list of [j1-j6] or [xyzwpr].            
        config : str
            the configuration of pose, e.g.: 'FUT,0,0,0'
        Returns
        -------
        (int, str, list) 
            code, msg -> see function send_cmd.
            data:  LIST with is_reachable, XYZWPR and JOINPOS.
                is_reachable:   bool (True or False) is the first element in data.
                XYZWPR:         list with the given data
                JOINPOS:        list with the joint values converted from XYZWPR.
        """
        return self.set_check_pos_reg(0, 'pose', vals, config=config)
        
    
    def joint_to_pos(self, vals:list, ext_ang:list=None) -> (int, str, list):
        """
        Convetrs a given JOINTPOS position to XYZWPR.
        Parameters
        ----------
        vals : list
            JOINTPOS, point representation as list of [j1-j6].             
        ext_ang : list, optional
            Extended Joint values, when available. The default is None.
        Returns
        -------
        (int, str, list) 
            code, msg -> see function send_cmd.
            data:  LIST with is_reachable, XYZWPR and JOINPOS.
                is_reachable:   bool (True or False) is the first element in data.
                JOINPOS:        list with the given data
                XYZWPR:         list with the POSITION values converted from JOINPOS.
        """
        return self.set_check_pos_reg(0, 'joint', vals, ext_ang)

    
#%%############################################################################
##########          FANUC RSI  (Remote  Sensor  Interface)         ############
# status, enable, disable
###############################################################################
    def rsi_is_enable(self)->(int, str, list):
        """ Get status of RSI, 1 (= enable) or 0 (= disable). """
        return self.get_var('$AVC_GRP[1].$AVC_MODE[1]', 'INTEGER')            
    
        
    def run_faroc_mover(self)->(int, str):
        """ Run the task 'FaRoC_MOVER' """
        task_name = 'FaRoC_MOVER'
        code, msg, _ = self.send_cmd(f'run_tsk:0:{len(task_name):02d}:{task_name}')
        return code, msg
    
    
    
#%%############################################################################
#
#
#           Class FaRoC_Writer extended FaRoC_Reader
#
#
#%%############################################################################
class FaRoC_Writer(FaRoC_Reader):
    def __init__(
        self,
        robot_ip :str = '127.0.0.1',         # ip address of fanuc controller
        port :int = 24087,                       # the port of KAREL program "FAROC_SERVER"
        byte_order = '<',                         # byte order to unpack binary data
        socket_timeout : int = 5,
        debug_mode : bool = False,
    ):
        """
        Parameters
        ----------
        socket_timeout : int, optional
            Socket timeout in seconds. The default is 5.
        debug_mode : bool, optional
            to print more infos. The default is False.
        """
        
        FaRoC_Reader.__init__(self, robot_ip, port, byte_order, socket_timeout, debug_mode)
        self.mode = "FaRoC_Writer"
        
        
#%%############################################################################
##########             Robot In & Out (I/O: RI & RO)                 ##########
# get & set RO
###############################################################################
    def set_rdo(self, rdo_nr:int, rdo_val) -> (int, str, list):
        """
        Set the value of a robot out (RO). TP -> MENU -> I/O -> Robot.
        Parameters
        ----------
        rdo_nr : int
            Number of the robot out.
        rdo_val : TYPE
            The new value to set. 1 or 0, True or False (for resp. ON & OFF)
        Returns
        -------
        (int, str, list) code, msg: see function send_cmd.
            data: list with the new value set in RO
        """
        assert rdo_nr in range(1,9), f'rdo_nr must be in range [1-8], got: {rdo_nr}'
        assert rdo_val in range(2), f'rdo_val must be [0-1] or [False-True], got: {rdo_val}'
        cmd = f'set_rdo:{rdo_nr}:{rdo_val:1}'
        return self.send_cmd(cmd, d_type='B')


    def gripper(self, rdo_val:bool) -> (int, str, list):
        """
        Opens/closes robot gripper.
        Parameters
        ----------
        rdo_val : bool
            True for "ON"", false for "OFF".
        Returns
        -------
        (int, str, list) see function set_rdo
        """
        assert hasattr(self, 'ee_DO_num'), "please use 'set_ee_do_num' to set the end effector DO number."
        return self.set_rdo(self.ee_DO_num, rdo_val)
          

    def set_ee_do_num(self, ee_do_num:int)->None:
        """ Set the number of end effector digital output. """
        assert ee_do_num in range(1,9), f'rdo_nr must be in range [1-8], got: {ee_do_num}'
        self.ee_DO_num = ee_do_num


#%%############################################################################
##########               FLAG Registers (I/O: Flag)               #############
# get & set
###############################################################################
    def set_flag(self, flag_nr:int, flag_val) -> (int, str, list):
        """
        Set the value of a FLAG register. TP -> MENU -> I/O -> Flag.
        Parameters
        ----------
        flag_nr : int
            Number of the robot flag.
        flag_val : int or bool
            The new value to set. 1 or 0, True or False (for resp. ON & OFF)
        Returns
        -------
        (int, str, list) code, msg: see function send_cmd.
            data: list with the new value set in FLAG[flag_nr]
        """
        assert flag_nr in range(1,1025), f'flag_nr must be in range [1-1024], got: {flag_nr}'
        assert flag_val in range(2), f'rdo_val must be [0-1] or [False-True], got: {flag_val}'
        cmd = f'st_flag:{flag_nr:4}:{flag_val:1}'
        return self.send_cmd(cmd, d_type='B')
    
    
#%%############################################################################
##########        Robot Variables incl. System Variables (SV)        ##########
# get & set variable from Type [REAL, INTEGER, SHORT, BYTE, BOOLEN, STRING]
# check KAREL TYPE of a variable
###############################################################################
    def set_var(self, var_name:str, k_type:str, value, prog_name:str='*SYSTEM*')->(int, str, list):
        """
        Sets the value of a system variable (SV).
        Parameters
        ----------
        var_name : str
            the Name of system variable(s). e.g.'$AP_PRC_DSBM[1]', '$PRO_CFG.$INS_PWR',
        k_type : str, optional
            KAREL type of the system variable(s), REAL, INTEGER, BOOLEAN or STRING. The default is 'REAL'.
        value: 
            the new value to put in the system variable.
        prog_name : str, optional
            the name of the program to get its variable value. The default is '*SYSTEM*'.
        Returns
        -------
        (int, str, list)
            code, msg: see function send_cmd.
            data: a list with the new value of SV.
        """
        d_type = KTYPE_2_DTYPE[k_type.upper()]
        val_str = f"{value}"
        assert len(val_str) < 100, f'length of var_str must be < 100, got: {len(val_str)}'
        if value == None:
            if d_type=='S':
                cmd = f'set_var:{d_type}:{len(var_name):03d}:{var_name}:{len(prog_name):02}:{prog_name}:{-1:02d}:{val_str}' 
            else:
                cmd = f'set_var:{d_type}:{len(var_name):03d}:{var_name}:{len(prog_name):02}:{prog_name}:{1:02d}:{0}'
        else:
            if d_type=='B':
                assert value in range(2), f'value must be in range [0-1], got: {value}'
                val_str = '1' if value==1 else '0'
            cmd = f'set_var:{d_type}:{len(var_name):03d}:{var_name}:{len(prog_name):02}:{prog_name}:{len(val_str):02d}:{val_str}' 
        
        return self.send_cmd(cmd, d_type)


    def set_user_fram(self, ufram_nr:int)->(int, str, list):
        assert ufram_nr in range(1,10) and type(ufram_nr) == int, f'ufram_nr must be in range [1-9], got: {ufram_nr}'
        return self.set_var('$MNUFRAMENUM[1]', 'BYTE', ufram_nr)
    
    def adopt_user_fram(self, ufram_nr:int)->(int, str, list):
        assert ufram_nr in range(1,10) and type(ufram_nr) == int, f'ufram_nr must be in range [1-9], got: {ufram_nr}'
        return self.send_cmd(f'apl_ufr:{ufram_nr:02}', d_type='I')
    
    def set_tool_fram(self, utool_nr:int)->(int, str, list):
        assert utool_nr in range(1,11) and type(utool_nr) == int, f'utool_nr must be in range [1-10], got: {utool_nr}'
        return self.set_var('$MNUTOOLNUM[1]', 'BYTE', utool_nr)
    
    def adopt_tool_fram(self, utool_nr:int)->(int, str, list):
        assert utool_nr in range(1,11) and type(utool_nr) == int, f'utool_nr must be in range [1-10], got: {utool_nr}'
        return self.send_cmd(f'apl_utl:{utool_nr:02}', d_type='I')


#%%############################################################################
##########                 USER FRAMES & TOOL FRAMES               ############
# get & set (setter in FaRoC_Writer)
###############################################################################
    def set_frame(self, frame_type:str, frame_nr:int, vals:list, config:str) -> (int, str, list):
        """
        Apply the specified pose and configuration to the specified user or tool frame.
        ----------
        frame_type : str
            'user' to set user framem 'tool' to set tool frame
        frame_nr : int
            number of the position register to set.
        vals : list
            point representation as list of xyzwpr.            
        config : str
            the configuration of pose, e.g.: 'FUT,0,0,0'
        Returns
        -------
        (int, str, list) 
            code, msg -> see function send_cmd.
            data:  LIST with the values just set, i.e.:
                'UTOOL' or 'UFRAME', configuration and xyzwpr.
        """
        assert frame_type in ['user', 'tool'], f"frame_type must be 'user' or 'tool', got: {frame_type}"        
        if frame_type == 'user':
            assert frame_nr in range(1,10), f"frame_nr must be in range [1-9], got: {frame_nr}"
        if frame_type == 'tool':
            assert frame_nr in range(1,11), f"frame_nr must be in range [1-10], got: {frame_nr}"
        assert len(vals) == 6, f"length of vals must be 6, got: {len(vals)}"

        cmd = f"st_fram:{frame_type[0]}:{frame_nr:02}:{config:25}"

        # prepare joint values
        for val in vals:
            val_str = f"{abs(val):09.4f}"
            sign = "+" if val >= 0 else "-"
            cmd += f":{sign}{val_str}"
        
        code, msg, data =  self.send_cmd(cmd, d_type='R')
        if code == SUCCESS_CODE:
            msg_data = msg.split('|') 
            data = [msg_data[1]] + [msg_data[2]] + data
            msg = msg_data[0]
        return code, msg, data
    
    
#%%############################################################################
##########               DATA Registers                           #############
# reset, set & get (for value & comment)
###############################################################################
    def set_reg(self, reg_nr:int, val=None, cmt:str=None, prec:int=6)->(int, str, list):
        """
        Set the value and/or comment of the DATA register number 'reg_nr'.
        Parameters
        ----------
        reg_nr : int
            Number of DATA register to change its value and/or comment.
        val : TYPE, optional
            Value to put in the DATA register. If None dont change it. The default is None.
        cmt : str, optional
            Comment to put. If None dont chang. The default is None.
        prec : int, optional
            the precision for rounding the value before sending it . The default is 6.
        Returns
        -------
        (int, str, list)
            code, msg: see function send_cmd.
            data: list with the new value set if val != None, otherwise with the comment
        """
        assert reg_nr in range(1,201), f'reg_nr must be in range [1-200], got: {reg_nr}.'
        assert val==None or type(val)==float or type(val)==int, f'val must be int, float or None, got: {type(val)}'
        assert val!=None or cmt!=None, 'value AND command are None. Nothing to do!'
        assert cmt==None or type(cmt)==str, f'cmt must be str or None, got: {type(cmt)}'
        
        cmd = 'set_reg:'
        if val != None:
            if type(val)== float:
                cmd += f'R:{reg_nr:03d}:' 
                val_str = f"{abs(val):.{prec}f}"
                if val >= 0:
                    val_str = "+" + val_str
                else:
                    val_str = "-" + val_str
            else: # int
                cmd += f'I:{reg_nr:03d}:'
                val_str = f"{abs(val)}"
                if val >= 0:
                    val_str = "+" + val_str
                else:
                    val_str = "-" + val_str

            cmd += f"{len(val_str):02d}:{val_str}:"
            
        else: # val == None
            cmd += f'X:{reg_nr:03d}:{-1:02d}::'
            
        if cmt != None:
            cmd += f"{len(cmt):02d}:{cmt}"
        else :
            cmd += f"{-1:02d}:"     # no comment to set
            
        if type(val) == float: 
            return self.send_cmd(cmd, d_type='R')   # set int value (and comment)
        if type(val) == int: 
            return self.send_cmd(cmd, d_type='I')   # set real value (and comment)
        return self.send_cmd(cmd, d_type='S')       # ONLY set comment
    
    
    def reset_reg(self, reg_nr:int)->(int, str, list):
        """
        Set the value of the DATA register number 'reg_nr' to 0 and the comment to ''.
        Parameters
        ----------
        reg_nr : int
            Number of DATA register to reset its value and comment..
        Returns
        -------
        (int, str, list) 
            code, msg: see function set_reg.
            data: list with the new value set in register.
        """
        return self.set_reg( reg_nr, val=0, cmt='')
        

#%%############################################################################
##########                  Robot String Registers (SR)              ##########
# get, set & reset (value & comment)
###############################################################################
    def set_str_reg(self, str_reg_nr:int, sr_str:str,)->(int, str, list):
        """
        Set a new string in a string register (SR).
        Parameters
        ----------
        str_reg_nr : int
            Number of string register to change its value.
        sr_str : str
            new string to put in the string register.
        Returns
        -------
        (int, str, list) 
            code, msg: see function send_cmd.
            data: a list with the new value (string)
        """
        cmd = f'st_sreg:{str_reg_nr:02d}:{len(sr_str):03d}:{sr_str}'
        return self.send_cmd(cmd, d_type='S')
    

    def set_str_reg_cmt(self, str_reg_nr:int, cmt_str:str,)->(int, str, list):
        """
        Set a new string as comment for a string register (SR).
        Parameters
        ----------
        str_reg_nr : int
            Number of string register to change its comment.
        cmt_str : str
            new string to put as comment.
        Returns
        -------
        (int, str, list) 
            code, msg: see function send_cmd.
            data: a list with the new comment (string)
        """
        cmd = f'st_scmt:{str_reg_nr:02d}:{len(cmt_str):02d}:{cmt_str}'
        return self.send_cmd(cmd, d_type='S')


    def set_str_reg_both(self, str_reg_nr:int, cmt_str:str, sr_str:str, show_detail:bool=False)->(int, str, list):
        """
        Set a new string in a string register (SR) and/or change its comment.
        ----------
        str_reg_nr : int
            Number of string register to change its value and/or comment.
        cmt_str : str
            new string to put as comment.
        sr_str : str
            new string to put as value for the SR.
        show_detail : bool, optional
            Specifies whether to show datails on the console. The default is False.
        Returns
        -------
        (int, str, list) 
            code, msg: see function send_cmd.
            data: list with 2 strings: vlaue and comment string set in SR.
        """
        data = []
        code, msg, data_ = self.set_str_reg(str_reg_nr, sr_str)
        if code != 0:
            print(f"Error while setting value in string register nr. [{str_reg_nr}]: {msg}")
            return code, msg, data_
        data.append(data_[0])
        
        code, msg, data_ = self.set_str_reg_cmt(str_reg_nr, cmt_str)
        if code != 0:
            print(f"Error while setting comment for string register nr. [{str_reg_nr}]: {msg}")
            return code, msg, data_
        data.append(data_[0])
        
        if show_detail:
            print(f"SR[{str_reg_nr}: {cmt_str}] = '{sr_str}'")
            
        return code, msg, data
    
    
    def reset_str_reg(self, lst:list=list(range(1,26)), show_detail:bool=False)->(int, str, list):
        """
        Clears value & comment for a list of string registers (SR).
        Parameters
        ----------
        lst : list, optional
            A list the the number of str. reg. to clears. The default is list(range(1,26)).
        show_detail : bool, optional
            Specifies whether to show datails on the console. The default is False.
        Returns
        -------
        (int, str, list)
            code, msg: see function send_cmd.
            data: list of lists. Each list has 2 strings: value and comment string set in SR
        """
        data = []
        for str_reg_nr in lst:
            code, msg, d = self.set_str_reg_both(str_reg_nr, '', '', show_detail)
            if code != 0: return code, msg, d
            data.append(d)
        return code, msg, data


#%%############################################################################
##########                  INIIT DATA CLIENT                   ###############
###############################################################################
    def set_data_clnt_param(self, sys_var_real:list, sys_var_int:list, sys_var_bool:list, clnt_nr:int, clnt_port:int, curjpos:bool=False, curpos:bool=False, show_detail:bool=False)->(int, str, str):
        """
        Sets the given data for the Data Client in the Robot's string registers. 
        If `curjpos` and/or `curpos` are required, they are placed at the beginning 
        of the dataset, followed by `sys_var_real`, `sys_var_int`, and at the end 'sys_var_bool'.
        Parameters
        ----------
        sys_var_real : list
            A list with the names of the system variables whose values are REAL.
        sys_var_int : list
            A list with the names of the system variables whose values are INTEGER.
        sys_var_bool : list
            A list with the names of the system variables whose values are BOOLEAN.
        curjpos : bool, optional
            Specifies whether `curjpos` should be sent. The default is False.
        curpos : bool, optional
            Specifies whether `curpos` should be sent. The default is False.
        show_detail : bool, optional
            Specifies whether to show datails on the console. The default is False.
        Returns
        -------
        (int, str, str)
            code, msg: see function send_cmd.
            header: header of the log file created via the UDP server.
        """
        if len(sys_var_real) + len(sys_var_int) + len(sys_var_bool) + (curjpos*6) + (curpos*6) > 32:
            msg = 'Error!!! Max 32 values can be sent!'
            return 1, msg, ''
        
        def set_sysvar_in_str_reg(str_reg_nr:int, sys_var_lst:list, d_type:str, show_detail:bool=False)->(int, str, int):
            """
            set the sys. var. in `sys_var_lst` in the robot string register starting at index `str_reg_nr`
            Parameters
            ----------
            str_reg_nr : int
                The number of robot's string register.
            sys_var_lst : list
                A list with the names of the system variables as str.
            d_type : str
                the type of the system variable(s), 'R', 'I', 'B', 'S' for REAL,
                INTEGER, BOOLEAN and STRING.
            show_detail : bool, optional
                Specifies whether to show datails on the console. The default is False.
            Returns
            -------
            (int, str, int)
                code, msg: see function send_cmd.
                sv_end: the number of the last string register, where data is set.
            """
            nr_sys_var = 0
            sv_str = ''
            sv_cmt_str = ''
            i = 0
            send_flag = False
            
            while i < len(sys_var_lst):
                sv = sys_var_lst[i]
                if len(sv_str) + len(sv) + 2 <= 115 and nr_sys_var <= 3:  # 126 = Maximum length that can be sent in one operation
                    sv_str += f'{sv} '
                    sv_cmt_str += f'_{len(sv):02d}'
                    nr_sys_var += 1
                    i += 1
                    
                else: send_flag = True
                    
                if  send_flag or i == len(sys_var_lst):
                    cmt_str = f'{d_type}_{nr_sys_var}{sv_cmt_str}'
                    code, msg, data = self.set_str_reg_both(str_reg_nr, cmt_str, sv_str[:-1], show_detail)
                    if code != 0: 
                        return code, msg, data
                    
                    sv_end = str_reg_nr
                    send_flag = False
                    str_reg_nr += 1
                    nr_sys_var = 0
                    sv_str = ''
                    sv_cmt_str = ''
            return 0, 'success', sv_end
        
        sv_start = 2
        sv_end = 1
        if len(sys_var_real) > 0:
            code, msg, sv_end = set_sysvar_in_str_reg(sv_start, sys_var_real, 'R', show_detail=show_detail)
            if code != 0: return code, msg, ''
        sv_end_r = sv_end
        
        if len(sys_var_int) > 0:
            sv_start_i = sv_end+1
            code, msg, sv_end = set_sysvar_in_str_reg(sv_start_i, sys_var_int, 'I', show_detail=show_detail)
            if code != 0: return code, msg, ''
        sv_end_i = sv_end
        
        if len(sys_var_bool) > 0:
            sv_start_b = sv_end+1
            code, msg, sv_end = set_sysvar_in_str_reg(sv_start_b, sys_var_bool, 'B', show_detail=show_detail)
            if code != 0: return code, msg, ''
            
        print('--------------------------------------------------------------')
        if len(sys_var_real) > 0:
            print(f'REAL    system variables are placed in string register: [{sv_start}]-[{sv_end_r}]')
            
        if len(sys_var_int) > 0:
            print(f'INTEGER system variables are placed in string register: [{sv_start_i}]-[{sv_end_i}]')
        
        if len(sys_var_bool) > 0:
            print(f'BOOLEAN system variables are placed in string register: [{sv_start_b}]-[{sv_end}]')
            
        print('--------------------------------------------------------------')
        
        # Set parameter in string register No. 1
        str_reg_nr = 1
        sv_str = f'{curjpos:d}_{curpos:d}_{sv_start:02d}_{sv_end:02d}_C{clnt_nr}_{clnt_port}'
        cmt_str = f'C{clnt_nr}_{clnt_port}'

        code, msg, _  = self.set_str_reg_both(str_reg_nr, cmt_str, sv_str, show_detail=True)
    
        def get_header(sys_var_real, sys_var_int, curjpos, curpos):
            header = 'ts '
            if curjpos: header += 'J1 J2 J3 J4 J5 J6 '
            if curpos: header += 'X Y Z W P R '
            for sv in sys_var_real + sys_var_int + sys_var_bool:
                header += f'{sv} '
            return header[:-1]
    
        header = get_header(sys_var_real, sys_var_int, curjpos, curpos)
        return code, msg, header
    
    
#%%############################################################################
##########               Robot Date & Time                           ##########
# get & set
###############################################################################
    def set_time(self, date_time:str)->(int, str, list):
        """
        Set the robot time
        Parameters
        ----------
        date_time : str
            date_time must be in the format: "2022.11.26 20:29:30"
            ATTENTION: sec must be in range [0-30]
        Returns
        -------
        (int, str, list) 
            code, msg: see function send_cmd.
            data: list with the time as INTEGER
        """
        date_str, time_str =  date_time.split(' ')
        year_s, month_s, day_s = date_str.split('.')
        hour_s, min_s, sec_s = time_str.split(':')
        
        year_i, month_i, day_i = int(year_s), int(month_s), int(day_s)
        hour_i, min_i, sec_i = int(hour_s), int(min_s), int(sec_s)
        
        assert month_i in range(1,13), f'sec must be in range [1-12], got: {month_i}'
        assert day_i in range(1,32), f'sec must be in range [1-31], got: {day_i}'
        
        assert sec_i in range(30), f'sec must be in range [0-29], got: {sec_i}'
        assert min_i in range(60), f'sec must be in range [0-59], got: {min_i}'
        assert hour_i in range(24), f'sec must be in range [0-23], got: {hour_i}'
        
        year_b = int( bin( year_i -1980 )[2:])
        month_b = int( bin( month_i )[2:])
        day_b = int( bin( day_i )[2:])
        hour_b = int( bin( hour_i )[2:])
        min_b = int( bin( min_i )[2:])
        sec_b = int( bin( sec_i )[2:])
        
        time_bin = f'{year_b:07}{month_b:04}{day_b:05}{hour_b:05}{min_b:06}{sec_b:05}'
        time_int = int(time_bin, 2)
        cmd = f'st_time:{time_int}'
        return self.send_cmd(cmd, d_type='I')
    
    
#%%############################################################################
##########               POSITION REGISTER PR[*]                  #############
# get type, is_reachable, joint_to_pos, get & set
###############################################################################
    def set_pos_reg(self, pos_reg_nr:int, point_type:str, vals:list, ext_ang=None, config=None) -> (int, str, list):
        """
        Set position values POSJOINT or XYZWPR in position register. if one value in vals is None, 
        the current value of this joint/coordinate is adopted. In case of 'pose'
        xyzwpr is included in val, but CONFIG will be adopted from robot's current pose.
        Parameters
        ----------
        pos_reg_nr : int
            number of the position register to set.
        point_type : str
            type of point representation, "joint" or "pose".
        vals : list
            point representation as list of [j1-j6] or [xyzwpr].            
        ext_ang : list, optional
            Extended Joint values, when available. The default is None.
        config : str (only for pose)
            the configuration of pose, e.g.: 'FUT,0,0,0'
        Returns
        -------
        (int, str, list)
            code, msg -> see function send_cmd.
            data:  LIST with is_reachable and 2 Lists.
                is_reachable:   bool (True or False) is the first element in data.
                1.st List:      list with the given data that is now in the PR.
                2.nd list:      list with data converted from the given data. joint <-> pose.
        """
        assert pos_reg_nr in range(1,101), f"position register number must be in range [1-100], got: {pos_reg_nr}"
        return self.set_check_pos_reg(pos_reg_nr, point_type, vals, ext_ang, config)

    
#%%############################################################################
##########          FANUC RSI  (Remote  Sensor  Interface)         ############
# status, enable, disable
###############################################################################
    def rsi_enable(self)->(int, str, list):
        """
        Enable RSI. Sets the system variable: '$AVC_GRP[1].$AVC_MODE[1]' to 1.
        Returns
        -------
        (int, str, list)
            code, msg -> see function send_cmd.
            data: list with the new value set in the system variable.
        """
        return self.set_var('$AVC_GRP[1].$AVC_MODE[1]', 'INTEGER', 1)
    

    def rsi_disable(self)->(int, str, list):
        """
        Disable RSI (no robot data will be streamed to device). Sets the system
        variable: '$AVC_GRP[1].$AVC_MODE[1]' to 0.
        Returns
        -------
        (int, str, list)
            code, msg -> see function send_cmd.
            data: list with the new value set in the system variable.
        """
        return self.set_var('$AVC_GRP[1].$AVC_MODE[1]', 'INTEGER', 0)
    
    
    
#%%############################################################################
##########            HOST CONFIGURATION, Server & Client          ############
# config
###############################################################################
    def set_prog_var(self, name_val_dic:dict, prog_name:str='*SYSTEM*') -> (int, str, list):
        data_ = []
        for var_name, val in name_val_dic.items():
            k_type = PYTHON_2_KTYPE[type(val)]
            code, msg, data = self.set_var(var_name, k_type, val, prog_name=prog_name)
            if code != SUCCESS_CODE: return code, msg, data_
            data_.append(f"{prog_name} -> {var_name}: {data[0]}")
        return code, msg, data_
        
    
    def config_host_server(self, tag_nr:int, port:int, comment:str=''):
        assert tag_nr in range(1,9), f'tag_nr must be in range[1-8], got: {tag_nr}'
        
        data_ = [f"Serve_Tag_Nr: {tag_nr}"]
        pre = f'$HOSTS_CFG[{tag_nr}].$'
        name_val_dic = {pre+'COMMENT': comment, pre+'SERVER_PORT':port, pre+'PROTOCOL':'SM', 
                        pre+'OPER':2, pre+'STATE':2}        # to define
        
        code, msg, data = self.set_prog_var(name_val_dic)
        if code != SUCCESS_CODE: return code, msg, data_
        data_ += data
        
        name_val_dic = {pre+'OPER':3, pre+'STATE':3}        # to start
        code, msg, data = self.set_prog_var(name_val_dic)
        if code != SUCCESS_CODE: return code, msg, data_
        data_ += data
        msg = 'Please restart Fanuc controller to apply the changes!'
        print(msg)
        return code, msg, data_
    
    
    def config_host_client(self, tag_nr:int, host_ip:str, port:int, comment:str='', use_udp:bool=True) -> (int, str, list):
        assert tag_nr in range(1,9), f'tag_nr must be in range[1-8], got: {tag_nr}'
        
        data_ = [f"Client_Tag_Nr: {tag_nr}"]
        pre = f'$HOSTC_CFG[{tag_nr}].$'
        name_val_dic = {pre+'COMMENT': comment, pre+'SERVER_PORT':port, pre+'PROTOCOL':'SM', 
                        pre+'STRT_REMOTE':host_ip, pre+'USE_UDP':use_udp,
                        pre+'OPER':2, pre+'STATE':2}        # to define
        
        code, msg, data = self.set_prog_var(name_val_dic)
        if code != SUCCESS_CODE: return code, msg, data_
        data_ += data
        
        name_val_dic = {pre+'OPER':3, pre+'STATE':3}        # to start
        code, msg, data = self.set_prog_var(name_val_dic)
        if code != SUCCESS_CODE: return code, msg, data_
        data_ += data
        msg = 'Please restart Fanuc controller to apply the changes!'
        print(msg)
        return code, msg, data_
    

#%%############################################################################
#
#
#           Class FaRoC_Mover extended FaRoC_Writer
#
#
#%%############################################################################
class FaRoC_Mover(FaRoC_Writer):
    def __init__(
        self,
        robot_ip :str = '127.0.0.1',         # ip address of fanuc controller
        port :int = 24088,                       # the port of KAREL program "FAROC_SERVER"
        byte_order = '<',                         # byte order to unpack binary data
        socket_timeout : int = 30,
        debug_mode : bool = False,
    ):
        """
        Parameters
        ----------
        socket_timeout : int, optional
            Socket timeout in seconds. The default is 30.
            Increase this value if your method should use the KAREL routine RUN.
        debug_mode : bool, optional
            to print more infos. The default is False.
        """
        
        FaRoC_Writer.__init__(self, robot_ip, port, byte_order, socket_timeout, debug_mode)
        self.mode = "FaRoC_Mover"
        self.port = 24088   # the port of KAREL program "FAROC_MOVER"
        
        
#%%############################################################################
##########                      ROBOT MOVE                         ############
# move (j1-j9 or xyzwpr)
# chang_joint:      change one or more joints stepwise
# chang_position:   change one or more pose coordinates stepwise
###############################################################################
    def move(self, point_type:str, vals:list, ext_ang=None, velocity:int=10, 
             acceleration:int=10, cnt_val:int=100, linear:bool=False, 
             block_sock:bool=True, config:str=None) -> (int, str, list):
        """
        move the robot in linaer (L) or joint (J) mode. 

        Parameters
        ----------
        point_type : str
            type of point representation, "joint" or "pose".
        vals : list
            point representation as list of [j1-j6] or [xyzwpr].
            if one value in vals is None, this joint/coordinate will not be change.
            (( KAREL will placed this values in position register PR[81] )).
        ext_ang : TYPE, optional
            Extended Joint values, when available. The default is None.
        velocity : int, optional
            velocity parameter to set. Percentage for J or mm/sec for L. The default is 10.
            (( KAREL will placed this value in register R[81] )).
        acceleration : int, optional
            acceleration parameter to set. The default is 10. 
            (( KAREL will placed this value in register R[82] )).
        cnt_val : int, optional
            CNT parameter to set. The default is 100. 
            (( KAREL will placed this value in register R[83] )).
        linear : bool, optional
            True for LINEAR movement (L), False for JOINT movement (J). The default is False.
        block_sock : bool, optional
            True to block the socket until the movement is finished. The default is True.
        config : str, optional
            pose configuration. Only in case of 'pose'. e.g.: 'F U T, 0, 0, 0' or 'N U T, 0, 0, 0'.
        Returns
        -------
        (int, str, list) 
            code, msg: see function send_cmd.
            data: list contains the (joint) position when the data was sent.
        """
        assert point_type in ['joint', 'pose'], f"point_type must be 'joint' or 'pose', got: {point_type}"
        assert  len(vals) == 6, f"length of vals must be 6, got: {len(vals)}"
        assert ext_ang == None or len(ext_ang)==3, f"ext_ang must have the length 3 or be None, got: {ext_ang}"
        assert linear in range(2), f"linear must be boolean or in range [0-1], got: {linear}"
        assert block_sock in range(2), f"block_sock must be boolean or in range [0-1], got: {block_sock}"
        
        # prepare velocity.
        # format: aaaa, e.g.: 0001, 0020, 3000 
        velocity = int(velocity)
        velocity = f"{velocity:04}"
        
        # prepare acceleration.
        # format: aaaa, e.g.: 0001, 0020, 0100 
        acceleration = int(acceleration)
        acceleration = f"{acceleration:04}"

        # prepare CNT value
        # format: aaa, e.g.: 001, 020, 100
        cnt_val = int(cnt_val)
        assert 0 <= cnt_val <= 100, "Incorrect CNT value."
        cnt_val = f"{cnt_val:03}"
      
        mtn_type = 'L' if linear else 'J'
        
        if point_type == "joint":
            cmd = f"mov_jnt:{block_sock:1}:{mtn_type}:{velocity}:{acceleration}:{cnt_val}"
        elif point_type == "pose":
            cmd = f"mov_pos:{block_sock:1}:{mtn_type}:{velocity}:{acceleration}:{cnt_val}"
            cmd += f":{1}:{config:25}" if config else f":{0}"
            
        # prepare joint values
        for val in vals:
            if val == None: val = 9999      # to ignor it in KAREL
            val_str = f"{abs(val):09.4f}"
            sign = "+" if val >= 0 else "-"
            cmd += f":{sign}{val_str}"
        
        if point_type == "joint":
            if ext_ang != None:
                for val in ext_ang:
                    if val == None: val = 9999
                    val_str = f"{abs(val):09.4f}"
                    sign = "+" if val >= 0 else "-"
                    cmd += f":{sign}{val_str}"
            else:
                for _ in range(3):
                    vs = 9999               # to ignor it in KAREL
                    cmd += f":+{vs:09.4f}"
            
        return self.send_cmd(cmd, d_type='R')
    
    
    def move_L(self, point_type:str, vals:list, ext_ang=None, velocity:int=10, 
             acceleration:int=10, cnt_val:int=100, block_sock:bool=True, 
             config:str=None) -> (int, str, list):
        """
        move the robot in linaer (L) mode. 

        Parameters
        ----------
        point_type : str
            type of point representation, "joint" or "pose".
        vals : list
            point representation as list of [j1-j6] or [xyzwpr]
            if one value in vals is None, this joint/coordinate will not be change.
            (( KAREL will placed this values in position register PR[81] )).
        ext_ang : TYPE, optional
            Extended Joint values, when available. The default is None.
        velocity : int, optional
            velocity parameter to set. unit: mm/sec. The default is 10.
            (( KAREL will placed this value in register R[81] )).
        acceleration : int, optional
            acceleration parameter to set. The default is 10.
            (( KAREL will placed this value in register R[82] )).
        cnt_val : int, optional
            CNT parameter to set. The default is 100.
            (( KAREL will placed this value in register R[83] )).
        block_sock : bool, optional
            True to block the socket until the movement is finished. The default is True.
        config : str, optional
            pose configuration in case of 'pose'. e.g.: 'F U T, 0, 0, 0' or 'N U T, 0, 0, 0'.
        Returns
        -------
        (int, str, list)
            code, msg: see function send_cmd.
            data: list contains the (joint) position when the data was sent.
        """
        return self.move(point_type, vals, ext_ang, velocity, acceleration, 
                           cnt_val, True, block_sock, config)
    
    def move_J(self, point_type:str, vals:list, ext_ang=None, velocity:int=10, 
             acceleration:int=10, cnt_val:int=100, block_sock:bool=True, 
             config:str=None) -> (int, str, list):
        """
        move the robot in joint (J) mode. 

        Parameters
        ----------
        point_type : str
            type of point representation, "joint" or "pose".
        vals : list
            point representation as list of [j1-j6] or [xyzwpr]
            if one value in vals is None, this joint/coordinate will not be change.
            (( KAREL will placed this values in position register PR[81] )).
        ext_ang : TYPE, optional
            Extended Joint values, when available. The default is None.
        velocity : int, optional
            velocity parameter to set. unit: Percentage. The default is 10.
            (( KAREL will placed this value in register R[81] )).
        acceleration : int, optional
            acceleration parameter to set. The default is 10.
            (( KAREL will placed this value in register R[82] )).
        cnt_val : int, optional
            CNT parameter to set. The default is 100.
            (( KAREL will placed this value in register R[83] )).
        block_sock : bool, optional
            True to block the socket until the movement is finished. The default is True.
        config : str, optional
            pose configuration in case of 'pose'. e.g.: 'F U T, 0, 0, 0' or 'N U T, 0, 0, 0'.
        Returns
        -------
        (int, str, list)
            code, msg: see function send_cmd.
            list: contains the (joint) position when the data was sent.
        """
        return self.move(point_type, vals, ext_ang, velocity, acceleration, 
                           cnt_val, False, block_sock, config)
    
    
    def chang_joint(self, joint_lst:list, vel:int=50, acc:int=50, step:float=1,
                    linear:bool=False, block_sock:bool=True)->(int, str, list):
        """
        Changes one or more joints listed in 'joint_lst' stepwise.
        Parameters
        ----------
        joint_lst : list
            List of joint to move. e.g.: [2,4] to change joints: J2 & J4.
        vel : int, optional
            velocity parameter to set. Percentage for J or mm/sec for L. The default is 50.
        acc : int, optional
            acceleration parameter to set. The default is 50.
        step : float, optional
            specifies by how much the respective value is to be changed. The default is 1.
        linear : bool, optional
            True for LINEAR movement (L), False for JOINT movement (J). The default is False.
        block_sock : bool, optional
            True to block the socket until the movement is finished. The default is True.
        Returns
        -------
        (int, str, list)
            code, msg: see function send_cmd.
            data: list contains the (joint) position when the data was sent.
        """
        for j in joint_lst:
            assert j in range(1,7), f'joint nr. must be one in range [1-6], got: {j}'
            
        code, msg, data = self.get_curjpos(6)
        if code != 0: return code, msg
        for j in joint_lst:
            data[j-1] += step 
        return self.move(
                        "joint",
                        vals = data,
                        velocity = vel,
                        acceleration = acc,
                        cnt_val = 100,
                        linear = linear,
                        block_sock = block_sock)
        
    
    def chang_position(self, ch:str, vel:int=50, acc:int=50, step:float=1, 
                       linear:bool=False, block_sock:bool=True)->(int, str, list):
        """
        Changes one or more pose coordinates (x,y,z,w,p,r) stepwise.
        Parameters
        ----------
        ch : str
            contains the coordinates that should be changed, e.g.: 'xy' or 'zr'
        vel : int, optional
            velocity parameter to set. Percentage for J or mm/sec for L. The default is 50.
        acc : int, optional
            acceleration parameter to set. The default is 50.
        step : float, optional
            specifies by how much the respective value is to be changed. The default is 1.
        linear : bool, optional
            True for LINEAR movement (L), False for JOINT movement (J). The default is False.
        block_sock : bool, optional
            True to block the socket until the movement is finished. The default is True.
        Returns
        -------
        (int, str, list)
            code, msg: see function send_cmd.
            data: list contains the (joint) position when the data was sent.
        """
        assert ch.lower() in 'xyzwpr', f'channel(s) must be in "xyzwp", got: {ch}'
        code, msg, data = self.get_curpos()
        if code != 0: return code, msg
        data = data[1:] # only xyzwpr
        for c in ch:
            nr_ch = 'xyzwpr'.find(c.lower())
            data[nr_ch] += step 
        return self.move(
                        "pose",
                        vals = data,
                        velocity = vel,
                        acceleration = acc,
                        cnt_val = 100,
                        linear = linear,
                        block_sock = block_sock)
    
    
#%%############################################################################
##########           ROBOT TASK Status  & Program Type             ############
# run TP & KAREL program (with and without calling program being paused)
###############################################################################
    def call_prog(self, prog_name:str, start_at_line:int=0)->(int, str):
        """
        Calls an external KAREL or teach pendant program, beginning at a specified
        line. BUT the calling program is paused until the called program is terminated.
        User must confirm the execution on the TP.
        Parameters
        ----------
        prog_name : str
            External program name. TP or KAREL program.
        start_at_line: int
            ONLY for TP programs. Specifies the line at which to begin execution for a teach pendant program.
            0 or 1 is used for the beginning of the program. KAREL programs always execute
            at the beginning of the program.
        Returns
        -------
        (int, str) 
            code, msg: see function send_cmd.
        """
        cmd = f"cal_prg:{start_at_line:03}:{len(prog_name):02d}:{prog_name}"
        code, msg, _ = self.send_cmd(cmd)
        return code, msg
    
    
    def run_task(self, task_name:str, to_confirm:bool=True)->(int, str):
        """
        Run the Task 'task_name' parallel to the calling program. The calling 
        program is not paused.
        Parameters
        ----------
        task_name : str
            Name of Task to run.
        to_confirm : bool, optional
            IF true user must confirm the execution on the TP. The default is True.
        Returns
        -------
        (int, str) 
            code, msg: see function send_cmd.
        """
        conf = 1 if to_confirm else 0
        code, msg, _ = self.send_cmd(f'run_tsk:{conf}:{len(task_name):02d}:{task_name}')
        return code, msg


    def stop_task(self, task_name:str)->(int, str):
        """
        Stop the Task 'task_name'.
        Parameters
        ----------
        task_name : str
            Name of Task.
        Returns
        -------
        (int, str) 
            code, msg: see function send_cmd.
        """
        code, msg, _ =  self.send_cmd(f'stp_tsk:{len(task_name):02d}:{task_name}')
        return code, msg


