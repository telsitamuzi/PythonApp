select state, age, sum(price)
from Sales F, Store S, customer a
where F.storeID = S.storeID && F.custID = a.custID
group by state, age;

select state, i.color, age, sum(price)
from Sales F, Store S, customer a, item i 
where F.storeID = S.storeID && F.custID = a.custID && i.itemID = F.itemID
group by state, age, i.color;

select state, i.color, age, i.category, sum(price)
from Sales F, Store S, customer a, item i 
where F.storeID = S.storeID && F.custID = a.custID && i.itemID = F.itemID
group by state, age;

select state, i.color, age, i.category, sum(price)
from Sales F, Store S, customer a, item i 
where F.storeID = S.storeID && F.custID = a.custID && i.itemID = F.itemID && i.color = 'blue'
group by state, age, i.color;

select i.color, age, sum(price)
from Sales F, Store S, customer a, item i 
where F.storeID = S.storeID && F.custID = a.custID && i.itemID = F.itemID
group by age, i.color;


























select i.color, age, sum(price)
from sales f, store s, customer a, item i
where f.storeID = s.storeID && f.custID = a.custID && i.itemID = F.itemID
group by age, i.color


