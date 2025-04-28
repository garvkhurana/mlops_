import sys
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import pandas as pd
from network_security.utils import load_object
import re
import socket
import requests
import whois
import datetime
import time
import pickle
import numpy as np
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class CustomData:

    def __init__(self,
                 having_IP_Address,
                 URL_Length,
                 Shortining_Service,
                 having_At_Symbol,
                 double_slash_redirecting,
                 Prefix_Suffix,
                 having_Sub_Domain,
                 SSLfinal_State,
                 Domain_registeration_length,
                 Favicon,
                 port,
                 HTTPS_token,
                 Request_URL,
                 URL_of_Anchor,
                 Links_in_tags,
                 SFH,
                 Submitting_to_email,
                 Abnormal_URL,
                 Redirect,
                 on_mouseover,
                 RightClick,
                 popUpWidnow,
                 Iframe,
                 age_of_domain,
                 DNSRecord,
                 web_traffic,
                 Page_Rank,
                 Google_Index,
                 Links_pointing_to_page,
                 Statistical_report
                 ):
        self.having_IP_Address = having_IP_Address
        self.URL_Length = URL_Length
        self.Shortining_Service = Shortining_Service
        self.having_At_Symbol = having_At_Symbol
        self.double_slash_redirecting = double_slash_redirecting
        self.Prefix_Suffix = Prefix_Suffix
        self.having_Sub_Domain = having_Sub_Domain
        self.SSLfinal_State = SSLfinal_State
        self.Domain_registeration_length = Domain_registeration_length
        self.Favicon = Favicon
        self.port = port
        self.HTTPS_token = HTTPS_token
        self.Request_URL = Request_URL
        self.URL_of_Anchor = URL_of_Anchor
        self.Links_in_tags = Links_in_tags
        self.SFH = SFH
        self.Submitting_to_email = Submitting_to_email
        self.Abnormal_URL = Abnormal_URL
        self.Redirect = Redirect
        self.on_mouseover = on_mouseover
        self.RightClick = RightClick
        self.popUpWidnow = popUpWidnow
        self.Iframe = Iframe
        self.age_of_domain = age_of_domain
        self.DNSRecord = DNSRecord
        self.web_traffic = web_traffic
        self.Page_Rank = Page_Rank
        self.Google_Index = Google_Index
        self.Links_pointing_to_page = Links_pointing_to_page
        self.Statistical_report = Statistical_report

    def get_pandas_dataframe(self):
        try:
            data_dict = {
                "having_IP_Address": [self.having_IP_Address],
                "URL_Length": [self.URL_Length],
                "Shortining_Service": [self.Shortining_Service],
                "having_At_Symbol": [self.having_At_Symbol],
                "double_slash_redirecting": [self.double_slash_redirecting],
                "Prefix_Suffix": [self.Prefix_Suffix],
                "having_Sub_Domain": [self.having_Sub_Domain],
                "SSLfinal_State": [self.SSLfinal_State],
                "Domain_registeration_length": [self.Domain_registeration_length],
                "Favicon": [self.Favicon],
                "port": [self.port],
                "HTTPS_token": [self.HTTPS_token],
                "Request_URL": [self.Request_URL],
                "URL_of_Anchor": [self.URL_of_Anchor],
                "Links_in_tags": [self.Links_in_tags],
                "SFH": [self.SFH],
                "Submitting_to_email": [self.Submitting_to_email],
                "Abnormal_URL": [self.Abnormal_URL],
                "Redirect": [self.Redirect],
                "on_mouseover": [self.on_mouseover],
                "RightClick": [self.RightClick],
                "popUpWidnow": [self.popUpWidnow],
                "Iframe": [self.Iframe],
                "age_of_domain": [self.age_of_domain],
                "DNSRecord": [self.DNSRecord],
                "web_traffic": [self.web_traffic],
                "Page_Rank": [self.Page_Rank],
                "Google_Index": [self.Google_Index],
                "Links_pointing_to_page": [self.Links_pointing_to_page],
                "Statistical_report": [self.Statistical_report]
            }
            return pd.DataFrame(data_dict)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

class PredictionPipeline:
   try: 
    def __init__(self):
        self.model_path='C:\Users\garvk\Desktop\project\1st_end_to_end_using_mlops\artifacts\best_model.pkl' 
        self.scaler_path='C:\Users\garvk\Desktop\project\1st_end_to_end_using_mlops\artifacts\scaler.pkl'   

        self.model=load_object(self.model_path)
        self.scaler=load_object(self.scaler_path)


    def model_prediction(self,features):
        data_scaled = self.scaler.transform(features)
        preds = self.model.predict(data_scaled)
        return preds    

   except Exception as e:
       raise NetworkSecurityException(e,sys) 



class URLAnalyzer:
    def __init__(self, model_path="artifacts/model.pkl", scaler_path="artifacts/scaler.pkl"):
        self.model = pickle.load(open(model_path, "rb"))
        self.scaler = pickle.load(open(scaler_path, "rb"))

    def fetch_url_content(self, url):
        try:
            response = requests.get(url, timeout=5)
            return response
        except Exception:
            return None

    def having_IP_Address(self, url):
        try:
            ip = re.findall(r'\d+\.\d+\.\d+\.\d+', url)
            return -1 if ip else 1
        except:
            return 1

    def URL_Length(self, url):
        return -1 if len(url) >= 75 else (0 if len(url) >= 54 else 1)

    def Shortining_Service(self, url):
        shorteners = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|tinyurl"
        return -1 if re.search(shorteners, url) else 1

    def having_At_Symbol(self, url):
        return -1 if "@" in url else 1

    def double_slash_redirecting(self, url):
        last_double_slash = url.rfind("//")
        return -1 if last_double_slash > 6 else 1

    def Prefix_Suffix(self, url):
        domain = urlparse(url).netloc
        return -1 if '-' in domain else 1

    def having_Sub_Domain(self, url):
        domain = urlparse(url).netloc
        if domain.count('.') > 3:
            return -1
        elif domain.count('.') == 3:
            return 0
        else:
            return 1

    def SSLfinal_State(self, url):
        try:
            if urlparse(url).scheme == "https":
                return 1
            else:
                return -1
        except:
            return -1

    def Domain_registeration_length(self, url):
        try:
            domain_info = whois.whois(url)
            expiration_date = domain_info.expiration_date
            creation_date = domain_info.creation_date
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            age = (expiration_date - creation_date).days
            return 1 if age >= 365 else -1
        except:
            return -1

    def Favicon(self, response, domain):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            for head in soup.find_all('head'):
                for link in head.find_all('link', href=True):
                    if domain not in link['href']:
                        return -1
            return 1
        except:
            return 1

    def port(self, url):
        try:
            domain = urlparse(url).netloc
            port = socket.getservbyport(443)
            return 1
        except:
            return -1

    def HTTPS_token(self, url):
        domain = urlparse(url).netloc
        return -1 if "https" in domain else 1

    def Request_URL(self, response, domain):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            total = 0
            safe = 0
            for img in soup.find_all('img', src=True):
                total += 1
                if domain in img['src'] or img['src'].startswith('/'):
                    safe += 1
            return 1 if safe / total >= 0.5 else -1
        except:
            return 1

    def URL_of_Anchor(self, response, domain):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            total = 0
            unsafe = 0
            for a in soup.find_all('a', href=True):
                total += 1
                if '#' in a['href'] or 'javascript' in a['href'].lower() or domain not in a['href']:
                    unsafe += 1
            return 1 if unsafe / total < 0.3 else -1
        except:
            return 1

    def Links_in_tags(self, response, domain):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            tags = soup.find_all(['meta', 'script', 'link'])
            total = len(tags)
            unsafe = 0
            for tag in tags:
                if tag.has_attr('href') and domain not in tag['href']:
                    unsafe += 1
            return 1 if unsafe / total < 0.3 else -1
        except:
            return 1

    def SFH(self, response):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            forms = soup.find_all('form', action=True)
            for form in forms:
                if form['action'] == "" or "about:blank" in form['action']:
                    return -1
            return 1
        except:
            return 1

    def Submitting_to_email(self, response):
        try:
            if "mailto:" in str(response.content):
                return -1
            else:
                return 1
        except:
            return 1

    def Abnormal_URL(self, url):
        try:
            domain = urlparse(url).netloc
            whois_info = whois.whois(domain)
            if whois_info is None:
                return -1
            else:
                return 1
        except:
            return -1

    def Redirect(self, response):
        try:
            if len(response.history) <= 1:
                return 1
            elif len(response.history) <= 4:
                return 0
            else:
                return -1
        except:
            return 1

    def on_mouseover(self, response):
        try:
            if re.findall("<script>.+onmouseover.+</script>", str(response.content)):
                return -1
            else:
                return 1
        except:
            return 1

    def RightClick(self, response):
        try:
            if re.findall(r"event.button ?== ?2", str(response.content)):
                return -1
            else:
                return 1
        except:
            return 1

    def popUpWidnow(self, response):
        try:
            if re.findall(r"alert\(", str(response.content)):
                return -1
            else:
                return 1
        except:
            return 1

    def Iframe(self, response):
        try:
            if re.findall(r"<iframe>", str(response.content)):
                return -1
            else:
                return 1
        except:
            return 1

    def age_of_domain(self, url):
        try:
            domain_info = whois.whois(url)
            creation_date = domain_info.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            age = (datetime.datetime.now() - creation_date).days
            return 1 if age >= 180 else -1
        except:
            return -1

    def DNSRecord(self, url):
        try:
            domain = urlparse(url).netloc
            socket.gethostbyname(domain)
            return 1
        except:
            return -1

    def web_traffic(self, url):
        try:
            return 1
        except:
            return -1

    def Page_Rank(self, url):
        try:
            return 1
        except:
            return -1

    def Google_Index(self, url):
        try:
            return 1
        except:
            return -1

    def Links_pointing_to_page(self, response):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            return -1 if len(links) < 2 else 1
        except:
            return 1

    def Statistical_report(self, url):
        try:
            return 1
        except:
            return -1

    def extract_features(self, url):
        features = []
        domain = urlparse(url).netloc
        response = self.fetch_url_content(url)
        
        features.append(self.having_IP_Address(url))
        features.append(self.URL_Length(url))
        features.append(self.Shortining_Service(url))
        features.append(self.having_At_Symbol(url))
        features.append(self.double_slash_redirecting(url))
        features.append(self.Prefix_Suffix(url))
        features.append(self.having_Sub_Domain(url))
        features.append(self.SSLfinal_State(url))
        features.append(self.Domain_registeration_length(url))
        features.append(self.Favicon(response, domain))
        features.append(self.port(url))
        features.append(self.HTTPS_token(url))
        features.append(self.Request_URL(response, domain))
        features.append(self.URL_of_Anchor(response, domain))
        features.append(self.Links_in_tags(response, domain))
        features.append(self.SFH(response))
        features.append(self.Submitting_to_email(response))
        features.append(self.Abnormal_URL(url))
        features.append(self.Redirect(response))
        features.append(self.on_mouseover(response))
        features.append(self.RightClick(response))
        features.append(self.popUpWidnow(response))
        features.append(self.Iframe(response))
        features.append(self.age_of_domain(url))
        features.append(self.DNSRecord(url))
        features.append(self.web_traffic(url))
        features.append(self.Page_Rank(url))
        features.append(self.Google_Index(url))
        features.append(self.Links_pointing_to_page(response))
        features.append(self.Statistical_report(url))

        return np.array(features).reshape(1, -1)      



















