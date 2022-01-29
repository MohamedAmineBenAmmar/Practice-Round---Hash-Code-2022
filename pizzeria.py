from collections import OrderedDict
import re
import os


def remove_undesired_characters(string):
    return re.sub('\s+', ' ', string).rstrip()


def set_keys(my_dict, keys):
    for key in keys:
        my_dict[key] = True


def extract_data(file_path):
    with open(file_path) as f:
        n = remove_undesired_characters(f.readline())
        ingredients = OrderedDict()
        clients_likes_dislikes = []
        index = 1
        flag = 1
        for line in f:
            tmp_line = remove_undesired_characters(line)
            tmp_line = tmp_line.split(' ')
            del tmp_line[0]

            # Inserting the clients likes and dislikes
            if flag % 2 != 0:
                # Handling the clients likes
                client_likes = {}
                set_keys(client_likes, tmp_line)
                # clients_likes_dislikes.append({"likes": [*tmp_line]})
                clients_likes_dislikes.append({"likes": client_likes})
            else:
                client_dislikes = {}
                set_keys(client_dislikes, tmp_line)
                # clients_likes_dislikes[(int(flag / 2)) -1]['dislikes'] = [*tmp_line]
                clients_likes_dislikes[(int(flag / 2)) -1]['dislikes'] = client_dislikes

            flag += 1

            for i in range(0, len(tmp_line)):
                # Insert the ingredients in the ingredients dict
                if not tmp_line[i] in ingredients:
                    ingredients[tmp_line[i]] = index
                    index += 1

    return {
        "clients_number": n,
        "clients_likes_dislikes": clients_likes_dislikes,
        "ingredients": ingredients
    }


def truth_table_constructor(max_power):
    truth_table = []

    bites = []
    occ = []
    for i in range(1, max_power + 1):
        bites.append(0)
        occ.append(0)


    for i in range(1, pow(2, max_power) + 1):        
        truth_table.append([*bites])
        for j in range(0, len(occ)):
            occ[j]+= 1

            if occ[j] == pow(2, j):
                if bites[j] == 0:                    
                    bites[j] = 1
                else:
                    bites[j] = 0

                occ[j] = 0
             

    return truth_table


def display_truth_table(truth_table):
    for truth_table_line in truth_table:
        print(truth_table_line)


def clients_optimization(data):
    ingredients = data['ingredients']
    clients_likes_dislikes = data['clients_likes_dislikes']
    ingredients_list_keys = list(ingredients.keys())    
    ingredients_list_values = list(ingredients.values())
    max_ingredient_index = ingredients_list_values[len(ingredients_list_values) - 1]

    truth_table = truth_table_constructor(max_ingredient_index)
    # display_truth_table(truth_table)

    pizza_ingredients = []
    ncmax = 0
    # for truth_table_line in truth_table:        
    for i in range(1, len(truth_table)) :        
        truth_table_line = [*truth_table[i]]

        tmp_ncmax = 0     
        tmp_pizza_ingredients = []

        for client_likes_dislikes in clients_likes_dislikes:
            client_ingredient_satisfaction = True

            for ingredient_index in range(0, len(truth_table_line)):
                if truth_table_line[ingredient_index] == 1:
                    if not ((ingredients_list_keys[ingredient_index] in client_likes_dislikes['likes'] 
                        and ingredients_list_keys[ingredient_index] not in client_likes_dislikes['dislikes'])
                        or ( (ingredients_list_keys[ingredient_index] not in client_likes_dislikes['likes']) 
                        and (ingredients_list_keys[ingredient_index] not in client_likes_dislikes['dislikes'])  ) ):

                        client_ingredient_satisfaction = False
                        break

            if client_ingredient_satisfaction == True:
                tmp_ncmax+= 1
                tmp_pizza_ingredients = [*truth_table_line]

                    

        if tmp_ncmax >= ncmax:
            ncmax = tmp_ncmax
            pizza_ingredients = [*tmp_pizza_ingredients]
            # print(pizza_ingredients)
            # print("test \n")
            # input()

        # print('yo')
        # print()
        # input()

    
    pizza_ingredients_names = []
    for i in range(0, len(pizza_ingredients)):
        if pizza_ingredients[i] == 1:
            pizza_ingredients_names.append(ingredients_list_keys[i])
    
    output = {
        'max_clients_number': ncmax,
        'pizza_ingredients': pizza_ingredients_names
    }

    return output


def load_data(file_path, data):
    with open(file_path, 'w') as f:
        for item in data:
            f.write(item)
            f.write(' ')


def format_data(data):
    return [str(len(data)), *data]

def wrapper(input_directory_path, output_directory_path):

    for root, dirs, files in os.walk(input_directory_path):
        for filename in files:
            # print(os.path.join(root, filename))
            # print(filename)
            data = extract_data(os.path.join(root, filename))
            output = clients_optimization(data)
            formatted_output = format_data(output['pizza_ingredients'])
            load_data(os.path.join(output_directory_path, "output_" + filename), formatted_output)


   
if __name__ == '__main__':
    # data = extract_data('Sample_Input.txt')
    # print(data)
    # output = clients_optimization(data)
    # print(output)
    input_directory_path = 'test_cases'
    output_directory_path = 'output'
    wrapper(input_directory_path, output_directory_path)
