import sys
import os

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created “soft” magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''

internet = {"bloomberg.com": bloomberg_com,
            "nytimes.com": nytimes_com}

def create_file(dir_name, file_name, text):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    with open(dir_name + '/' + file_name, 'w', encoding='utf-8') as file:
        file.write(text)


def read_cached(dir_name, new_file_name):
    path = dir_name + '/' + new_file_name
    if os.path.isfile(path):
        with open(path, 'r') as fi:
            return fi.read()
    else:
        return "Not exists!"


# manage folder name
folder_name = "dir-for-files"
if len(sys.argv) == 2:
    folder_name = sys.argv[1]

# write your code here
while True:
    command = input('> ')
    if command == 'exit':
        break

    # check if in history
    if '.com' not in command:
        answer = read_cached(folder_name, command + '.txt')
        if answer != "Not exists!":
            print(answer)
            continue
        else:
            print("Error: Incorrect URL")
            continue
    if command in internet:
        print(internet[command])
        # create file
        file_name = command.replace('.com', '.txt')
        create_file(folder_name, file_name, internet[command])
    else:
        print("Error: Incorrect URL")

