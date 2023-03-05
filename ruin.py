import argparse
import requests
import random


def get_heroes():
    heroes = requests.get("https://api.opendota.com/api/heroes").json()
    return [{"name": hero["localized_name"], "id": hero["id"], 
             "primary_attr": hero["primary_attr"], 
             "attack_type": hero["attack_type"], 
             "roles": hero["roles"]} for hero in heroes]

def get_random_hero(primary_attr=None, attack_type=None, roles=None, banned=None):
    heroes = get_heroes()
    set_hero = set(i['name'] for i in heroes)
    set_roles = set(j for i in heroes for j in i['roles'])
    set_attack_type = set(i['attack_type'] for i in heroes)
    set_primary_attr = set(i['primary_attr'] for i in heroes)
    
    if banned:
        banned = set(banned.split(","))
        if banned.issubset(set_hero):
            heroes = [hero for hero in heroes if hero["name"] not in banned]
        else:
            print("Неверные имена героев" + '\n' + "Пробелы в именах экранируются через \\")
            exit()
            
    if primary_attr:
        if primary_attr in set_primary_attr:
            heroes = [hero for hero in heroes if hero["primary_attr"] == primary_attr]
        else:
            print('Неверное имя атрибута')
            exit()
            
    if attack_type:
        if attack_type in set_attack_type:
            heroes = [hero for hero in heroes if hero["attack_type"] == attack_type]
        else:
            print('Неверный тип атаки')
            exit()
            
    if roles:
        roles = set(roles.split(","))
        if roles.issubset(set_roles):
            heroes = [hero for hero in heroes if set(roles).issubset(set(hero["roles"]))]
        else:
            print('Неверные роли')
            exit()
            
    return random.choice(heroes)


def get_random_boots():
    items = requests.get("https://api.opendota.com/api/constants/items").json()
    boots_list = []
    
    for item in items:
        try:
            item_name = items[item]['dname']
            if (
                item_name.find('Boot') > -1
                or item_name == 'Power Treads'
                or item_name == 'Guardian Greaves'
            ) and item_name.find('Recipe') == -1 and item_name != 'Boots of Speed':
                boots_list.append(item_name)
        except Exception:
            continue
            
    return random.choice(boots_list)


def get_item_types():
    url = "https://api.opendota.com/api/constants/items"
    response = requests.get(url)
    items = response.json()
    set_items_qual = set()
    
    for item in items:
        try:
            set_items_qual.add(items[item]['qual'])
        except:
            continue
            
    return set_items_qual


def get_random_items(n=5, min_cost=3200, max_cost=10000, types=None):
    url = "https://api.opendota.com/api/constants/items"
    response = requests.get(url)
    items = response.json()
    items_list = []
    set_items_qual = get_item_types()
    
    if types is not None and not set(types).issubset(set_items_qual):
        print('you loh')
        exit()
        
    for item in items:
        try:
            cost = items[item]['cost']
            item_type = items[item]['qual']
            if cost >= min_cost and cost <= max_cost and (types is None or item_type in types):
                items_list.append(items[item]['dname'])
        except Exception:
            continue
            
    return random.sample(items_list, n)


def get_random_line():
    return random.choice(['Bot', 'Mid', 'Top', 'Forest', 'Roam'])


def get_random_role():
    return random.choice(['Support', 'Core'])


def main():
    parser = argparse.ArgumentParser(description='Колесо фортуны', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--hero', action='store_true', help='Выбор случайного героя')
    parser.add_argument('--boots', action='store_true', help='Выбор случайного ботинка')
    parser.add_argument('--items', nargs='?', const='5,3200,10000', type=str, 
                        help='Выбор случайных предметов (по умолчанию 5 предметов дороже 3200 голды)')
    parser.add_argument('--line', action='store_true', help='Выбор случайной линии')
    parser.add_argument('--role', action='store_true', help='Выбор случайной роли')
    parser.add_argument('--all', action='store_true', help='Случайно генерирует абсолютно все')
    parser.add_argument('--items_type', type=str, help='Редкость предметов через запятую')
    parser.add_argument('--primary_attr', type=str, help='Выбор основного атрибута героя')
    parser.add_argument('--attack_type', type=str, help='Выбор типа атаки героя')
    parser.add_argument('--roles', type=str, help='Выбор ролей героя через запятую')
    parser.add_argument('--banned', type=str, help='Указание запрещенных героев через запятую')
    
    heroes = get_heroes()
    set_items_qual = get_item_types()
    set_hero = set(i['name'] for i in heroes)
    set_roles = set(j for i in heroes for j in i['roles'])
    set_attack_type = set(i['attack_type'] for i in heroes)
    set_primary_attr = set(i['primary_attr'] for i in heroes)
        
    parser.epilog = f"  Список ролей: {', '.join(set_roles)}." + "\n\n" + f"  Список типов атаки: {', '.join(set_attack_type)}." + "\n\n" + f"  Список основных атрибутов: {', '.join(set_primary_attr)}." + "\n\n" + f"  Список качеств предметов: {', '.join(set_items_qual)}." + "\n\n" + f"  Список героев: {', '.join(set_hero)}." 
   
    args = parser.parse_args()
    
    
    item_types = None
    if args.items_type:
        item_types = args.items_type.split(",")
    
    if args.hero or args.all:
        heroes = set()
        counter = 1
        while True:
            hero = get_random_hero(primary_attr=args.primary_attr, attack_type=args.attack_type, roles=args.roles, banned=args.banned)['name']
            heroes.add(hero)
            if len(heroes) == 3:
                break
        for hero in heroes:
            print(f'Random hero {counter}: {hero}')
            counter += 1
            
    if args.boots or args.all:
        print(f"Random boots: {get_random_boots()}")

    if args.items is not None or args.all: 
        if args.items:
            items = args.items.split(",")
            items = [int(item) if item.isdigit() else item for item in items]
            items_count = items[0]
            min_cost = items[1] if len(items) > 1 else 3200
            max_cost = items[2] if len(items) > 2 else 10000
        else:
            items_count, min_cost, max_cost = 5, 3200, 10000
        items_list = get_random_items(n=items_count, min_cost=min_cost, max_cost=max_cost, types=item_types)
        print(f"Random items: {', '.join(items_list)}")

    if args.line or args.all:
        print(f"Random line: {get_random_line()}")

    if args.role or args.all:
        print(f"Random role: {get_random_role()}")

    if not any(vars(args).values()):
        parser.print_help()


if __name__ == '__main__':
    main()
