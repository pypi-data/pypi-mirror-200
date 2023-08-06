# Site Sniffer in Python 🐽

Site Sniffer is a Python package designed to extract information about a website by providing its URL. It is useful for individuals who need to perform website analysis, including web developers, SEO specialists, and website owners. The package extracts various details such as the IP address, HTTP status code, SSL certificate information, domain registration details, load time, meta description, keywords, and a list of links on the page.


## Installation

Install sitesniffer with pip

```bash
  pip install sitesniffer
```

## Essential Python Libraries for Web Scraping and HTTP Requests

The following Python libraries are essential for working with the Site Sniffer package:

* requests: used for sending HTTP requests and receiving responses.
* socket, ssl, and idna: used for working with IP addresses and SSL certificates.
* whois: used for querying WHOIS information for a domain.
* re: used for working with regular expressions.
* time: used for timing how long it takes to load a webpage.
* BeautifulSoup: used for parsing HTML.



## The defined functions included:

| Function Name  | Function Description |
| ------------- | ------------- |
| extract_hostname(url)  | Extracts the hostname from a URL  |
| get_ip_address(url)  | Gets the IP address of a domain  |
|get_domain_info(url)| Gets domain information for a website |
|get_status_code(url)|Gets the HTTP status code of a URL|
|get_ssl_info(url)|Gets SSL certificate information for a domain|
|get_load_time(url)| Gets the load time for a website and its sub-pages |
|get_page_meta_description(url)| Gets the meta description for a page |
|get_page_keywords(url)| Gets the meta keywords for a page |
|get_links(url)|Gets a list of URLs on a page|
|check_mobile_friendly(url)| Checks if a website is using mobile-friendly design |
|check_responsive_design(url)| Checks if a website is using responsive design |
|check_cookies(url)| Checks if a website is using cookies|
|check_google_analytics|Checks if a website is using Google Analytic|
|get_site_info|Returns all website information|
