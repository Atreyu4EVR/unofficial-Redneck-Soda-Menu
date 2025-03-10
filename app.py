import os
import csv
from flask import Flask, render_template, send_file
from collections import defaultdict

app = Flask(__name__)

def get_menu_from_csv():
    menu = {
        'drinks': defaultdict(list),
        'energy_drinks': defaultdict(list),
        'waters': defaultdict(list),
        'sodas': defaultdict(list),
        'syrups': defaultdict(list),
        'sugar_free_syrups': defaultdict(list),
        'purees': defaultdict(list),
        'creams': defaultdict(list),
        'treats': {
            'hillbilly_rounds': {
                'size': '',
                'options': ''
            },
            'cookies': {
                'size': '',
                'flavors': ''
            },
            'ice_cream': {
                'serving': '',
                'flavors': ''
            }
        }
    }
    
    current_category = None
    
    try:
        with open('menu.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row if present
            
            for row in reader:
                if not row:  # Skip empty rows
                    continue
                    
                # Assuming CSV columns: Category, Name, Ingredients, Base
                category = row[0].strip() if len(row) > 0 else current_category
                name = row[1].strip() if len(row) > 1 else ""
                ingredients = row[2].strip() if len(row) > 2 else ""
                base = row[3].strip() if len(row) > 3 else "Regular"
                
                if not category:  # Skip rows without category
                    continue
                    
                current_category = category
                category_lower = category.lower()
                
                # Handle treats specially
                if 'treats' in category_lower:
                    if name.lower() == 'hillbilly rounds':
                        menu['treats']['hillbilly_rounds']['size'] = ingredients
                        menu['treats']['hillbilly_rounds']['options'] = 'Choose Cookie & Ice Cream Flavor'
                    elif name.lower() == 'cookies':
                        menu['treats']['cookies']['size'] = ingredients
                        menu['treats']['cookies']['flavors'] = base
                    elif name.lower() == 'ice cream':
                        menu['treats']['ice_cream']['serving'] = ingredients
                        menu['treats']['ice_cream']['flavors'] = base
                # Handle other categories
                elif 'redneck drinks' in category_lower:
                    menu_section = menu['drinks']
                    menu_section[base].append({
                        "name": name,
                        "ingredients": ingredients
                    })
                elif 'redneck energy' in category_lower:
                    menu_section = menu['energy_drinks']
                    menu_section[base].append({
                        "name": name,
                        "ingredients": ingredients
                    })
                elif 'redneck water' in category_lower:
                    menu_section = menu['waters']
                    menu_section[base].append({
                        "name": name,
                        "ingredients": ingredients
                    })
                elif 'sodas' in category_lower:
                    menu_section = menu['sodas']
                    menu_section[base].append({
                        "name": name,
                        "ingredients": ingredients
                    })
                elif 'syrup flavors' in category_lower:
                    menu_section = menu['syrups']
                    menu_section[base].append({
                        "name": name,
                        "ingredients": ingredients
                    })
                elif 'sugar free syrups' in category_lower:
                    menu_section = menu['sugar_free_syrups']
                    menu_section[base].append({
                        "name": name,
                        "ingredients": ingredients
                    })
                elif 'purees' in category_lower:
                    menu_section = menu['purees']
                    menu_section[base].append({
                        "name": name,
                        "ingredients": ingredients
                    })
                elif 'creams' in category_lower:
                    menu_section = menu['creams']
                    menu_section[base].append({
                        "name": name,
                        "ingredients": ingredients
                    })
                    
    except FileNotFoundError:
        print("Error: menu.csv file not found")
        return menu
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return menu
        
    return menu

@app.route('/favicon.svg')
def favicon():
    return send_file('static/favicon.svg', mimetype='image/svg+xml')

@app.route('/')
def menu():
    menu_data = get_menu_from_csv()
    return render_template('menu.html', menu=menu_data)

@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')

def generate_static_site():
    menu_data = get_menu_from_csv()
    with app.app_context():
        # Generate main menu page
        rendered_menu = render_template('menu.html', menu=menu_data)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(rendered_menu)
            
        # Generate disclaimer page
        rendered_disclaimer = render_template('disclaimer.html')
        with open('disclaimer.html', 'w', encoding='utf-8') as f:
            f.write(rendered_disclaimer)

    print("Static site generated as index.html and disclaimer.html")

if __name__ == '__main__':
    generate_static_site()