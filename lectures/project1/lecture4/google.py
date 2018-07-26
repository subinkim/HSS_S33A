import requests

def main():
    res = requests.get('https://www.google.com/')
    print(res.text)
    print(res.status_code)

if __name__ == '__main__':
    main()
