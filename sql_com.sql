insert into orders (title, description, status, is_paid, phone, created_at, updated_at)
values ('test2', 'descr2', 'В работе', false, 79278947467, NOW(), now());

select * from users;


insert into orders (title, description, status, is_paid, phone, created_at, updated_at)
values ('Трах в попку', 'Очко в работе', 'В работе', false, 79178131924, NOW(), now());

delete from users where phone = '79178131924';
delete from users where phone = '79278947467'
delete from orders where phone = '79278947467';

insert into orders (title, description, status, is_paid, phone, created_at, updated_at)
values ('Руль сделать', 'Руль в говне', 'В работе', false, 79871632838, NOW(), now());