
import mysql.connector
BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode(num, alphabet=BASE62):
    """Encode a positive number in Base X

    Arguments:
    - `num`: The number to encode
    - `alphabet`: The alphabet to use for encoding
    """
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

def decode(string, alphabet=BASE62):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0
    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1
    return num

def get_max_id():
    cnx = mysql.connector.connect(user='root',host='127.0.0.1',database='urldb')
    cursor = cnx.cursor()
    cursor.execute("select max(idx) from urls")
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    return int(result[0][0])

def insert_url(idx,prefix,long_url,short_url):
    cnx = mysql.connector.connect(user='root',host='127.0.0.1',database='urldb')
    cursor = cnx.cursor()
    #print("insert into urls (idx,prefix,long_url,short_url) values ('"+idx+"','"+prefix+"','"+long_url+"','"+short_url+"');")
    cursor.execute("insert into urls (idx,prefix,long_url,short_url) values ('"+idx+"','"+prefix+"','"+long_url+"','"+short_url+"');")
    cnx.commit()
    cursor.close()
    cnx.close()

def query_url(idx):
    try:
        id = str(idx)
        cnx = mysql.connector.connect(user='root',host='127.0.0.1',database='urldb')
        cursor = cnx.cursor()
        #print("select * from urls where idx="+id+";")
        cursor.execute("select * from urls where idx="+id+";")
        #if id doesn't exit
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return result[0][1]+result[0][2]
    except:
        return None


def parse_url(url):
    if 'http://' not in url and 'https://' not in url:
        return 'http://',url
    if 'http://' in url:
        return 'http://',url[7:]
    if 'https://' in url:
        return 'https://',url[8:]
    return 'invalid url',url

def generate_short_url(long_url):
    prefix,url = parse_url(long_url)
    if prefix == 'invalid url':
        return prefix
    #if not existing then insert [prefix,url] combo
    idx = get_max_id() + 1
    shortenString = encode(idx)
    #otherwise query
    insert_url(str(idx),prefix,url,shortenString)
    short_url = prefix + shortenString
    return short_url

def translate_short_long(short_url):
    prefix,url = parse_url(short_url)
    #print(prefix,url)
    idx = decode(url)
    #query idx in db
    #if not exist, return null
    #if exist
    return query_url(idx)

if __name__ == "__main__":
    #print do you want to shorten or query
    print("test app for shorten URL \n")
    print("please select an action (q for quit, s for get shorten url, t for translate short url to long) \n")
    input = raw_input('Input:').lower()
    while input != 'q':
        if input == 's':
            print("please provide url you'd like to shorten \n")
            url = raw_input('Input:').lower()
            print("shortened url: \n")
            print(generate_short_url(url))
        if input == 't':
            print("please provide url you'd like to translate back \n")
            url = raw_input('Input:')
            print("translated url: \n")
            print(translate_short_long(url))
        print("please select an action (q for quit, s for get shorten url, t for translate short url to long) \n")
        input = raw_input('Input:').lower()
