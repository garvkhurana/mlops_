import sys
import pandas as pd
import numpy as np
import pickle
import re
import socket
import whois
import datetime
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from network_security.exception.exception import NetworkSecurityException
from network_security.utils import load_object

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
                 Statistical_report):
        
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
            data = {
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
            return pd.DataFrame(data)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

class PredictionPipeline:
    def __init__(self):
        try:
            self.model_path = r'artifacts\best_model.pkl'
            self.scaler_path = r'artifacts\scaler.pkl'

            self.model = load_object(self.model_path)
            self.scaler = load_object(self.scaler_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def predict(self, features):
        try:
            scaled_features = self.scaler.transform(features)
            prediction = self.model.predict(scaled_features)
            return prediction
        except Exception as e:
            raise NetworkSecurityException(e, sys)

class URLAnalyzer:
    def __init__(self):
        pass

    def fetch_response(self, url):
        try:
            return requests.get(url, timeout=5)
        except:
            return None

    def having_IP_Address(self, url):
        return -1 if re.findall(r'\d+\.\d+\.\d+\.\d+', url) else 1

    def URL_Length(self, url):
        return -1 if len(url) >= 75 else (0 if len(url) >= 54 else 1)

    def Shortining_Service(self, url):
        return -1 if re.search(r"(bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|tinyurl)", url) else 1

    def having_At_Symbol(self, url):
        return -1 if "@" in url else 1

    def double_slash_redirecting(self, url):
        return -1 if url.rfind("//") > 6 else 1

    def Prefix_Suffix(self, url):
        return -1 if '-' in urlparse(url).netloc else 1

    def having_Sub_Domain(self, url):
        domain = urlparse(url).netloc
        if domain.count('.') > 3:
            return -1
        elif domain.count('.') == 3:
            return 0
        else:
            return 1

    def SSLfinal_State(self, url):
        return 1 if urlparse(url).scheme == "https" else -1

    def Domain_registeration_length(self, url):
        try:
            domain_info = whois.whois(url)
            expiration_date = domain_info.expiration_date
            creation_date = domain_info.creation_date
            if isinstance(expiration_date, list): expiration_date = expiration_date[0]
            if isinstance(creation_date, list): creation_date = creation_date[0]
            age = (expiration_date - creation_date).days
            return 1 if age >= 365 else -1
        except:
            return -1

    def Favicon(self, response, domain):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('link', href=True):
                if domain not in link['href']:
                    return -1
            return 1
        except:
            return 1

    def port(self, url):
        try:
            domain = urlparse(url).netloc
            socket.gethostbyname(domain)
            return 1
        except:
            return -1

    def HTTPS_token(self, url):
        domain = urlparse(url).netloc
        return -1 if "https" in domain else 1

    def Request_URL(self, response, domain):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            total, safe = 0, 0
            for img in soup.find_all('img', src=True):
                total += 1
                if domain in img['src'] or img['src'].startswith('/'):
                    safe += 1
            return 1 if total > 0 and safe / total >= 0.5 else -1
        except:
            return 1

    def URL_of_Anchor(self, response, domain):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            total, unsafe = 0, 0
            for a in soup.find_all('a', href=True):
                total += 1
                if '#' in a['href'] or 'javascript' in a['href'].lower() or domain not in a['href']:
                    unsafe += 1
            return 1 if total > 0 and unsafe / total < 0.3 else -1
        except:
            return 1

    def Links_in_tags(self, response, domain):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            tags = soup.find_all(['meta', 'script', 'link'])
            total, unsafe = len(tags), 0
            for tag in tags:
                if tag.has_attr('href') and domain not in tag['href']:
                    unsafe += 1
            return 1 if total > 0 and unsafe / total < 0.3 else -1
        except:
            return 1

    def SFH(self, response):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            for form in soup.find_all('form', action=True):
                if form['action'] == "" or "about:blank" in form['action']:
                    return -1
            return 1
        except:
            return 1

    def Submitting_to_email(self, response):
        return -1 if "mailto:" in str(response.content) else 1

    def Abnormal_URL(self, url):
        try:
            domain = urlparse(url).netloc
            return 1 if whois.whois(domain) else -1
        except:
            return -1

    def Redirect(self, response):
        return 1 if len(response.history) <= 1 else (0 if len(response.history) <= 4 else -1)

    def on_mouseover(self, response):
        return -1 if re.findall("<script>.+onmouseover.+</script>", str(response.content)) else 1

    def RightClick(self, response):
        return -1 if re.findall(r"event.button ?== ?2", str(response.content)) else 1

    def popUpWidnow(self, response):
        return -1 if re.findall(r"alert\(", str(response.content)) else 1

    def Iframe(self, response):
        return -1 if re.findall(r"<iframe>", str(response.content)) else 1

    def age_of_domain(self, url):
        try:
            domain_info = whois.whois(url)
            creation_date = domain_info.creation_date
            if isinstance(creation_date, list): creation_date = creation_date[0]
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
        return 1  # Placeholder

    def Page_Rank(self, url):
        return 1  # Placeholder

    def Google_Index(self, url):
        return 1  # Placeholder

    def Links_pointing_to_page(self, response):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            return -1 if len(links) < 2 else 1
        except:
            return 1

    def Statistical_report(self, url):
        return 1  # Placeholder

    def extract_features(self, url):
        response = self.fetch_response(url)
        domain = urlparse(url).netloc
        return np.array([
            self.having_IP_Address(url),
            self.URL_Length(url),
            self.Shortining_Service(url),
            self.having_At_Symbol(url),
            self.double_slash_redirecting(url),
            self.Prefix_Suffix(url),
            self.having_Sub_Domain(url),
            self.SSLfinal_State(url),
            self.Domain_registeration_length(url),
            self.Favicon(response, domain),
            self.port(url),
            self.HTTPS_token(url),
            self.Request_URL(response, domain),
            self.URL_of_Anchor(response, domain),
            self.Links_in_tags(response, domain),
            self.SFH(response),
            self.Submitting_to_email(response),
            self.Abnormal_URL(url),
            self.Redirect(response),
            self.on_mouseover(response),
            self.RightClick(response),
            self.popUpWidnow(response),
            self.Iframe(response),
            self.age_of_domain(url),
            self.DNSRecord(url),
            self.web_traffic(url),
            self.Page_Rank(url),
            self.Google_Index(url),
            self.Links_pointing_to_page(response),
            self.Statistical_report(url)
        ]).reshape(1, -1)
