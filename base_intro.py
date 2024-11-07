from peewee import *
from faker import Faker
from random import randint

if __name__ == "__main__":
    db = SqliteDatabase('database.sqlite')

    class Person(Model): 
        first_name = CharField(max_length=50)
        last_name = CharField(max_length=50)
        birth_date = DateField(default="2000-06-08")
        gender= SmallIntegerField()
        job = CharField(max_length=50)
        email = CharField(max_length=100)

        class Meta: 
            database = db

    class Telephone(Model):
        number = CharField(max_length=50)
        owner = ForeignKeyField(Person, null=True, backref="telephones")
        model = CharField(max_length=80)
        ram_size = SmallIntegerField()

        def __str__(self):
            return f"Telephone ({self.get_id()}) : {self.number}"

        class Meta:
            database = db
        
    db.connect() 
    db.create_tables([Person, Telephone], safe=True)

    john= Person(first_name= 'John', last_name="last", gender=0, job='hitman', email='jdoe@gmail.com')
    john.save()
    Person.create(first_name= 'John', last_name="last", gender=0, job='hitman', email='jdoe@gmail.com')

    # Utiliser Faker pour générer des données
    faker = Faker()

    # Ajouter des personnes
    person = Person(
        first_name=faker.first_name(), 
        last_name=faker.last_name(), 
        gender=randint(0, 1), 
        job=faker.job(), 
        email=faker.email(), 
        birth_date=faker.date_of_birth(minimum_age=18, maximum_age=99)
    )
    person.save()

    for individual in Person.select().where(Person.birth_date > "1990-01-01" & Person.birth_date <"2000-06-07"): 
        print(individual.birth_date)

    owner = Person.select().order_by(fn.RANDOM()).get()
    phone1 = Telephone.create(
        number=faker.phone_number(),
        owner=owner,
        model=f"iPhone {randint(1, 15)}",
        ram_size=randint(1, 32)
    )

    # Lister les téléphones de la base
    for telephone in Telephone.select():
        print(telephone, telephone.owner)