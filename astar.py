class Car():
    def __init__(self, nr ,brand):
        self.nr = nr
        self.brand = brand
        self.friends = []

    def set_nr(self, nr):
        self.nr = nr

    def set_brand(self, brand):
        self.brand = brand

    def get_nr(self):
        return self.nr

    def get_brand(self):
        return self.brand

    def add_friend(self, friend):
        self.friends.append(friend)

    def get_friends(self):
        return self.friends

a = Car(44,"a")
car_list_a = [Car(45,"b"),Car(46,"c"),Car(47,"d")]
car_list_b = [Car(48,"d"),Car(49, "e")]

for c in car_list_a:
    a.add_friend(c)
a.add_friend(car_list_b[1])
def change_stuff(car):
    for c in car.get_friends():
        c.set_nr("00")

change_stuff(a)

for c in car_list_a:
    print(c.get_nr())

for c in car_list_b:
    print(c.get_nr())
