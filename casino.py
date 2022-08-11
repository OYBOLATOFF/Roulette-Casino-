import random
from tkinter import *
import pickle
import datetime
from contextlib import redirect_stdout
with redirect_stdout(None):
    from pygame import mixer, init
init();
root = Tk();

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~| Классы |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Загружает все аккаунты игры
def Download_accounts():
    global accounts
    with open('files/accounts/accounts.bin', 'rb') as file:
        accounts = pickle.load(file);

def Save_accounts():
    with open('files/accounts/accounts.bin', 'wb') as file:
        pickle.dump(accounts, file);

#Добавляет аккаунт в базу данных
def Add_an_account(account):
    global accounts
    accounts.append(account);
    Save_accounts();

def Leave():
    global Login
    Login = LoginIntoAccount();
    global_time.lift()

def GoTime(count = 0):
    global now_time, global_time
    if count == 0:
        global_time = Label(root, bg='#373737', fg='white', font=('Gardens CM', 23, ''), text='Текущее время: ');
        global_time.place(x=1100, y=0, width=400, height=50);
        root.after(1, lambda: GoTime(count+1));
    else:
        now = datetime.datetime.now();
        months = {
            1: 'Января', 2: 'Февраля', 3: 'Марта', 4: 'Апреля', 5: 'Мая', 6: 'Июня',
            7: 'Июля', 8: 'Августа', 9: 'Сентября', 10: 'Октября', 11: 'Ноября', 12: 'Декабря'
        }
        now_day = '0'+str(now.day) if now.day < 10 else now.day;
        now_month = months[now.month]
        now_second = '0'+str(now.second) if now.second < 10 else now.second;
        now_time = f'{now_day} {now_month} {now.year} {now.hour}:{now.minute}:{now_second}'
        global_time.configure(text=f'{now_time}')
        root.after(1000, lambda: GoTime(count+1));

def format_integer(number, thousand_separator=','):
    def reverse(string):
        string = "".join(reversed(string))
        return string

    s = reverse(str(number))
    count = 0
    result = ''
    for char in s:
        count = count + 1
        if count % 3 == 0:
            if len(s) == count:
                result = char + result
            else:
                result = thousand_separator + char + result
        else:
            result = char + result
    return result

class Entry(Entry):
    def __init__(self, message, type, *args, **kwargs):

        def set_balance(new_balance):
            global balance
            new_balance = ''.join([i for i in new_balance if i != ','])
            if new_balance.isdigit():
                balance = int(new_balance);
                Roulette.balance_label.configure(text=f'Баланс: {format_integer(balance)}')
            else:
                Roulette.BET.delete(0, END);

        if type=='Bet' or type=='balance':
            def clear_of_letter(something, count=0):
                necessary_Entry = Roulette.BET if type=='Bet' else Login.new_account_ballance
                if count == 1:
                    text = necessary_Entry.get()
                    necessary_Entry.delete(0, END);
                    necessary_Entry.insert(0, text[:len(text)-1]);
                root.after(1, lambda: clear_of_letter(self, count+1))

            def make_a_correct_bet(something, count=0):
                necessary_Entry = Roulette.BET if type=='Bet' else Login.new_account_ballance
                if count == 1:
                    if necessary_Entry.get() != '':
                        bet = ''.join([i for i in necessary_Entry.get() if i != ',']);
                        necessary_Entry.delete(0, END); necessary_Entry.insert(0, format_integer( int(bet) ))
                root.after(1, lambda: make_a_correct_bet(self, count+1))

        else:
            if type=='password':
                def clear_of_letter(something, count=0):
                    global current_password
                    if count == 1:
                        text = Login.password_field.get()
                        current_password += text[-1]
                        Login.password_field.delete(0, END);
                        Login.password_field.insert(0, text[:len(text)-1]+"*");
                    root.after(1, lambda: clear_of_letter(self, count+1))

                def backspace(something):
                    global current_password
                    current_password = current_password[:-1];
            else:
                def clear_of_letter(something): pass
            def make_a_correct_bet(something): pass

        def focus_in(self, text):
            if text.lower() == 'сумма ставки':
                #Активируем кнопки
                Roulette.RED_btn.configure(state=NORMAL);
                Roulette.BLACK_btn.configure(state=NORMAL);
                Roulette.GREEN_btn.configure(state=NORMAL);
                #Удаляем подсказку
                Roulette.BET.delete('0', 'end');
                Roulette.BET.configure(fg='black');

            if text.lower() == 'логин':
                Login.login_field.delete('0', 'end');
                Login.login_field.configure(fg='black');

            if text.lower() == 'пароль':
                Login.password_field.delete('0', 'end');
                Login.password_field.configure(fg='black');

            if text.lower() == 'логин ':
                Login.new_login_field.delete('0', 'end');
                Login.new_login_field.configure(fg='black');

            if text.lower() == 'пароль ':
                Login.new_password_field.delete('0', 'end');
                Login.new_password_field.configure(fg='black');

            if text.lower() == 'повторите пароль ':
                Login.new_password_repeat_field.delete('0', 'end');
                Login.new_password_repeat_field.configure(fg='black');

            if text.lower() == 'новый баланс':
                Login.new_account_ballance.delete('0', 'end');
                Login.new_account_ballance.configure(fg='white');


        def format_integer(number, thousand_separator=','):
            def reverse(string):
                string = "".join(reversed(string))
                return string

            s = reverse(str(number))
            count = 0
            result = ''
            for char in s:
                count = count + 1
                if count % 3 == 0:
                    if len(s) == count:
                        result = char + result
                    else:
                        result = thousand_separator + char + result
                else:
                    result = char + result
            return result

        #Стандартный вызов кнопки, как обычно, а снизу модифицируем
        super().__init__(*args, **kwargs)

        #При создании кнопки автоматически вставляем подсказу и биндим события
        self.insert(0, message); self.configure(fg='gray')
        self.bind("<FocusIn>", lambda something: focus_in(self, self.get()) )
        self.bind("<Right>", lambda self: Roulette.Game('BLACK', Roulette.BET.get()))
        self.bind("<Left>", lambda self: Roulette.Game('RED', Roulette.BET.get()))
        self.bind("<Down>", lambda self: Roulette.Game('GREEN', Roulette.BET.get()))
        self.bind("<Up>", lambda self: Roulette.set_bet_size(Roulette.previous_bet))
        self.bind("<Return>", lambda self: set_balance( Roulette.BET.get() ))
        self.bind(f"<BackSpace>", make_a_correct_bet)

        #Все буквы биндим на команду clear_of_letter, которая не даёт ввести буквы в ставку
        for i in 'abcdefghijklmnopqrstuvwxyz.-':
            self.bind(f"{i}", lambda self, letter = i: clear_of_letter(self))
            self.bind(f"{i.upper()}", lambda self, letter = i: clear_of_letter(self))

        #Все буквы биндим на команду clear_of_letter, которая не даёт ввести буквы в ставку
        for i in 'абвгдеёжзклмнопрстуфхцчщъыьэюя':
            self.bind(f"{i}", lambda self, letter = i: clear_of_letter(self))
            self.bind(f"{i.upper()}", lambda self, letter = i: clear_of_letter(self))

        for i in '0123456789':
            self.bind(f"{i}", make_a_correct_bet)

        if type=='password':
            for i in '0123456789':
                self.bind(f"{i}", clear_of_letter)
            self.bind(f'<BackSpace>', backspace)
    
    def focus_out(self, message):
        self.delete(0, END)
        self.insert(0, message); self.configure(fg='gray');
        Roulette.RED_btn.configure(state=DISABLED);
        Roulette.BLACK_btn.configure(state=DISABLED);
        Roulette.GREEN_btn.configure(state=DISABLED);
        Roulette.message_label.place_forget();
        root.focus()

class RouletteWindow():

    class ColorButton(Button):
        def __init__(self, number):
            self.number = number
            super().__init__(RouletteWindow.roulette_field, fg='white', font=('', 20, ''));
            if number == 0:
                self.configure(bg='#37d799', fg='black', text=str(number));
            else:
                self.configure(bg=('#ff0000' if number % 2 == 0 else '#3a3131'), text=str(number))

        def __str__(self):
            return str(self.number)

    images = {
        'bg': PhotoImage(file='files/images/Roulette/Main.png'),
        'lose': PhotoImage(file='files/images/Roulette/LOSE.png'),
        'win': PhotoImage(file='files/images/Roulette/WIN.png'),
        'RED': PhotoImage(file='files/images/Roulette/RED.png'),
        'BLACK': PhotoImage(file='files/images/Roulette/BLACK.png'),
        'GREEN': PhotoImage(file='files/images/Roulette/GREEN.png'),
        'Leave': PhotoImage(file='files/images/Roulette/leave.png'),
        'empty_field': PhotoImage(file='files/images/Roulette/errors/empty_field.png'),
        'invalid_bet': PhotoImage(file='files/images/Roulette/errors/invalid_bet.png'),
        '100_percents': PhotoImage(file='files/images/percents/100.png'),
        '75_percents': PhotoImage(file='files/images/percents/75.png'),
        '50_percents': PhotoImage(file='files/images/percents/50.png'),
        '25_percents': PhotoImage(file='files/images/percents/25.png'),
    }
    sounds = {
    'spin': mixer.Sound("files/sounds/spin.wav"), 
    'win': mixer.Sound("files/sounds/win.wav"), 
    'fail': mixer.Sound("files/sounds/fail.wav")
    }
    roulette_field = Frame(root, padx=0, pady=0, bg='blue') #<--- Создаём поле рулетки
    guess_number = None;
    previous_bet = 1000;
    def __init__(self):
        self.roulette_field.place(x=410, y=255, width=603, height=67); #<--- Размещаем поле рулетки
        #Создаём массив кнопок
        self.buttons = [RouletteWindow.ColorButton(x) for x in range(0, 37)]
        self.buttons = self.buttons[33:]+self.buttons[:33]
        
        #Задний фон окна рулетки
        self.background = Label(root, image=self.images['bg']);
        self.background.place(x=-2, y=0);

        self.LEAVE = Button(root, image=self.images['Leave'], command=Leave, bd=0);
        self.LEAVE.place(x=10, y=10, width=77, height=77)

        #Создаём красную, чёрную и зеленую кнопки ставок
        self.RED_btn = Button(root, state=DISABLED, image=self.images['RED'], relief=RAISED, command=lambda: self.Game('RED', self.BET.get()));
        self.RED_btn.place(x=410, y=410, width=292, height=92);

        self.BLACK_btn = Button(root, state=DISABLED, image=self.images['BLACK'], relief=RAISED, command=lambda: self.Game('BLACK', self.BET.get()));
        self.BLACK_btn.place(x=725, y=410, width=292, height=92);

        self.GREEN_btn = Button(root, state=DISABLED, image=self.images['GREEN'], relief=RAISED, command=lambda: self.Game('GREEN', self.BET.get()));
        self.GREEN_btn.place(x=410, y=514, width=607, height=92);

        #Поле ввода ставок        
        self.BET = Entry('Сумма ставки', 'Bet', root, justify=CENTER, font=('Gardens CM', 20, ''), bd=10);
        self.BET.place(x=410, y=335, width=603, height=65);
        #Биндим задний фон на клик, чтоб блокировать кнопки ставок
        self.background.bind('<Button-1>', lambda something: self.BET.focus_out('Сумма ставки'))
        self.roulette_field.lift(); #<--- Рамку рулетки функцией .lift() помещаем поверх заднего фона

        #Окно вывода ошибок. Изначально не видно, активируется при встрече с ошибкой
        self.message_label = Label(root);

        #Таблица с историей ставок
        self.log_frame = Listbox(root, bg='#c1c1c1', selectmode=SINGLE, relief=RIDGE, bd=10, font=('Gardens CM', 14, ''))
        self.log_frame.place(x=1040, y=175, width=360, height=430)

        #Показатель баланса
        self.balance_label = Label(root, text=f' Баланс: {format_integer(10000)}', bg='#3a3131', fg='#ffffff', font=('Gardens CM', 15, ''), relief=RIDGE, bd=5)
        self.balance_label.place(x=1051, y=543, width=337, height=50);
        
        #Проценты ставок
        self.percent_max_btn = Button(root, image=self.images['100_percents'], bd=0, relief=FLAT, command = lambda: self.set_bet_size(balance));
        self.percent_max_btn.place(x=340, y=335, width=59, height=30);
        
        self.percent_75_btn = Button(root, image=self.images['75_percents'], bd=0, relief=FLAT, command = lambda: self.set_bet_size(int(balance*0.75)));
        self.percent_75_btn.place(x=340, y=370, width=59, height=30);
        
        self.percent_50_btn = Button(root, image=self.images['50_percents'], bd=0, relief=FLAT, command = lambda: self.set_bet_size(int(balance*0.5)));
        self.percent_50_btn.place(x=340, y=405, width=59, height=30);
        
        self.percent_25_btn = Button(root, image=self.images['25_percents'], bd=0, relief=FLAT, command = lambda: self.set_bet_size(int(balance*0.25)));
        self.percent_25_btn.place(x=340, y=440, width=59, height=30);

        for i in range(37): #<--- Генерируем клетки
            self.buttons[i].place(x=67*i, y=0, width=67, height=67)

        #Имя аккаунта в углу
        self.account_name = Label(root, text=f'Вы вошли как: ', fg='white', bg='#373737', font=('Gardens CM', 20, ''), justify=CENTER)
        self.account_name.place(x=1100, y=750, width=400, height=50);

    def Game(self, color, bet_size):

        def Check(color, bet_size):
            global balance
            bet_size = ''.join([i for i in bet_size if i != ',']);
            ERROR = 1 if bet_size == '' else 0;
            if not(ERROR): ERROR = 2 if not(1 <= float(bet_size) <= balance) else 0
            if ERROR:
                self.BET.delete('0', 'end'); #<--- Обнуляем поле ввода
                self.BET.configure(fg='black');  #<--- Код 0 - ошибка пустого поля, ошибка в Label меняется на соответствующую
                #Снизу словарь, в котором каждому коду ошибки сопоставляется картинка, которая передастся в ErrorLabel
                error_images = {1: self.images['empty_field'], 2: self.images['invalid_bet']}
                self.message_label.place(x=410, y=205, width=603, height=37)
                self.message_label.configure(image=error_images[ERROR]) #<--- Меняем картинку в ErrorLabel на соответствующую
                return False
            return True

        def Animation(color, bet_size, count=0):
            global guess_number, accounts, history
            if count == 0: self.sounds['spin'].play();
            #Если рулетка сдвинулась 93 раза, то есть 2.5 круга, то уже можно останавливать, крутим до тех пор, пока не встретим загаданное число
            if count >= 93:
                if self.buttons[5].number == self.guess_number:
                    self.sounds['spin'].stop() #<--- Останавливаем звук вращения

                    #После вращения рулетки высчитывается результат и вызывается соответствующая функция с наградой или проигрышем
                    if color=='GREEN' and self.guess_number == 0:
                        self.sounds['win'].play();
                        self.win(bet_size, 36)
                    elif color=='RED' and self.guess_number % 2 == 0 and self.guess_number != 0 or color=='BLACK' and self.guess_number % 2 != 0:
                        self.sounds['win'].play();
                        self.win(bet_size, 1)
                    else:
                        self.sounds['fail'].play()
                        self.lost(bet_size)
                    history.append((color, self.guess_number, int(bet_size)))
                    self.log_write(history[-1])

                    self.RED_btn.configure(state=NORMAL);  self.BLACK_btn.configure(state=NORMAL);  self.GREEN_btn.configure(state=NORMAL);
                    self.BET.configure(state=NORMAL)
                    self.balance_label.configure(text=f'Баланс: {format_integer(balance)}')
                    accounts[account_index][2] = balance;
                    accounts[account_index][3] = history
                    for account in accounts:
                        print(account)
                    Save_accounts();
                    return None

            self.buttons = self.buttons[1:]+self.buttons[:1];
            self.place_color_buttons();
            root.after(int(40+count*0.5), lambda: Animation(color, bet_size, count+1));
        
        if Check(color, bet_size):
            bet_size = int(''.join([i for i in bet_size if i != ','])) #<--- Избавляемся от запятых в ставке
            self.previous_bet = bet_size
            self.BET.delete('0', 'end'); #<--- Удаляем ставку с поля ввода
            self.message_label.place_forget(); #<--- Удаляем сообщение об ошибке
            self.balance_label.configure(text=f'Баланс: {format_integer(balance-int(bet_size))}')
            self.guess_number = random.randint(0, 36);
            Animation(color, bet_size) #<--- Запускаем анимацию рулетки

            root.focus() #<--- Убираем курсор с поля ввода ставки, переводим на главный экран
            #Временно выключаем кнопки ставок
            self.RED_btn.configure(state=DISABLED);  self.BLACK_btn.configure(state=DISABLED);  self.GREEN_btn.configure(state=DISABLED);
            self.BET.configure(state=DISABLED)


    def win(self, bet_size, award):
        global balance
        balance += int(bet_size)*award
        self.message_label.configure(image=self.images['win'])
        self.message_label.place(x=410, y=205, width=603, height=37)

    def lost(self, bet_size):
        global balance, history
        balance -= int(bet_size)
        self.message_label.configure(image=self.images['lose'])
        self.message_label.place(x=410, y=205, width=603, height=37)

        if balance == 0:
            EndGame.Show()

    def log_write(self, recording):

        if recording[1] == 0:
            self.log_frame.insert(END, ' Выпал 0 | '+(f'Вы выиграли {recording[2]*36}' if recording[0]=='GREEN' else f'Вы проиграли {recording[2]}'))
            self.log_frame.itemconfig(END, fg='black', bg='#37d799')
        
        elif recording[1] % 2 == 0:
            self.log_frame.insert(END, f' Выпало {recording[1]} | '+(f'Вы выиграли {recording[2]}' if recording[0]=='RED' else f'Вы проиграли {recording[2]}'))
            self.log_frame.itemconfig(END, fg='black', bg='#e63e3e')
        
        elif recording[1] % 2 != 0:
            self.log_frame.insert(END, f' Выпало {recording[1]} | '+(f'Вы выиграли {recording[2]}' if recording[0]=='BLACK' else f'Вы проиграли {recording[2]}'))
            self.log_frame.itemconfig(END, fg='white', bg='#3a3131')

    def place_color_buttons(self, start=False, j=0):
        if not(start) and int(j) == 67:
            return None
        for i in range(37): #<--- С помощью цикла сдвигаем каждую клетку влево
            self.buttons[i].place(x=67*i-j, y=0, width=67, height=67)
        if not(start): root.after(1, lambda: self.place_color_buttons(False, j+1.776))

    def set_bet_size(self, size):
        self.BET.focus();
        self.RED_btn.configure(state=NORMAL);  self.BLACK_btn.configure(state=NORMAL);  self.GREEN_btn.configure(state=NORMAL);
        self.BET.configure(fg='black');
        self.BET.delete(0, END)
        self.BET.insert(0, str(size));

class EndGame():

    images = {
    'continue': PhotoImage(file='files/images/EndGame/continue.png'),
    'finish': PhotoImage(file='files/images/EndGame/finish.png'),
    'bg': PhotoImage(file='files/images/EndGame/Main.png')
    }

    def __init__(self):
        self.Frame = Frame(root, bg='red')
        self.Background = Label(self.Frame, image=self.images['bg'])
        self.Background.place(x=-1.5, y=0)
        
        self.continue_btn = Button(self.Frame, image=self.images['continue'], bd=0, relief=FLAT, command=self.Continue)
        self.finish_btn = Button(self.Frame, image=self.images['finish'], bd=0, relief=FLAT, command=self.Finish)
        self.continue_btn.place(x=380, y=275, width=755, height=155);
        self.finish_btn.place(x=380, y=450, width=755, height=155);

    def Show(self, count=0):
        if count == 2:
            self.Frame.place(x=0, y=0, width=1500, height=800)
        root.after(750, lambda: self.Show(count+1))

    def Continue(self):
        self.Frame.place_forget();

    def Finish(self):
        root.destroy()

class LoginIntoAccount():
    images = {
    'bg': PhotoImage(file='files/images/Login/Main.png'),
    'Login_active': PhotoImage(file='files/images/Login/Login_active.png'),
    'Login_not_active': PhotoImage(file='files/images/Login/Login_not_active.png'),
    'Registration_active': PhotoImage(file='files/images/Login/Registration_active.png'),
    'Registration_not_active': PhotoImage(file='files/images/Login/Registration_not_active.png'),
    'Different_passwords': PhotoImage(file='files/images/Login/errors/different_passwords.png'),
    'Too_short_pass': PhotoImage(file='files/images/Login/errors/too_short_pass.png'),
    'Already_exists': PhotoImage(file='files/images/Login/errors/already_exists.png'),
    'Wrong_password': PhotoImage(file='files/images/Login/errors/wrong_password.png'),
    'Account_does_not_exists': PhotoImage(file='files/images/Login/errors/account_does_not_exists.png'),
    'Admin_delete': PhotoImage(file='files/images/Login/admin/delete.png'),
    'Successful_registration': PhotoImage(file='files/images/Login/congratulations/successful_registration.png')
    }
    def __init__(self):
        #Размещаем окно
        self.Frame = Frame(root, bg='gray')
        self.Frame.place(x=0, y=0, width=1500, height=800);

        #Установка заднего фона и фокус по нажатию мышкой
        self.Background = Label(self.Frame, image=self.images['bg'])
        self.Background.bind("<Button-1>", lambda self: root.focus())
        self.Background.place(x=-208, y=-141)

        #Вывод ошибок на экран
        self.error_message = Label(self.Frame, image=self.images['Too_short_pass']);

        #Кнопка переключения на ВХОД
        self.login = Button(self.Frame, image=self.images['Login_active'], bd=-1, relief=FLAT, command=self.login_interface)
        self.login.place(x=453, y=253, width=146, height=46)

        #Кнопка переключения на РЕГИСТРАЦИЮ
        self.registration = Button(self.Frame, image=self.images['Registration_not_active'], bd=-1, relief=FLAT, command=self.registration_interface)
        self.registration.place(x=666, y=253, width=416, height=46)

        #Поле для ввода логина
        self.login_field = Entry('Логин', 'login', self.Frame, bg='#e4e5e9', font=('Gardens CM', 20, ''), bd=0, justify=CENTER, highlightbackground="black", highlightthickness=3);
        self.login_field.bind('<FocusOut>', lambda something: self.focus_out( self.login_field, 'Логин' ))
        self.login_field.bind('<Return>', lambda something: self.Login())
        self.login_field.place(x=453, y=315, width=627, height=54);

        #Поле для ввода пароля
        self.password_field = Entry('Пароль', 'password', self.Frame, bg='#e4e5e9', font=('Gardens CM', 20, ''), bd=0, justify=CENTER, highlightbackground="black", highlightthickness=3);
        self.password_field.bind('<FocusOut>', lambda something: self.focus_out( self.password_field, 'Пароль' ))
        self.password_field.bind('<Return>', lambda something: self.Login())
        self.password_field.place(x=453, y=392, width=627, height=54);

        #Кнопка-запрос на вход в аккаунта
        self.login_submit = Button(self.Frame, text='ВОЙТИ', bd=5, bg='#373737', fg='white', justify=CENTER, font=('Gardens CM', 25, ''), highlightbackground="red", highlightthickness=10, command=self.Login)
        self.login_submit.place(x=453, y=469, width=627, height=54);
        self.login_submit.bind("<Enter>", lambda something: self.login_submit.configure(bg='#c44949'));
        self.login_submit.bind("<Leave>", lambda something: self.login_submit.configure(bg='#373737'));


        #Поле для ввода логинка ПРИ РЕГИСТРАЦИИ
        self.new_login_field = Entry('Логин ', 'login', self.Frame, bg='#e4e5e9', font=('Gardens CM', 20, ''), bd=0, justify=CENTER, highlightbackground="black", highlightthickness=3);
        self.new_login_field.bind('<Return>', lambda something: self.Registration())
        self.new_login_field.bind('<FocusOut>', lambda something: self.focus_out( self.new_login_field, 'Логин ' ))

        #Кнопка для ввода пароля ПРИ РЕГИСТРАЦИИ
        self.new_password_field = Entry('Пароль ', 'password', self.Frame, bg='#e4e5e9', font=('Gardens CM', 20, ''), bd=0, justify=CENTER, highlightbackground="black", highlightthickness=3);
        self.new_password_field.bind('<Return>', lambda something: self.Registration())
        self.new_password_field.bind('<FocusOut>', lambda something: self.focus_out( self.new_password_field, 'Пароль ' ))

        #Кнопка для ввода повторного пароля ПРИ РЕГИСТРАЦИИ
        self.new_password_repeat_field = Entry('Повторите пароль ', 'password', self.Frame, bg='#e4e5e9', font=('Gardens CM', 20, ''), bd=0, justify=CENTER, highlightbackground="black", highlightthickness=3);
        self.new_password_repeat_field.bind('<Return>', lambda something: self.Registration())
        self.new_password_repeat_field.bind('<FocusOut>', lambda something: self.focus_out( self.new_password_repeat_field, 'Повторите пароль ' ))

        #Кнопка-запрос на регистрацию аккаунта
        self.registration_submit = Button(self.Frame, text='ЗАРЕГИСТРИРОВАТЬСЯ', bd=5, bg='#373737', fg='white', justify=CENTER, font=('Gardens CM', 25, ''), highlightbackground="red", highlightthickness=10, command=self.Registration)
        self.registration_submit.bind("<Enter>", lambda something: self.registration_submit.configure(bg='#c44949'));
        self.registration_submit.bind("<Leave>", lambda something: self.registration_submit.configure(bg='#373737'));


        #АДМИН ПАНЕЛЬ
        self.admin_panel = Listbox(self.Frame, bg='#d7d8dc', bd=3, highlightbackground="black", highlightthickness=3, font=('Arial', 11, ''), selectmode=EXTENDED)
        self.admin_panel.bind('<Return>', lambda something: self.Login( accounts[self.admin_panel.curselection()[0]] ))
        
        #Надпись "Режим администратора"
        self.admin_label = Label(self.Frame, text='Режим администратора', justify=CENTER, bg='#373737', font=('Gardens CM', 18, ''), fg='white')
        
        #Кнопка "Удалить аккаунт"
        self.admin_delete = Button(self.Frame, image=self.images['Admin_delete'], bd=0, command=lambda something=1: self.delete_account( self.admin_panel.curselection() ));

        #Поле "Изменить баланс"
        self.new_account_ballance = Entry('Новый баланс', 'balance', self.Frame, bg='#373737', fg='white', font=('Gardens CM', 16, ''), bd=0, justify=CENTER, highlightbackground="black", highlightthickness=3);
        self.new_account_ballance.configure(fg='white')
        self.new_account_ballance.bind('<Return>', lambda something=1: self.new_balance( self.new_account_ballance.get(), self.admin_panel.curselection() ))
        self.new_account_ballance.bind('<FocusOut>', lambda something: self.focus_out( self.new_account_ballance, 'Новый баланс' ))

    def delete_account(self, indexes):
        global accounts
        for index in indexes:
            accounts[index] = [];
        for i in range(len(indexes)):
            self.admin_panel.delete(indexes[i]-i)
        accounts = [account for account in accounts if account != []]
        Save_accounts();

    def new_balance(self, balance, indexes):
        global accounts
        balance = int(''.join([i for i in balance if i != ',']));
        for index in indexes:
            accounts[index][2] = balance;
            self.admin_panel.delete(index, index)
            self.admin_panel.insert(index, f'[{accounts[index][0]}] [{accounts[index][1]}] [{accounts[index][2]}]')
        Save_accounts();

    def login_interface(self):
        global current_password
        current_password = ''
        self.error_message.place_forget(); #<--- Стираем ошибку с экрана
        #Меняем подсветку кнопок местами
        self.login.configure(image=self.images['Login_active']);
        self.registration.configure(image=self.images['Registration_not_active'])
        
        #Возвращаем подсказки для логинка
        self.login_field.delete(0, END);
        self.login_field.insert(0, 'Логин');
        self.login_field.configure(fg='gray')

        #Возвращаем подсказки для gfhjkz
        self.password_field.delete(0, END);
        self.password_field.insert(0, 'Пароль');
        self.password_field.configure(fg='gray');
        root.focus();

        #Скрываем кнопки для РЕГИСТРАЦИИ
        self.new_login_field.place_forget();
        self.new_password_field.place_forget();
        self.new_password_repeat_field.place_forget();
        self.registration_submit.place_forget();

        #Включаем кнопки для ВХОДА
        self.login_field.place(x=453, y=315, width=627, height=54);
        self.password_field.place(x=453, y=392, width=627, height=54);
        self.login_submit.place(x=453, y=469, width=627, height=54);

    def registration_interface(self):
        self.error_message.place_forget(); #<--- Стираем ошибку с экрана
        self.HiseAdminPanel(); #<--- Скрываем админ панель
        #Меняем подсветку кнопок местами
        self.login.configure(image=self.images['Login_not_active']);
        self.registration.configure(image=self.images['Registration_active'])

        #Скрываем кнопки для ВХОДА
        self.login_field.place_forget();
        self.password_field.place_forget();
        self.login_submit.place_forget();

        #Включаем кнопки для РЕГИСТРАЦИИ
        self.new_login_field.place(x=453, y=315, width=627, height=54);
        self.new_password_field.place(x=453, y=392, width=627, height=54);
        self.new_password_repeat_field.place(x=453, y=469, width=627, height=54);
        self.registration_submit.place(x=453, y=546, width=627, height=54)

    def Login(self, account=False, count=0):
        global balance, account_index, current_password
        #Очищаем табло с историей ставок
        Roulette.log_frame.delete(0, END);
        self.HiseAdminPanel(); #<--- Скрываем админ панель

        if not(account): #<--- Если аккаунт не передался аргументом (т.е. если это не вход администратора)
            nickname = self.login_field.get();
            password = current_password;
        else:
            nickname, password, balance, history = account
        
        if nickname=='admin' and password=='admin': #<--- Активация админ-панели
            self.AdminPanel();
        else:
            for index in range(len(accounts)):
                if nickname in accounts[index] and password in accounts[index]:
                    self.Frame.place_forget();
                    balance = accounts[index][2]; #<--- Загружаем баланс игрока
                    account_index = index; #<--- Чтоб менять историю игрока, нужен его индекс в учётной записи игроков
                    current_password = '' #<--- В этой переменной хранится введённый на данный момент пароль
                    history = accounts[index][3]; #<--- Загружаем историю игрока
                    Roulette.balance_label.configure(text=f'Баланс: {format_integer(balance)}') #<--- Показываем баланс игрока
                    Roulette.account_name.configure(text=f'Вы вошли как: {accounts[account_index][0]}') #<--- Показываем логин авторизации
                    
                    for bet in history:
                        Roulette.log_write(bet)

                    return True
                elif nickname in accounts[index] and password not in accounts[index]:
                    self.error_message.configure(image=self.images['Wrong_password'])
                    self.error_message.place(x=455, y=212, width=626, height=32)
                    return False
            self.error_message.configure(image=self.images['Account_does_not_exists'])
            self.error_message.place(x=455, y=212, width=626, height=32)
            return False

    def Registration(self):
        global accounts, current_password
        nickname = self.new_login_field.get();
        if any( nickname in account for account in accounts): #<--- Если аккаунт уже существует
            self.error_message.configure(image=self.images['Already_exists'])
            self.error_message.place(x=455, y=212, width=626, height=32)
        else:
            if self.new_password_field.get() == self.new_password_repeat_field.get():
                password = self.new_password_field.get();
                if len(password) >= 4:
                    Add_an_account( [nickname, password, 10000, []] ) #<--- Добавляем аккаунт в базу данных
                    self.admin_panel.insert(END, f'[{nickname}] [{password}] [10000]')
                    self.error_message.configure(image=self.images['Successful_registration'])
                    self.error_message.place(x=455, y=212, width=626, height=32)
                else: #<--- Если пароль менее 4-х символов
                    self.error_message.configure(image=self.images['Too_short_pass'])
                    self.error_message.place(x=455, y=212, width=626, height=32)
            else: #<--- Если введённые пароли разные
                self.error_message.configure(image=self.images['Different_passwords'])
                self.error_message.place(x=455, y=212, width=626, height=32)

    def AdminPanel(self):
        self.admin_panel.delete(0, END);
        for account in accounts:
            nickname, password, balance, history = account;
            self.admin_panel.insert(END, f'[{nickname}] | [{password}] | [{balance}]');
        self.admin_panel.place(x=55, y=165, width=361, height=306);
        self.admin_label.place(x=55, y=472, width=361, height=50)
        self.admin_delete.place(x=55, y=525, width=165, height=40)
        self.new_account_ballance.place(x=228, y=525, width=188, height=36)

    def HiseAdminPanel(self):
        #Убираем админ-панель
        self.admin_panel.place_forget();
        self.admin_label.place_forget();
        self.admin_delete.place_forget();
        self.new_account_ballance.place_forget();

    def focus_out(self, object, message):
        if object.get().lower() not in ('логин', 'пароль', 'повторите пароль', 'новый баланс', ''):
            return None
        object.delete(0, END);
        object.insert(0, message);
        object.configure(fg='gray')
        self.new_account_ballance.configure(fg='white')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~| Подготовка переменных |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
balance = None;
account_index = None;
now_time = None;
current_password = '';
accounts = [];
history = [];


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~| Настройка окна и запуск |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#(Шаг №1) - Загружаем сохранённые аккаунты
Download_accounts();

#(Шаг №2) - Создаём игровое окно рулетки
Roulette = RouletteWindow();

#(Шаг №3) - Создаём окно при проигрыше
EndGame = EndGame();

#(Шаг №4) - Создаём авторизационное окно
Login = LoginIntoAccount()

#(Шаг №5) - Запускаем отслеживание времени
GoTime()

root.title('Казино');
root.geometry('1500x800+200+100');
root.resizable(width=False, height=False)
root.mainloop();