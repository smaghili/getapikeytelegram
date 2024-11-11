import subprocess
import sys
import os

def check_and_install_requirements():
    # Check if running as root
    if os.geteuid() != 0:
        print("This script needs root privileges to install required packages.")
        print("Please run with sudo or as root.")
        sys.exit(1)

    # Check if pip3 is installed
    try:
        subprocess.run(['which', 'pip3'], check=True, capture_output=True)
        print("pip3 is already installed")
    except subprocess.CalledProcessError:
        print("Installing python3-pip...")
        try:
            subprocess.run(['apt', 'update'], check=True)
            subprocess.run(['apt', 'install', '-y', 'python3-pip'], check=True)
            print("python3-pip installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install python3-pip: {e}")
            sys.exit(1)

    # Check if required packages are installed
    try:
        import requests
        import bs4
        print("Required Python packages are already installed")
    except ImportError:
        print("Installing required Python packages...")
        try:
            subprocess.run(['pip3', 'install', 'requests', 'beautifulsoup4'], check=True)
            print("Required packages installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install required packages: {e}")
            sys.exit(1)

def save_credentials(api_id, api_hash):
    data = {
        "api_id": api_id,
        "api_hash": api_hash,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open("telegram_credentials.json", "w") as f:
        json.dump(data, f, indent=4)

def main():
    session = requests.Session()
    
    phone = input('Enter your phone number (ex. 18880001234): ')

    send_password_url = 'https://my.telegram.org/auth/send_password'
    response = session.post(send_password_url, data={'phone': phone})
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return
        
    if "Sorry, too many tries" in response.text:
        print("Too many tries. Please try again later.")
        return
        
    try:
        random_hash = response.json()['random_hash']
    except Exception as e:
        print(f"Failed to get random hash: {response.text}")
        return
    
    confirmation_code = input('Enter the confirmation code: ')
    
    login_url = 'https://my.telegram.org/auth/login'
    login_data = {
        'phone': phone,
        'random_hash': random_hash,
        'password': confirmation_code
    }
    
    response = session.post(login_url, data=login_data)
    if response.status_code != 200 or response.text != "true":
        print("Login failed!")
        print(f"Response: {response.text}")
        return

    time.sleep(1)

    apps_page = session.get('https://my.telegram.org/apps')
    if apps_page.status_code != 200:
        print(f"Failed to get apps page: {apps_page.status_code}")
        return

    soup = BeautifulSoup(apps_page.text, 'html.parser')
    
    api_id = None
    api_hash = None
    
    for div in soup.find_all('div', {'class': 'form-group'}):
        if div.find('strong'):
            api_id_elem = div.find('strong')
            if api_id_elem:
                api_id = api_id_elem.text.strip()
            
            next_div = div.find_next_sibling('div', {'class': 'form-group'})
            if next_div and next_div.find('span'):
                api_hash = next_div.find('span').text.strip()
                break
    
    if not api_id or not api_hash:
        page_hash = soup.find('input', {'name': 'hash'})
        if not page_hash:
            print("Could not find hash on page")
            return
            
        hash_value = page_hash.get('value')
        
        create_url = "https://my.telegram.org/apps/create"
        app_data = {
            'hash': hash_value,
            'app_title': 'MyTelegramApp',
            'app_shortname': 'mytgapp',
            'app_url': '',
            'app_platform': 'desktop',
            'app_desc': ''
        }
        
        response = session.post(create_url, data=app_data)
        if response.status_code != 200:
            print(f"Failed to create app: {response.status_code}")
            return

        time.sleep(1)
            
        apps_page = session.get('https://my.telegram.org/apps')
        soup = BeautifulSoup(apps_page.text, 'html.parser')
        
        for div in soup.find_all('div', {'class': 'form-group'}):
            if div.find('strong'):
                api_id_elem = div.find('strong')
                if api_id_elem:
                    api_id = api_id_elem.text.strip()
                
                next_div = div.find_next_sibling('div', {'class': 'form-group'})
                if next_div and next_div.find('span'):
                    api_hash = next_div.find('span').text.strip()
                    break
    
    if not api_id or not api_hash:
        print("Could not retrieve API credentials")
        return
        
    print("\n=== API Credentials ===")
    print(f"API ID: {api_id}")
    print(f"API Hash: {api_hash}")
    
    save_credentials(api_id, api_hash)
    print("\nCredentials saved to 'telegram_credentials.json'")

if __name__ == '__main__':
    try:
        # First check and install requirements
        check_and_install_requirements()
        
        # Now import the required packages
        import requests
        from bs4 import BeautifulSoup
        import json
        import time
        
        main()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        input("\nPress Enter to exit...")
