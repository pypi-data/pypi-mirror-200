import time

from .thirdparty_packages import requests
try:
    from config import ThirdServicesConfig
    DNSLOG_SERVER = ThirdServicesConfig.DNSLOG_SERVER
except ImportError:
    DNSLOG_SERVER = ""


class GTLog(object):
    gtlog_addr = DNSLOG_SERVER

    def __init__(self):
        self.domain = []
        self.payload = []

    def get_random_domain(self):
        if not self.gtlog_addr:
            raise RuntimeError("DNSLOG server not configure)")
        try:
            rs = requests.get('{}/api/get_domain'.format(self.gtlog_addr))
        except:
            raise RuntimeError(f"Get Domain from {self.gtlog_addr} failed.")
        else:
            domain = rs.text
            self.domain.append(domain)
            return domain

    def get_callback_domain(self):
        if not self.gtlog_addr:
            raise RuntimeError("DNSLOG server not configure)")
        try:
            rs = requests.get('{}/api/get_callback_domain'.format(self.gtlog_addr))
        except:
            raise RuntimeError(f"Get Domain from {self.gtlog_addr} failed.")
        else:
            return rs.text

    def verify_dnslog(self, domain=None, delay=5):
        if not self.gtlog_addr:
            raise RuntimeError("DNSLOG server not configure)")
        if domain is None:
            domain = self.domain[-1]
        for _ in range(3):
            time.sleep(delay)
            try:
                rs = requests.get('{}/api/verify_dnslog/{}'.format(self.gtlog_addr, domain))
            except:
                pass
            else:
                if rs.status_code == 200 and rs.json().get("status"):
                    return True
        return False

    def get_domain_record(self, domain_prefix):
        if not self.gtlog_addr:
            raise RuntimeError("DNSLOG server not configure)")
        try:
            rs = requests.get('{}/v1/gtlog/dnslog?random_string={}'.format(self.gtlog_addr, domain_prefix))
        except:
            pass
        else:
            if rs.status_code == 200 and rs.json().get("lists", []):
                return rs.json().get("lists")
        return []
