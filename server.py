import sqlite3
import hashlib 
import socket
import threading
import time

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost",9999))

server.listen()


class CinemaTicketSystem:
    def __init__(self):
        self.conn_movies = sqlite3.connect("moviesdata.db")
        self.cur_movies = self.conn_movies.cursor()
        self.conn_user=sqlite3.connect("userdata.db")
        self.cur_user=self.conn_user.cursor()
        self.conn_ticket=sqlite3.connect("ticketsdata.db")
        self.cur_ticket=self.conn_ticket.cursor()
        self.logged_in=False
        self.account=""
    def checkMovie(self, title, year):
        self.cur_movies.execute("SELECT FROM moviesdata (title, year) VALUES (?, ?)",
                                (title, year))
        self.movies = self.cur_movies.fetchall()
        if not self.movies:
            return True
        return False
    def addMovie(self, title, year):
        try:
            self.cur_movies.execute("INSERT INTO moviesdata (title, year) VALUES (?, ?)",
                                (title, year))
            self.conn_movies.commit()
        except:
            return(f"Something went wrong.")

        else:
            return(f"Movie '{title}' added successfully.")

    def showAllMovies(self):
        self.cur_movies.execute("SELECT * FROM moviesdata")
        self.movies = self.cur_movies.fetchall()
        if not self.movies:
            return ("No movies available.")
        else:
            movies=[]
            for movie_id, title, year in self.movies:
                movies.append(f"{movie_id}. {title}, {year}")
            return movies

   
    def addUser(self, username, password):
        try:
            self.cur_user.execute("INSERT INTO userdata (username, password) VALUES (?, ?)",
                                (username, password))
            self.conn_user.commit()
        except:
            return(f"Something went wrong.")

        else:
            return(f"User added successfully.")
            
    def login(self,username,password):
        self.cur_user.execute("SELECT * FROM userdata WHERE username=? AND password=?",(username,password))
        if self.cur_user.fetchall():
            self.account=username
            self.logged_in=True
        else:
            self.logged_in=False

    def buyTicket(self, movie_id):
        self.cur_movies.execute("SELECT * FROM moviesdata")
        self.movies = self.cur_movies.fetchall()
        self.cur_user.execute("SELECT * FROM userdata WHERE username=?",(self.account,))
        self.user=self.cur_user.fetchone()
        user_id,*_=self.user
        
        try:
            self.cur_ticket.execute("INSERT INTO ticketsdata (user_id, movie_id) VALUES (?, ?)",
                               (user_id, movie_id))
            self.conn_ticket.commit()
        except:
            return(f"Something went wrong.")

        else:
            self.cur_ticket.execute("SELECT * FROM ticketsdata WHERE (movie_id,user_id)=(?,?)", (movie_id,user_id))
            self.ticket = self.cur_ticket.fetchone()
            id,*_=self.ticket
            return(f"Ticket bought successfully. Ticket ID is {id}.")

    def cancelTicket(self, ticket_id):
        if ticket_id in self.tickets:
            try:
                self.cur_ticket.execute("DELETE FROM ticketsdata WHERE ticket_id=?",
                                (ticket_id, ))
                self.conn_ticket.commit()
            except:
                return(f"Something went wrong.")

            else:
                return(f"Ticket canceled successfully.")
        return "Ticket not found."
    

    def usernameValid(self,username):
        self.cur_user.execute("SELECT * FROM userdata")
        self.users = self.cur_user.fetchall()
        if username in self.users:
            return False
        return True
    
    def showMyTickets(self,username):
        self.cur_user.execute("SELECT * FROM userdata WHERE username=?", (username,))
        self.user = self.cur_user.fetchone()
        
        if self.user:
            user_id, db_username, password = self.user
            self.cur_ticket.execute("SELECT * FROM ticketsdata WHERE user_id=?", (user_id,))
            self.tickets = self.cur_ticket.fetchall()
            if not self.tickets:
                return("You have no tickets.")
            else:
                tickets=[]
                for ticket in self.tickets:
                    ticket_id, movie_id, *_ = ticket  
                    self.cur_movies.execute("SELECT * FROM moviesdata WHERE id=?", (movie_id,))
                    self.movie = self.cur_movies.fetchone()                    
                    if self.movie:
                        _, title, year = self.movie
                        tickets.append(f"ID: {ticket_id} {title}, {year} - {db_username}")
                return tickets

def handle_connection(c):
    c.send("""
Здравствуйте, у вас есть следующие доступные функции:

1. Войти;
2. Добавить нового пользователя;
3. Показать все доступные фильмы;



    """.encode())

    cinemaSystem=CinemaTicketSystem()

    choice=c.recv(1024).decode()


    if choice =="1":
        c.send("Username: ".encode())
        username=c.recv(1024).decode()
        c.send("Password: ".encode())
        password=c.recv(1024)
        password=hashlib.sha256(password).hexdigest()
        cinemaSystem.login(username,password)
        if cinemaSystem.logged_in:
            c.send("Logged in successfully! Press enter.".encode())
        else: 
            c.send("Login failed. Press enter.".encode())
        
        

        
    
    elif choice == "3":
        if isinstance(cinemaSystem.showAllMovies(), list):
            c.send('\n'.join(cinemaSystem.showAllMovies()).encode())
        else:
            c.send(cinemaSystem.showAllMovies().encode())
    
    elif choice=="2":
        c.send("Username: ".encode())
        username=c.recv(1024).decode()
        while not cinemaSystem.usernameValid(username): 
            c.send("Seems the username is already taken. Try new one: ".encode())
            username=c.recv(1024).decode()
        c.send("Enter your password: ".encode())
        pass1=c.recv(1024)
        pass1=hashlib.sha256(pass1).hexdigest()
        c.send("Enter your password again: ".encode())
        pass2=c.recv(1024)
        pass2=hashlib.sha256(pass2).hexdigest()
        while not pass1==pass2:
            c.send("Entered passwords are different. Try again: ".encode())
            pass1=c.recv(1024)
            pass1=hashlib.sha256(pass1).hexdigest()
            c.send("Enter your password again: ".encode())
            pass2=c.recv(1024)
            pass2=hashlib.sha256(pass2).hexdigest()

        c.send(cinemaSystem.addUser(username,pass1).encode())
        cinemaSystem.login(username,pass1)
        
    else:
        c.send("Данной функции не существует.".encode())
        
        


    if cinemaSystem.logged_in:
        c.send("""
Здравствуйте, у вас есть следующие доступные функции:

1. Показать все доступные фильмы;
2. Посмотреть мои билеты;
3. Купить билет;
4. Отменить покупку билета;
5. Добавить новый фильм;




    """.encode())

    choice=c.recv(1024).decode()
    print(f"Received choice: {choice}") 
    if choice =="1":
        if isinstance(cinemaSystem.showAllMovies(), list):
            c.send('/n'.join(cinemaSystem.showAllMovies()).encode())
    elif choice=="2":
        
        if isinstance(cinemaSystem.showMyTickets(username), list):
            c.send('\n'.join(cinemaSystem.showMyTickets(username)).encode())
        else:
            c.send(cinemaSystem.showAllMovies())    
    elif choice=="3":
        c.send("Enter movie id: ".encode())
        movie_id=c.recv(1024).decode()
        c.send(cinemaSystem.buyTicket(movie_id).encode())
    elif choice =="4":
        c.send("Enter ticket id: ".encode())
        ticket_id=c.recv(1024).decode()
        c.send(cinemaSystem.cancelTicket(ticket_id).encode())
    elif choice=="5":
        c.send("Movie title: ".encode())
        title=c.recv(1024).decode()
        c.send("Release year: ".encode())
        year=c.recv(1024).decode()
        if year.isdigit():
            c.send(cinemaSystem.addMovie(title, int(year)).encode())
        else:
            c.send("Invalid year input. Please enter a valid number.".encode())

    else:
        c.send("Данной функции не существует.".encode())



while True:
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args=(client,)).start()

