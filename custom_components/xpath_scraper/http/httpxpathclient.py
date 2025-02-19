from .xpath_value import XpathValue

import requests
from lxml import html
import re
import time

class HttpXpathClient():
    
    def get_request(self, url, xpath_expr, ssl_check=True, clean_checker=False) -> XpathValue:
        max_retries=10
        attempt = 0
        while attempt < max_retries:
            attempt += 1
            try:
                response = requests.get(url)
                response.raise_for_status()  
            except requests.exceptions.RequestException as e:
                time.sleep(1)  
                continue   

            try:
                tree = html.fromstring(response.content)
            except Exception as e:
                time.sleep(1)  
                continue  

            results = tree.xpath(xpath_expr)
 
            if not results:
                time.sleep(1)  
                continue  
            else:
                for result in results:
                    if isinstance(result, html.HtmlElement):
                        result_text = result.text_content().strip()
                    else:
                        result_text = str(result)
                    if clean_checker:
                        result_text = self._clean_number(result_text)

                    return XpathValue(url, xpath_expr, result_text)

        return XpathValue(url, xpath_expr, None)

    def _clean_number(self, input_string):
        cleaned = re.sub(r'[^0-9.,]', '', input_string)
        
        if cleaned.count(',') > 1:
            cleaned = cleaned.replace(',', '', cleaned.count(',') - 1)
        if cleaned.count('.') > 1:
            cleaned = cleaned.replace('.', '', cleaned.count('.') - 1)
        
        return cleaned