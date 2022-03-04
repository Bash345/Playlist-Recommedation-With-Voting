import os
import shelve


def add_song():
    global data
    song = input('Enter a new song or press "ENTER" to skip. : ').strip()
    if not song:
        return
    if song in data:
        print('Error! This song already exists.')
    else:
        data[song] = [0, {}]
        save_all()
        print('Song added to queue')


def delete_song():
    global data
    if not data:
        print('\nThe song list is empty\n')
        return
    kl = show_playlist()
    songn = input('Enter the song number to delete or press "ENTER" to skip. : ').strip()
    if not songn:
        return
    try:
        assert 0 < int(songn) <= len(data)
        data.pop(kl[songn])
        save_all()
    except Exception as E:
        print('\nWrong choice!\n')


def vote():
    global data
    global users
    if not users:
        print('\nUser list is empty\n')
        return
    if not data:
        print('\nThe song list is empty\n')
        return
    x = enumerate(users, 1)
    for n, u in x:
        print(n, ':', u)
    user = input('Select a user number to vote : ').strip()
    try:
        assert 0 < int(user) <= len(users)
        user = users[int(user) - 1]
    except:
        print('\nWrong choice!\n')
        return
    kl = show_playlist()
    songn = input('Enter the song number to vote or press "ENTER" to skip. : ').strip()
    if not songn:
        return
    try:
        assert 0 < int(songn) <= len(data)
    except Exception as E:
        print('\nWrong choice!\n')
        return
    print('1 : Vote UP\n2 : Vote Down')
    vt = input('Select an action number to vote : ').strip()
    try:
        assert 0 < int(vt) <= 2
        res = [None, 1, -1][int(vt)]
        data[kl[songn]][1][user] = res
        data[kl[songn]][0] = sum(list(data[kl[songn]][1].values()))
        save_all()
    except Exception as E:
        print('\nWrong choice!\n')
        return
    

def save_all():
    global current_dir
    global data
    global users
    fn = os.path.join(current_dir, 'data_file')
    with shelve.open(fn) as file:
            file['data'] = data
            file['users'] = users
    

def add_user():
    global users
    name = input('Enter a new user name or press "ENTER" to skip. : ').strip()
    if not name:
        return
    if name in users:
        print('Error! This user already exists.')
    else:
        users.append(name)
        save_all()


def del_user():
    global users
    if not users:
        print('\nUser list is empty\n')
        return
    print('\nUsers:')
    for i in users:
        print(i)
    name = input('Enter the user name to delete or press "ENTER" to skip. : ').strip()
    if not name:
        return
    if name not in users:
        print('Error! This user not exists.')
    else:
        users.remove(name)
        save_all()


def show_playlist():
    global data
    if not data:
        print('\nThe song list is empty\n')
        return
    tmp = sorted(data, key=lambda x: data[x][0], reverse=True)
    kl = enumerate(tmp, 1)
    dx = {}
    for n, i in kl:
        print(n, i, data[i][0])
        dx[str(n)] = i
    return dx


def show_menu():
    while True:
        print()
        print('1 : Add a song')
        print('2 : Delete song')
        print('3 : Display playlist')
        print('4 : Add user')
        print('5 : Delete User')
        print('6 : Vote')
        print('0 : exit')
        chose = input('\nSelect an action : ').strip()
        try:
            assert 0 <= int(chose) <= 6
            return chose
        except Exception as e:
            print('\nWrong choice. Try again.\n')


def main():
    global data
    global users
    global current_dir
    current_dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(current_dir)
    data = {}
    users = []
    with shelve.open('data_file') as file:
        data = file.get('data', {})
        users = file.get('users', [])
    save_all()
    while True:
        if not data:
            print('There are no songs in the queue.')
        else:
            play = sorted(data, key=lambda x: data[x][0], reverse=True)[0]
            print('\nCurrent Song Playing is,', play)
        select = show_menu()
        print(select)
        if select == '0':
            print('\nExit\n')
            exit()
        if select == '1':
            add_song()
        if select == '2':
            delete_song()
        if select == '3':
            show_playlist()
        if select == '4':
            add_user()
        if select == '5':
            del_user()
        if select == '6':
            vote()
    

if __name__ == '__main__':
    main()
