class Person :
    def __init__(self,name):
        self.name =name 
    def talk(self) :
        print(f'my name is {self.name}')


john = Person('john smith')        

john.talk()

