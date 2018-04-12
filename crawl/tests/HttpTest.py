from crawl.common.http.Http import Http

http = Http("http://19.15.247.64:8080/InvestPro/minstone/indexAnalysis/getProjectNumByType")
print(http.post({'area': 440000}))