from main import ChapterAndPage
from folder import change_path
from time import sleep
import os
import re


def cap_page():
    print("")
    choice = input("Deseja baixar mais de 1 Capítulo?(y/n):\n>>> ").lower()
    print("")
    if choice == "y":
        while True:
            start = input("Do capítulo: ")
            start = re.sub("^0+(?!$)", "", start)
            end = input("a: ")
            end = re.sub("^0+(?!$)", "", end)
            os.system("cls")
            if start.isdigit() and end.isdigit():
                print(f"Baixar capítulos Do {start} a {end}?")
                choice = input("(y/n):>>> ").lower()
                print("")
                if choice == "y":
                    system.choice_chapter(start=start, end=end)
                    system.image_downloader()
                    os.system("cls")
                    print("\033[32mDownload Concluido\033[0m")
                    sleep(1)
                    break
                elif choice == "n":
                    os.system("cls")
                    pass
                else:
                    os.system("cls")
                    print("\033[31mOpção invalida\033[0m")
                    sleep(2)
                    os.system("cls")
            else:
                os.system("cls")
                print("\033[31mOpção invalida\033[0m")
                sleep(2)
                os.system("cls")
    elif choice == "n":
        num = input("Qual capítulo deseja baixar?\n>>> ")
        if num.isdigit():
            system.choice_chapter(num=num)
            system.image_downloader()
            os.system("cls")
            print("\033[32mDownload Concluido\033[0m")
            sleep(1)
        else:
            os.system("cls")
            print("\033[31mOpção invalida\033[0m")
            sleep(1)
            os.system("cls")
    else:
        os.system("cls")
        print("\033[31mOpção invalida\033[0m")
        sleep(1)
        os.system("cls")


while True:
    os.system("cls")
    print("+---------------------------+")
    print("|     Tipos de Busca        |")
    print("+---------------------------+")
    print("|   1 - Nome do Mangá       |")
    print("|   2 - Procurar Mangá      |")
    print("|   3 - Local da Pasta      |")
    print("|   4 - Sair                |")
    print("+---------------------------+")
    print("")
    try:
        system = ChapterAndPage()
        choice = int(input("Digite a opção desejada: "))
        print("")
        if choice == 1:
            os.system("cls")
            name = input("Digite o nome do mangá:\n>>> ")
            system.find_and_create_slug(slug_manga=name)
            cap_page()
        elif choice == 2:
            name = input("Digite o nome do mangá:\n>>> ")
            os.system("cls")
            system.find_and_create_slug(title=name)
            cap_page()
        elif choice == 3:
            print('Deseja adicionar um novo local para salvar os mangás?')
            y_n = input('(y/n)>>> ').lower()
            if y_n == 'y':
                change_path()
                os.system('cls')
                print('\033[32mLocal para salvamentos adicionado com sucesso\033[0m')
                sleep(2)
            elif y_n == 'n':
                pass
            else:
                os.system("cls")
                print("\033[31mOpção invalida\033[0m")
                sleep(1)
                os.system("cls")
        elif choice == 4:
            os.system("cls")
            for i in range(4):
                print("\033[31mEncerrando\033[0m" + "\033[31m.\033[0m" * i, end="")
                sleep(0.6)
                print("   ", end="\r")
            sleep(0.7)
            os.system("cls")
            break
        else:
            os.system("cls")
            print("\033[31mOpção invalida\033[0m")
            sleep(1)
            system("cls")

    except ValueError:
        os.system("cls")
        print("\033[31mOpção invalida\033[0m")
        sleep(1)
        os.system("cls")
