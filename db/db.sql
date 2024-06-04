use fcds;
create table students(
ID int not null unique auto_increment,
Name varchar(20) not null,
CGPA float not null,
Credit_Hours int not null,
UserName varchar(20) not null,
constraint students_ID_pk primary key(ID),
constraint unique_UserName unique(Username)

);
create table login(
UserName varchar(20) not null,
password varchar(30) not null,
constraint login_UserName_pk primary key(UserName),
constraint foreign key(UserName) references students(UserName) on delete cascade
);
