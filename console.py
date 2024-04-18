#!/usr/bin/python3
"""a program called console.py that contains
the entry point of the command interpreter
"""

import cmd
import re
from models.base_model import BaseModel
from models.user import User
from models.review import Review
from models.state import State
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.place import Place
import json
from models import storage

classes = {"BaseModel": BaseModel,
           "User": User,
           "Review": Review,
           "State": State,
           "City": City,
           "Place": Place,
           "Amenity": Amenity}
regex = [r'^(\w+)\.(\w+)\(\)$',
         r'^(\w+)\.(\w+)\("(.*?)",\s"(.*?)",\s(".*?")\)$',
         r'^(\w+)\.(\w+)\("(.*?)"\)$',
         r'^(\w+)\.(\w+)\("(.*?)",\s"(.*?)",\s([0-9]*?)\)$']


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def precmd(self, line):
        """Execute befor the onecmd"""
        match = None
        index = 0
        while match is None and index < len(regex):
            match = re.match(regex[index], line)
            index += 1
        if match and index == 1:
            tmp_list = list(match.groups())
            tmp_list.reverse()
            line = " ".join(tmp_list)
        elif match and index == 3:
            tmp_list = list(match.groups())
            name = tmp_list[0]
            tmp_list.pop(0)
            tmp_list.insert(1, name)
            line = " ".join(tmp_list)
        elif match and (index == 2 or index == 4):
            tmp_list = list(match.groups())
            name = tmp_list[0]
            tmp_list.pop(0)
            tmp_list.insert(1, name)
            line = " ".join(tmp_list)
        return cmd.Cmd.precmd(self, line)

    def do_create(self, line):
        """Creates a new instance of BaseModel"""
        if not line:
            print("** class name missing **")
            return
        line = line.split(" ")
        attr = []
        count = 1
        while (count < len(line)):
            attr.append(line[count])
            count += 1
        hold = []
        hold.append(line[0])
        line = hold
        if line[0] in classes:
            obj = classes[line[0]]()
            if len(line) == 1:
                line.insert(1, obj.id)
            for mem in attr:
                mem = mem.split('=')
                setattr(obj, mem[0], mem[1][1:-1])
        elif line[0] not in classes:
            print("** class doesn't exist **")
            return
        obj.save()
        print(obj.id)

    def do_show(self, args):
        """prints the string representation of an
        instance based on the class name and id
        """
        if args:
            arg = args.split()
        if not args:
            print("** class name missing **")
            return
        elif arg[0] not in classes:
            print("** class doesn't exist **")
            return
        elif len(arg) == 1:
            print("** instance id missing **")
            return
        else:
            content = storage.all()
            tmp_model = None
            for key, value in content.items():
                if arg[1] == value.to_dict()["id"]:
                    tmp_model = classes[arg[0]](**(value.to_dict()))
            if not tmp_model:
                print("** no instance found **")
                return
            else:
                print(tmp_model)

    def do_destroy(self, args):
        """"
        Deletes an instance based on the class name and
        id (save the change into the JSON file).
        """
        if args:
            arg = args.split()
        if not args:
            print("** class name missing **")
            return
        elif arg[0] not in classes:
            print("** class doesn't exist **")
            return
        elif len(arg) == 1:
            print("** instance id missing **")
            return
        else:
            content = storage.all()
            signal = None
            for key, value in content.items():
                if arg[1] == value.to_dict()["id"]:
                    signal = "yes"
                    key_value = key
            if signal == "yes":
                content.pop(key_value)
            else:
                print("** no instance found **")
                return
            storage.save()

    def do_clear(self, line):
        """clear the screen
        Usage: clear
        """
        import os
        os.system("clear")

    def do_all(self, line):
        """
        Prints all string representation of all
        instances based or not on the class name.
        """
        if not line:
            all_list = []
            content = storage.all()
            for value in content.values():
                all_list.append(classes[value.to_dict()["__class__"]]
                                (**(value.to_dict())).__str__())
        elif line not in classes:
            print("** class doesn't exist **")
            return
        else:
            all_list = []
            content = storage.all()
            for value in content.values():
                if value.to_dict()["__class__"] == line:
                    all_list.append(classes[line]
                                    (**(value.to_dict())).__str__())
        print(all_list)

    def do_update(self, args):
        """
        Updates an instance based on the class name
        and id by adding or updating attribute (
        save the change into the JSON file)
        """
        if args:
            arg = args.split()
        if not args:
            print("** class name missing **")
            return
        elif arg[0] not in classes:
            print("** class doesn't exist **")
            return
        elif len(arg) == 1:
            print("** instance id missing **")
            return
        content = storage.all()
        signal = None
        for value in content.values():
            if arg[1] == value.to_dict()["id"]:
                signal = "yes"
        if not signal:
            print("** no instance found **")
            return
        elif len(arg) == 2:
            print("** attribute name missing **")
            return
        elif len(arg) == 3:
            print("** value missing **")
            return
        else:
            for key, value in content.items():
                if arg[1] == value.to_dict()["id"]:
                    obj = value
                    tmp = arg[3]
                    if (tmp[0] == "\"" or tmp[0] == "\'"):
                        setattr(obj, arg[2], tmp[1:-1])
                    else:
                        if (float(tmp) - int(float(tmp))) == 0:
                            setattr(obj, arg[2], int(tmp))
                        else:
                            setattr(obj, arg[2], float(tmp))
            obj.save()

    def do_EOF(self, line):
        """quit with ctrl-D is presswd"""
        return (True)

    def emptyline(self):
        """Defines what happens when a line is empty"""
        pass

    def default(self, *args):
        """defines what happen whwn the command is not recognized"""
        pass

    def do_count(self, line):
        """retrieve the number of instances of a class:
        <class name>.count()."""
        content = storage.all()
        all_list = []
        for value in content.values():
            if value.to_dict()["__class__"] == line:
                all_list.append(classes[line](**(value.to_dict())).__str__())
        print(len(all_list))


if __name__ == "__main__":
    HBNBCommand().cmdloop()
