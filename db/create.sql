create table Address(
  id integer NOT  NULL ,
  id_customer integer NOT NULL ,
  street varchar(20),
  city varchar(20),
  country varchar(20),
  NoApp integer,
  CP varchar(10),
  PRIMARY KEY (id, id_customer)
);

create table Customer(
  id integer PRIMARY KEY ,
  first_name varchar(20),
  last_name varchar (20),
  gender char(1) CHECK (gender IN ('M', 'F')),
  phone varchar(20),
  email varchar(30),
  FOREIGN KEY (id) REFERENCES Address(id_customer)
);

create TABLE Account(
  id integer Primary Key,
  is_closed Boolean,
  open Date,
  closed Date,
  FOREIGN KEY (id) REFERENCES Address(id_customer)
);

create table WebUser(
  username varchar(20) PRIMARY KEY ,
  state varchar(20) CHECK (state IN ('New', 'Active', 'Blocked', 'Banned')),
  salt integer,
  hash_password integer,
  id_customer integer,
  FOREIGN KEY (id_customer) REFERENCES Customer(id)
  ON DELETE NO ACTION
  ON UPDATE CASCADE

);

create table 'Order'(
  id integer PRIMARY KEY ,
  id_account integer,
  ordered Date UNIQUE,
  shipped Date,
  total Real,
  status varchar(20),
  CHECK (status IN ('New', 'Hold', 'Shipped', 'Delivered', 'Closed')),
  FOREIGN KEY (id_account) REFERENCES Account(id)
  ON DELETE NO ACTION
  ON UPDATE CASCADE

);

create table Payment(
  id integer PRIMARY KEY ,
  id_order integer,
  id_account integer,
  paid Date,
  total REAL,
  details varchar(20),
  FOREIGN KEY (id_order)  REFERENCES 'Order'(id)
  ON DELETE CASCADE
  ON UPDATE CASCADE ,

  FOREIGN KEY (id_account) REFERENCES Account(id)
  ON DELETE NO ACTION
  ON UPDATE CASCADE

);

create table ShoppingCart(
  id PRIMARY KEY ,
  created DATE
);

create table LineItem(
  id PRIMARY Key,
  quantity integer,
  price REAL
);

create table Product(
  id integer PRIMARY KEY ,
  original_title varchar(20),
  overview varchar(50),
  vote_average varchar(10),
  backDrop varchar(100),
  category varchar(20),
  trending integer,
  watched integer
);

create table Sessions (
  id integer primary key,
  id_session varchar(32),
  username varchar(25)
);

insert into Product VALUES (1,'blue hat','a beautiful blue hat', '1','http://i66.tinypic.com/xg00mb.jpg','hat',1,1);
insert into Product VALUES (2,'blue scarf','a beautiful blue scarf', '2','http://i65.tinypic.com/2q0luo7.jpg','scarf',2,2);
insert into Product VALUES (3,'blue sweater','a beautiful blue sweater', '3','http://i63.tinypic.com/53a26f.jpg','sweater',3,3);
insert into Product VALUES (4,'scarf','a scarf from hell', '4','http://i66.tinypic.com/20kbo8x.jpg','scarf',1,4);
insert into Product VALUES (5,'peru_landscape','its so beautiful', '5','http://i66.tinypic.com/11vgoz9.jpg','other',1,5);
insert into Product VALUES (6,'native_spinning','thats my dream', '6','http://i64.tinypic.com/2vafmt2.jpg','other',1,6);

insert into Product VALUES (7,'beige hat','look at a beige hat', '1','http://i63.tinypic.com/xoe3ap.jpg','hat',3,7);
insert into Product VALUES (8,'beige2_hat','another beige hat wooow', '2','http://i66.tinypic.com/9gwlj8.jpg','hat',3,8);
insert into Product VALUES (9,'blue3 hat','this is so cool', '3','http://i65.tinypic.com/124it76.jpg','hat',3,9);
insert into Product VALUES (10,'blue hat jpeg','vaya!!', '4','http://i63.tinypic.com/25usj9t.jpg','hat',3,10);
insert into Product VALUES (11,'blue beenie hat','rastaman', '5','http://i64.tinypic.com/29vdw04.jpg','hat',3,11);
insert into Product VALUES (12,'dark blue hat','bangaram', '6','http://i68.tinypic.com/vr6ey9.jpg','hat',4,12);

insert into Product VALUES (13,'beige scarf','so sexy', '1','http://i66.tinypic.com/20kbo8x.jpg','scarf',1,13);
insert into Product VALUES (14,'white gloves','torride', '1','http://i63.tinypic.com/hwxyrn.jpg','gloves',1,14);
insert into Product VALUES (15,'pruple hat','nice', '6','http://i67.tinypic.com/30ndr15.jpg','hat',4,15);
insert into Product VALUES (16,'red hat','navidad!!', '5','http://i64.tinypic.com/29nezo3.jpg','hat',4,16);

insert into Address VALUES (1,1,'beaubien','st-bruno','can', 0,'J3v2v8');
insert into Customer VALUES (1,'ju','ju','M','450-111-1111','ju@ju.com');
-- insert into WebUser VALUES ('ju','ju','New', 1,1);

select * from Product;
select * from Address;
SELECT * from WebUser;