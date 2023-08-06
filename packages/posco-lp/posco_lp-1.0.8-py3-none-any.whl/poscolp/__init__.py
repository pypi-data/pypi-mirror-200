from .__version__ import __version__

import sys
import requests
import numpy as np
import pandas as pd
import pyautogui as pag
from datetime import datetime
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

class LP():
    def __init__(self, lp_id=None, lp_pw=None):
        """
        2023-03-30 V1.0.8, 김두환

        LP 크롤링을 위한 다양한 기능을 하나로 묶은 클래스입니다.
        2개의 생성자를 입력해(생략가능) 호출하면 LP 객체를 생성합니다.

        lp_id : (str) 관리자 권한이 있는 lp 아이디를 입력합니다.
        lp_pw : (str) lp 아이디에 맞는 비밀번호를 입력합니다.

        생성자 미입력해 호출하면 아이디와 비밀번호를 묻는 프롬프트창이 뜹니다.

        ※업데이트 이력
            - V1.0.8 : getSurveyAnswerList() 메소드 추가, 저장할 파일명에 확장자(xlsx) 누락 시 자동으로 확장자 입력되도록 변경
        """
        if lp_id is None or lp_pw is None:
            self.lp_id=pag.prompt("관리자 권한이 있는 LP 아이디를 입력해 주세요", "LP 아이디 입력")
            self.lp_pw=pag.prompt("LP 비밀번호를 입력해 주세요", "LP 비밀번호 입력")
        else:
            self.lp_id = lp_id
            self.lp_pw = lp_pw

        self.host = "https://lp.posco.co.kr"
        self.login_checked = False
        self.lp_session = requests.session()

        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        pd.set_option("mode.chained_assignment",  None)
        
    def _saveToExcel(self, df:pd.DataFrame, filename:str):
        if filename.split(".")[-1] != "xlsx":
            filename = filename + ".xlsx"
        df.to_excel(filename, index=False)

    def login(self):
        """
        lp에 로그인을 시도합니다. 별도의 파라미터는 없습니다.
        로그인에 성공하면 객체 내부에 requests 모듈의 세션 객체를 lp_session에 저장하게 됩니다.
        이후 lp_session을 이용해 세션을 유지한채로 크롤링을 시도하게 됩니다.
        """
        print("LP로그인 중...")
        url = "{}/S22/S22A10/member/login/ajax/login.do".format(self.host)
        header = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
        }
        form_data = {
            "email": self.lp_id,
            "password": self.lp_pw,
            "instructor": "false",
            "redirectUrl": ""
        }
        res = self.lp_session.post(url, data=form_data, headers=header, verify=False)
        data = res.json()
        if "statusCode" in data["messageMap"] and data["messageMap"]["statusCode"] == 1:
            url_admin = "{}/S22/S22A10/admin/changeAdminGrp.do".format(self.host)
            form_data_admin = {
                "menuId": "",
                "menuStep": "",
                "pMenuId": "",
                "choiceGrpId": "C_00000001"
            }
            self.lp_session.post(url_admin, form_data_admin, headers=header, verify=False)
            print("LP로그인에 성공하였습니다.")
            self.login_checked = True
        else:
            print("{} 오류 : LP로그인에 실패하였습니다. 아래 LP 메시지 코드를 확인해 보세요.".format(sys._getframe().f_code.co_name))
            print(res.text)
            self.login_checked = False

    def getCompanyList(self, company_cate="그룹사", filename_to_save=""):
        """
        LP에 등록된 그룹사/협력사/해외법인의 정보를 추출해 DataFrame으로 리턴해 줍니다.
        긁어오는 정보 : 회사명, 대표자명, 주소, 우편번호, 사업자번호, 대표 전화번호, 회사코드(company_code), LP에 등록된 직원계정 수, LP등록일시, 수정일시
        
        ※파라미터

        company_cate : (str) 그룹사, 협력사, 해외법인 중 하나를 입력. 기본값은 그룹사

        filename_to_save : (str) 결과값을 엑셀 파일로 저장하고 싶다면 저장할 파일명을 입력합니다.

        ※리턴 : pandas DataFrame
        """
        if self.login_checked == False:
            self.login()

        url = "{}/S22/S22A10/admin/company/ajax/companyList.do".format(self.host)
        if company_cate == "그룹사":
            searchType = "0002"
        elif company_cate == "협력사":
            searchType = "0004"
        elif company_cate == "해외법인":
            searchType = "0003"
        else:
            print("{} 오류 : company_cate 파라미터를 잘못 입력하였습니다.".format(sys._getframe().f_code.co_name))
            return False

        form_data = {
            "searchType" : searchType
        }
        res = self.lp_session.post(url, data=form_data, verify=False)
        data = res.json()
        df = pd.DataFrame(data["data"])
        kv_dict = {
            "compName" : "회사명",
            "president" : "대표자명",
            "addr" : "주소",
            "postCode" : "우편번호",
            "compRegNo" : "사업자번호",
            "telNo" : "대표전화번호",
            "compCode" : "회사코드(company_code)",
            "memberCount" : "직원계정수",
            "billCdNm" : "그룹웨어",
            "regDtm" : "LP등록일시",
            "chgDtm" : "수정일시"
        }
        df = df[kv_dict.keys()]
        df.rename(columns=kv_dict, inplace=True)
        if len(filename_to_save) > 0:
            self._saveToExcel(df, filename_to_save)

        return df

    def getUserList(self, search_text="", search_type="NAME", company_code="0", filename_to_save=""):
        """
        LP에서 특정 사용자(교육생)를 검색한 결과를 DataFrame으로 리턴해 줍니다.

        ※파라미터
        search_text : (str) 검색어를 입력합니다. 아무값도 입력하지 않으면 모든 검색결과를 다 출력해 줍니다. (기본값 NONE)

        search_type : (str) 검색조건입니다. 아래 3가지 중 하나를 입력하면 됩니다.
            - NAME : 이름으로 검색 (기본값)
            - ID : LP아이디로 검색
            - NUM : 직번으로 검색

        company_code : (str) 회사코드를 입력하면 필터링해 검색해 줍니다.
            - 회사 코드는 getCompanyList() 메서드를 통해 받을 수 있습니다.

        filename_to_save : (str) 결과값을 엑셀 파일로 저장하고 싶다면 저장할 파일명을 입력합니다.

        ※리턴 : pandas DataFrame
        """
        if self.login_checked == False:
            self.login()

        if search_text == "":
            search_text = pag.prompt("검색어를 입력해 주세요. 아무 값도 입력하지 않을 경우 회사 코드를 기준으로 전직원 정보를 가져옵니다.")
        
        if search_text is None:
            search_text = ""
            if company_code == "":
                company_code = "0"

        form_data_member = {
            "draw": "1",
            "start": "0",
            "length": "20000",
            "searchStayType": "N",
            "searchCompCodeText" : company_code,
            "searchMemberType": search_type,
            "searchMemberText": search_text
        }
        headers_member = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ko,ko-KR;q=0.9,en;q=0.8",
            "call_type": "AJAX",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        url_member = "{}/S22/S22A10/admin/member/ajax/memberPageList.do".format(self.host)
        res = self.lp_session.post(url_member, data=form_data_member, headers=headers_member, verify=False)
        data = res.json()
        if len(data["data"]) == 0:
            print("검색어 '{}' → 검색 결과가 없습니다.".format(search_text))
            return False
        df = pd.DataFrame(data["data"])
        kv_dict = {
            "compName" : "회사명",
            "deptName" : "부서명",
            "userName" : "이름",
            "posiName" : "직급명",
            "jikchkName" : "직책명",
            "memberNo" : "직번",
            "retrFlag" : "재직여부",
            "email" : "이메일",
            "telNo" : "전화번호",
            "brthdy" : "생년월일",
            "compCode" : "회사코드(company_code)",
            "userId" : "LP관리ID",
            "regDtm" : "등록일",
            "chgDtm" : "수정일",
            "loginDtm" : "마지막 로그인"
        }
        keys_list = kv_dict.keys()
        df = df[keys_list]
        df.rename(columns=kv_dict, inplace=True)
        if len(filename_to_save) > 0:
            self._saveToExcel(df, filename_to_save)

        return df

    def getChaList(self, group_name="", search_text="", start_date="", end_date="", simple=True, filename_to_save=""):
        """
        차수 목록을 DataFrame으로 리턴해 줍니다.
        관리부서명, 시작일, 종료일, 검색어를 입력하면 조건에 맞춰 출력해 줍니다.
        
        ※파라미터

        group_name : (str) 담당부서명을 입력합니다. 미입력시 전체 부서를 대상으로 검색합니다.

        search_text : (str) 차수명 검색어를 입력합니다. 미입력시 전체 차수명을 대상으로 검색합니다.

        start_date : (str) 교육시작일을 yyyymmdd 형식으로 입력합니다. 미입력시 오늘 날짜를 기준으로 검색합니다.

        end_date : (str) 교육종료일을 yyyymmdd 형식으로 입력합니다. 미입력시 오늘 날짜를 기준으로 검색합니다.
        
        simple : (bool) False로 입력하면 LP에서 보내주는 정보 전체를 그대로 출력해 줍니다. 기본값은 True

        filename_to_save : (str) 결과값을 엑셀 파일로 저장하고 싶다면 저장할 파일명을 입력합니다.

        ※리턴 : pandas DataFrame
        """
        if self.login_checked == False:
            self.login()

        if len(start_date) == 0:
            start_date = datetime.strftime(datetime.now(), "%Y%m%d")

        if len(end_date) == 0:
            end_date = datetime.strftime(datetime.now(), "%Y%m%d")

        url = "{}/S22/S22A10/admin/course/ajax/courseCsPageList.do".format(self.host)
        header = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
        }
        form_data_curi = {
            "start": "0",
            "length": "1000", #가져올 데이터의 최대량
            "search[regex]": "false",
            "courseSeq":"",
            "eduStatusCode":"",
            "eduAreaCode":"",
            "keywordType": "C",
            "keyword": search_text,
            "eduMngtDeptName": group_name,
            "subManagerName":"",
            "MyManager":"",
            "eduPeriodFlag": "C",
            "searchStartDt": start_date,
            "searchEndDt": end_date
        }
        res = self.lp_session.post(url, form_data_curi, headers = header, verify=False)
        data = res.json()
        if len(data["data"]) == 0:
            print("검색 결과가 없습니다.")
            return False

        df = pd.DataFrame(data["data"])

        if simple == True:
            kv_dict = {
                "courseCsName" : "차수명",
                "courseSeq" : "과정ID",
                "courseCsSeq" : "차수ID",
                "eduMngtDeptName" : "담당부서",
                "managerName" : "담당자",
                "eduStartDt" : "교육시작일",
                "eduEndDt" : "교육종료일",
                "studentCnt" : "정원",
                "studentCntApply" : "신청",
                "studentCntConfirm" : "확정",
                "studentCntWait" : "대기",
                "studentCntComplete" : "수료"
            }
            df = df[kv_dict.keys()]
            df.rename(columns=kv_dict, inplace=True)

        if len(filename_to_save) > 0:
            self._saveToExcel(df, filename_to_save)

        return df

    def getChaDetail(self, courseId:str, chaId:str):
        """
        과정ID, 차수ID를 입력하면 해당 차수의 상세 정보를 json으로 리턴해 줍니다.
        
        ※파라미터

        courseId : (str) 필수. 과정ID 값을 입력합니다.

        chaId : (str) 필수. 차수ID값을 입력합니다.

        과정 아이디와 차수 아이디는 getChaList() 메서드를 통해 얻을 수 있습니다.

        ※리턴 : dict(json)
        """
        url = "{}/S22/S22A10/admin/course/ajax/getCourseCsView.do".format(self.host)
        form_data = {
            "courseSeq": courseId,
            "courseCsSeq": chaId
        }
        res = self.lp_session.post(url, data=form_data, verify=False)
        
        return res.json()["courseCs"]

    def getStudentRegisterList(self, courseId:str, chaId:str, filename_to_save=""):
        """
        과정ID, 차수ID를 입력하면 해당 차수에 등록된 교육생 정보를 DataFrame으로 리턴해 줍니다.
        
        ※파라미터

        courseId : (str) 필수. 과정ID 값을 입력합니다.

        chaId : (str) 필수. 차수ID값을 입력합니다.

        filename_to_save : (str) 결과값을 엑셀 파일로 저장하고 싶다면 저장할 파일명을 입력합니다.

        과정 아이디와 차수 아이디는 getChaList() 메서드를 통해 얻을 수 있습니다.

        ※리턴 : pandas DataFrame
        """
        url = "{}/S22/S22A10/admin/course/ajax/courseRegisterStudentList.do".format(self.host)
        form_data = {
            "start": "0",
            "length": "1000",
            "search[regex]": "false",
            "courseSeq": courseId,
            "courseCsSeq": chaId,
            "keywordType": "NAME",
            "showOthGrpYn": "Y"
        }
        res = self.lp_session.post(url, data=form_data, verify=False)
        data = res.json()
        if len(data["data"]) == 0:
            print("검색 결과가 없습니다.")
            return False

        df = pd.DataFrame(data["data"])
        kv_dict = {
            "courseName" : "과정",
            "courseCsName" : "차수",
            "registerStatName" : "상태",
            "userName" : "이름",
            "memberNo" : "직번",
            "userId" : "LP관리ID",
            "compName" : "회사",
            "deptName" : "부서",
            "posiName" : "직급",
            "juminNo" : "생년월일",
            "email" : "이메일"
        }
        df = df[kv_dict.keys()]
        df.rename(columns=kv_dict, inplace=True)
        df["생년월일"] = df["생년월일"].str[-8:]

        if len(filename_to_save) > 0:
            self._saveToExcel(df, filename_to_save)

        return df

    def getStudentPassedList(self, courseId:str, chaId:str, filename_to_save=""):
        """
        과정ID, 차수ID를 입력하면 해당 차수의 수료자 정보를 DataFrame으로 리턴해 줍니다.
        
        ※파라미터

        courseId : (str) 필수. 과정ID 값을 입력합니다.

        chaId : (str) 필수. 차수ID값을 입력합니다.

        filename_to_save : (str) 결과값을 엑셀 파일로 저장하고 싶다면 저장할 파일명을 입력합니다.

        과정 아이디와 차수 아이디는 getChaList() 메서드를 통해 얻을 수 있습니다.

        ※리턴 : pandas DataFrame
        """
        url = "{}/S22/S22A10/admin/course/groupCourseEduPass.do".format(self.host)
        form_data = {
            "courseSeq": courseId,
            "courseCsSeq": chaId,
            "tabType": "CP14"
        }
        res = self.lp_session.post(url, data=form_data, verify=False)
        html = "<table><thead><tr><th></th>" + res.text.split('<table class="brd_list" style="width : 100%;">\r\n\t    <thead>\r\n\t     <tr>\r\n\t       <th rowspan="4"><input type="checkbox" id="chkStuUserAll" name="chkStuUserAll" /></th>\r\n\t')[1].split("</tbody>\r\n\t  </table>\r\n\t  </div>\r\n")[0] + "</tbody></table>"
        result = ""
        for notation in html.split("-->"):
            result += notation.split("<!--")[0]
        soup = BeautifulSoup(result, "html.parser")
        result = "<table>"
        for idx, item in enumerate(soup.select("tr")):
            if idx > 3:
                result += str(item)
        result += "</table>"
        df = pd.read_html(result)[0]
        try:
            df = df[[1, 2, 3, 4, 5, 6, 7]]
            df.rename(columns={
                1 : "이름",
                2 : "직번",
                3 : "회사",
                4 : "부서",
                5 : "직급",
                6 : "수료여부",
                7 : "이수시간"
            }, inplace=True)
        except:
            df = df[[1, 2, 3, 4, 5, 6]]
            df.rename(columns={
                1 : "이름",
                2 : "직번",
                3 : "회사",
                4 : "부서",
                5 : "직급",
                6 : "수료여부"
            }, inplace=True)
            df["이수시간"] = None
        c_info = self.getChaDetail(courseId, chaId)
        df["차수명"] = c_info["courseCsName"]
        df.drop(index=df[(df["직번"].isnull())].index, inplace=True)
        df["직번"] = df["직번"].astype("int")
        df.reset_index(inplace=True, drop=True)

        if len(filename_to_save) > 0:
            self._saveToExcel(df, filename_to_save)

        return df

    def getSurveyMeanScore(self, courseId:str, chaId:str, filename_to_save=""):
        """
        과정ID, 차수ID를 입력하면 해당 차수의 설문지 개수, 응답자수, 설문별 평균값을 출력해 줍니다.
        
        ※파라미터

        courseId : (str) 필수. 과정ID 값을 입력합니다.

        chaId : (str) 필수. 차수ID값을 입력합니다.

        filename_to_save : (str) 결과값을 엑셀 파일로 저장하고 싶다면 저장할 파일명을 입력합니다.

        과정 아이디와 차수 아이디는 getChaList() 메서드를 통해 얻을 수 있습니다.

        ※리턴 : pandas DataFrame
        """
        url1 = "{}/S22/S22A10/admin/course/ajax/groupStudyItemSurveyList.do".format(self.host)
        url2 = "{}/S22/S22A10/admin/course/popup/groupStudyItemSurveyForm.do".format(self.host)
        form_data1 = {
            "draw": "1",
            "start": "0",
            "length": "25",
            "search[value]": "",
            "search[regex]": "false",
            "searchStudyItemSeq": "",
            "searchStudyItemTypeCode": "POLL",
            "searchExamPaperTypeCode": "POLL",
            "searchUseFlag": "Y"
        }
        form_data2 = {
            "person": "N",
            "qustKindCode": "POLL",
            "isAdmin": "Y"
        }

        form_data1["courseSeq"] = courseId
        form_data1["courseCsSeq"] = chaId
        form_data2["courseSeq"] = courseId
        form_data2["courseCsSeq"] = chaId
        res = self.lp_session.post(url1, data=form_data1, verify=False)
        data = res.json()
        result = []
        for survey in data["data"]:
            form_data2["studyItemSeq"] = survey["studyItemSeq"]
            form_data2["examPaperSeq"] = survey["examPaperSeq"]
            res_detail = self.lp_session.post(url2, data=form_data2, verify=False)
            soup = BeautifulSoup(res_detail.text, "html.parser")

            cha_name = soup.select("table")[0].select("td")[1].select("span")[0].text.strip() #차수명
            period = soup.select("table")[0].select("td")[4].select("span")[0].text.strip() #설문기간
            survey_name = soup.select("table")[0].select("td")[5].select("span")[0].text.strip() #설문명
            target = soup.select("table")[0].select("td")[6].select("span")[0].text.strip() #대상자
            participants = int(soup.select("table")[0].select("td")[-1].select("span")[0].text.split("명")[0].strip())
            this_result = {
                "차수명" : cha_name,
                "설문명" : survey_name,
                "설문ID" : survey["studyItemSeq"],
                "설문지ID" : survey["examPaperSeq"],
                "설문기간" : period,
                "설문대상자" : target,
                "설문응답자" : participants
            }
            for item in soup.select("table")[1].select("td > div > span"):
                if item.text != "0":
                    this_result[item.parent.parent.parent.select("th")[0].text] = float(item.text)

            arr = np.array([float(x.text) for x in soup.select("table")[1].select("td > div > span") if x.text != "0"])
            mean = 0.
            if len(arr) > 0:
                mean = arr.mean()
            this_result["설문결과 평균"] = mean

            result.append(this_result)
        df = pd.DataFrame(result)

        if len(filename_to_save) > 0:
            self._saveToExcel(df, filename_to_save)

        return df

    def getSurveyAnswerList(self, courseId:str, chaId:str, filename_to_save=""):
        """
        과정ID, 차수ID를 입력하면 해당 차수의 설문 응답결과를 출력해 줍니다.
        
        ※파라미터

        courseId : (str) 필수. 과정ID 값을 입력합니다.

        chaId : (str) 필수. 차수ID값을 입력합니다.

        filename_to_save : (str) 결과값을 엑셀 파일로 저장하고 싶다면 저장할 파일명을 입력합니다.

        과정 아이디와 차수 아이디는 getChaList() 메서드를 통해 얻을 수 있습니다.

        ※리턴 : pandas DataFrame
        """
        url = "{}/S22/S22A10/admin/course/ajax/groupStudyItemDtlResultExcelDownload.do".format(self.host)
        form_data = {
            "courseSeq": courseId,
            "courseCsSeq": chaId,
            "searchType": "USER",
            "searchStudyItemTypeCode": "POLL",
            "searchExamPaperTypeCode": "POLL",
            "searchUseFlag": "Y",
            "person": "Y",
            "qustKindCode": "POLL",
            "isAdmin": "Y"
        }
        res = self.lp_session.post(url, data=form_data, verify=False)
        df = pd.read_excel(res.content)
        real_col = df.loc[0].to_dict()
        df.rename(columns=real_col, inplace=True)
        df.drop(index=[0, 1], inplace=True)
        df.reset_index(drop=True, inplace=True)
        if len(filename_to_save) > 0:
            self._saveToExcel(df, filename_to_save)

        return df        

    def getLectureRoomInfo(self, date:str, filename_to_save=""):
        """
        입력한 날짜(yyyymmdd)에 해당하는 강의실 예약정보를 DataFrame으로 리턴해 줍니다.
        
        ※파라미터

        date : (str) 필수. 날짜를 yyyymmdd 형식으로 입력합니다.

        filename_to_save : (str) 결과값을 엑셀 파일로 저장하고 싶다면 저장할 파일명을 입력합니다.

        ※리턴 : pandas DataFrame
        """
        date = "".join(char for char in date.strip() if char == " " or char.isalnum())
        if len(date) == 8:
            date = "{}.{}.{}".format(date[:4], date[4:6], date[6:])
        else:
            print("{} 오류 : 날짜 입력이 잘못되었습니다. 8자리 숫자를 정확히 넣어주세요.".format(sys._getframe().f_code.co_name))
            return False

        url = "{}/S22/S22A10/admin/support/ajax/getLectureroomCalendarList.do".format(self.host, verify=False)
        form_data = {
            "searchEduArea": "0001",
            "searchEduPlaceCode": "P1",
            "startDt": date,
            "endDt": date,
            "searchStartDt": date,
            "searchEndDt": date,
            "searchType": "REG_USER_NAME"
        }
        res = self.lp_session.post(url, data=form_data)
        df_src = pd.DataFrame(res.json()["lectureroomCalendarList"])

        kv_dict = {
            "deptName" : "예약자 부서",
            "eduPlaceName" : "건물명",
            "lectureroomNm" : "강의실명",
            "ho" : "호실",
            "userName" : "예약자",
            "eduName" : "교육명",
            "startTime" : "시작시간",
            "endTime" : "종료시간",
            "eduDts" : "일자"
        }
        df_src = df_src[kv_dict.keys()]
        df_src.rename(columns=kv_dict, inplace=True)

        new_result = []
        for item in df_src.iterrows():
            for idx, _ in enumerate(item[1]["예약자"].split("|")):
                new_result.append({
                    "예약자 부서" : item[1]["예약자 부서"].split("|")[idx],
                    "건물명" : item[1]["건물명"],
                    "강의실명" : item[1]["강의실명"],
                    "호실" : item[1]["호실"],
                    "예약자" : item[1]["예약자"].split("|")[idx],
                    "교육명" : item[1]["교육명"].split(",")[idx],
                    "시작시간" : item[1]["시작시간"].split(",")[idx],
                    "종료시간" : item[1]["종료시간"].split(",")[idx],
                    "일자" : date.replace(".", "")
                })
        df = pd.DataFrame(new_result)
        df = df[(df["예약자"] != "")]
        df.reset_index(drop=True, inplace=True)

        if len(filename_to_save) > 0:
            self._saveToExcel(df, filename_to_save)

        return df        

    def updateStudentToPassed(self, courseId:str, chaId:str):
        """
        과정ID, 차수ID를 입력하면 해당 차수의 수료조건에 해당되는 교육생들을 일괄 수료처리해 줍니다.
        
        ※파라미터

        courseId : (str) 필수. 과정ID 값을 입력합니다.

        chaId : (str) 필수. 차수ID값을 입력합니다.

        과정 아이디와 차수 아이디는 getChaList() 메서드를 통해 얻을 수 있습니다.

        ※리턴 : None
        """
        url = "{}/S22/S22A10/admin/course/groupCourseEduPass.do".format(self.host)
        form_data = {
            "courseSeq": courseId,
            "courseCsSeq": chaId,
            "tabType": "CP14"
        }
        res = self.lp_session.post(url, data=form_data, verify=False)
        html = "<table><thead><tr><th></th>" + res.text.split('<table class="brd_list" style="width : 100%;">\r\n\t    <thead>\r\n\t     <tr>\r\n\t       <th rowspan="4"><input type="checkbox" id="chkStuUserAll" name="chkStuUserAll" /></th>\r\n\t')[1].split("</tbody>\r\n\t  </table>\r\n\t  </div>\r\n")[0] + "</tbody></table>"
        result = ""
        for notation in html.split("-->"):
            result += notation.split("<!--")[0]
        soup = BeautifulSoup(result, "html.parser")
        student_list = []
        items = soup.select("tr")
        for item in items:
            try:
                student_list.append(item.select("td")[0].select("input")[0].attrs["value"])
            except:
                pass
        # return student_list, res
        url_update = "{}/S22/S22A10/admin/course/ajax/updateStudentEduPassStatGrpCs.do".format(self.host)
        form_data_update = {
            "courseSeq" : courseId,
            "courseCsSeq" : chaId,
            "passStatCode" : "N",
            "arrUserId[]" : student_list
        }
        res = self.lp_session.post(url_update, data=form_data_update, verify=False)
        if res.text == '{"data":1}':
            print("수료처리 완료")
        else:
            print("수료처리 실패!!!")

    def resetUserPassword(self, lp_user_id:str):
        """
        사용자의 LP관리ID(ex : 986669Y)를 입력하면 해당 사용자의 LP 비밀번호를 초기화해 줍니다.
        
        ※파라미터

        lp_user_id : (str) 필수. 사용자의 LP관리ID 값을 입력합니다.

        LP관리ID는 getStudentRegisterList() 혹은 getUserList() 메서드를 통해 얻을 수 있습니다.

        ※리턴 : None
        """
        url = "{}/S22/S22A10/admin/member/ajax/memberPwdUpdate.do".format(self.host)
        form_data = {
            "userIds[]": lp_user_id,
            "returnMessage": "show"
        }
        self.lp_session.post(url, data=form_data, verify=False)