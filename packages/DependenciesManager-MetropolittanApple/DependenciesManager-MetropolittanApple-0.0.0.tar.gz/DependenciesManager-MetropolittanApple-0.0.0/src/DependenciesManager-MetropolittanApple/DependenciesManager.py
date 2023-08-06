import os
from colorama import Fore

def init_dependencies(DEPENDENCIES, PRODUCT_NAME, VERSION = '1.0.0'):
    print(f" └─Running {PRODUCT_NAME} ")
    print(f"     └─Version: {VERSION}")

    for dependency in DEPENDENCIES:
        try:
            print('     --------------------')
            os.system(f"pip install {dependency}")
            
            for i in range(0,12):
                print()

            print('     --------------------')
        
        except: 
            print(f"Error: Couldn't install {dependency}. ")
            print(f" ▶ SOLUTION: 'pip install {dependency}'") 
            quit()

    print("     └─Errors:",Fore.GREEN + "None", Fore.RESET)
    print("     └─Dependencies:",Fore.GREEN + "✓", Fore.RESET)
