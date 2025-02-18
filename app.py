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
        'sodas': [],
        'syrups': [],
        'sugar_free_syrups': [],
        'purees': [],
        'creams': []
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
                base = row[3].strip() if len(row) > 3 else ""
                
                if not category:  # Skip rows without category
                    continue
                    
                current_category = category
                category_lower = category.lower()
                
                if 'redneck drinks' in category_lower:
                    menu_section = menu['drinks']
                elif 'redneck energy' in category_lower:
                    menu_section = menu['energy_drinks']
                elif 'redneck water' in category_lower:
                    menu_section = menu['waters']
                elif 'sodas' in category_lower:
                    menu['sodas'].append(name)
                elif 'syrup flavors' in category_lower:
                    menu['syrups'].append(name)
                elif 'sugar free syrups' in category_lower:
                    menu['sugar_free_syrups'].append(name)
                elif 'purees' in category_lower:
                    menu['purees'].append(name)
                elif 'creams' in category_lower:
                    menu['creams'].append(name)
                else:
                    continue
                    
                if isinstance(menu_section, defaultdict) and name:
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

def generate_static_site():
    menu_data = get_menu_from_csv()
    with app.app_context():
        rendered = render_template('menu.html', menu=menu_data)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(rendered)

if __name__ == '__main__':
    generate_static_site()
    print("Static site generated as index.html")