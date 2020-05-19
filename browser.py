import sys
import os
import requests
from bs4 import BeautifulSoup
from collections import deque


domains = ['.com', '.net', '.org', '.ru']
# manage folder name
folder_name = "dir-for-files"
if len(sys.argv) == 2:
    folder_name = sys.argv[1]
# stack
history_stack = deque()


def create_file(dir_name, file_name, text):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    with open(dir_name + '/' + file_name, 'w', encoding='utf-8') as file:
        file.write(text)


def format_url_to_filename(url):
    name = handle_url(url)
    for domain in domains:
        if name.endswith(domain):
            return name[8:(-1 * len(domain))]
    return name


def read_cached(dir_name, new_file_name):
    path = dir_name + '/' + new_file_name
    if os.path.isfile(path):
        with open(path, 'r', encoding="utf-8") as fi:
            return fi.read()
    else:
        return "Not exists!"


def handle_request_text(web_address):
    url = handle_url(web_address)
    try:
        r = requests.get(url, timeout=1.0)
    except requests.exceptions.RequestException as error:
        return error
    if r:
        # save content to file into storage
        content = html_to_text(r.text)
        file_name = format_url_to_filename(url) + '.txt'
        create_file(folder_name, file_name, content)
        # add mark into history file
        save_to_list(url=url, dir_name=folder_name)
        return content
    else:
        return "Not found. Status: " + str(r.status_code)


def handle_url(url):
    if "http://" in url:
        return url
    elif "https://" in url:
        return url
    else:
        return "https://" + url


def save_to_list(url, file_name='cached_list.txt', dir_name="dir-for-files"):
    # check if history file exists
    short_name = format_url_to_filename(url)
    path = dir_name + '/' + file_name
    if os.path.isfile(path):
        with open(path, 'r', encoding="utf-8") as storage:
            if short_name not in storage.read().split('\n'):
                with open(path, 'a', encoding="utf-8") as file:
                    file.write(short_name + '\n')
    else:
        with open(path, 'w', encoding="utf-8") as file:
            file.write(short_name + '\n')


def show_list(dir_name="dir-for-files", file_name='cached_list.txt'):
    path = dir_name + '/' + file_name
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    else:
        return "Not found"


def html_to_text(text):
    tags = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "ol", "li"]
    soup = BeautifulSoup(text, 'html.parser')
    tag_cont = soup.find_all(tags)
    content = ""
    for tag in tag_cont:
        content += (str(tag) + '\n')
    new_soup = BeautifulSoup(content, 'html.parser')
    return new_soup.get_text("\n", strip=True)


while True:
    command = input('> ')
    if command == 'exit':
        break
    if command == "back":
        if len(history_stack) > 1:
            history_stack.pop()
            page_name = history_stack[-1]
            print(read_cached(folder_name, page_name + '.txt'))
        continue
    if command == 'cache':
        print(show_list())
        continue

    # check if no domain in command
    # then look in history
    domain_match = any(domain in command for domain in domains)
    if not domain_match:
        answer = read_cached(folder_name, command + '.txt')
        if answer != "Not exists!":
            print(answer)
            history_stack.append(command)
            continue
        else:
            print("Error: Incorrect URL")
            continue

    # handle request
    response = handle_request_text(command)
    print(response)
    history_stack.append(format_url_to_filename(command))
