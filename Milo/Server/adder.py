import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import json
from PIL import Image
import re



widgets = []
selected = 0
def get_last_pet_info_id(directory='files'):
    max_id = 0  # Initialize max_id to keep track of the highest number found
    pattern = re.compile(r'pet_info_(\d+)')  # Regular expression pattern to match 'pet_info_<number>'

    # Loop through the files in the specified directory
    for filename in os.listdir(directory):
        match = pattern.match(filename)  # Check if the filename matches the pattern
        if match:
            # Extract the numeric part and convert it to an integer
            pet_id = int(match.group(1))
            max_id = max(max_id, pet_id)  # Update max_id if a larger number is found

    return max_id 

def open_temporary_window(widgets , placeholder, selected):#touple with the 

    temp_window = tk.Toplevel(root)
    temp_window.title("ERROR")
    temp_window.geometry("300x300")
    
    # Set the window to stay on top
    temp_window.attributes("-topmost", True)
    textt = ""
    if selected == 0:
        textt = textt + "Imagine neselectata \n"
        
    for widTxt, idd in widgets:
        if widTxt == placeholder:
            textt = textt + f"{widTxt} | Element Neschimbat \n"
        elif idd == 1:#letter
            textt = textt + f"{widTxt} | Elemente lipsa / Numere prezente \n"
        elif idd == 2:#number
            textt = textt + f"{widTxt} | Elemente lipsa / Litere prezente\n"
        elif idd == 3:#entryis
            textt = textt + f"{widTxt} Optiune neselectata \n"
    tk.Label(temp_window, text=textt).pack(pady=5)

    close_button = tk.Button(temp_window, text="Close", command=temp_window.destroy)
    close_button.pack()




def get_pet_info_files(directory='files'):
    # Initialize a list to hold the names of the pet info files
    pet_info_files = []

    # Loop through the directory
    for filename in os.listdir(directory):
        # Check if the file is a JSON file and matches the pattern
        if filename.startswith("pet_info_") and filename.endswith(".json"):
            pet_info_files.append(filename)  # Add the filename to the list

    return pet_info_files





def on_focus_in(entry, placeholder_text):
        
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)  
            entry.config(fg='black')  



def on_focus_out(entry, placeholder_text):
        if entry.get() == "":
            entry.insert(0, placeholder_text)  # Re-insert the placeholder text
            entry.config(fg='grey')  

def get_next_id():

    existing_files = [f for f in os.listdir("files/") if f.startswith("pet_info_") and f.endswith(".json")]
    ids = [int(f.split("_")[2].split(".")[0]) for f in existing_files if f.split("_")[2].split(".")[0].isdigit()]
    return max(ids) + 1 if ids else 1
    

btnList = []





def deleteJsonBtnCmd(pet_id,temp_window):

    global btnList
    maxJsonId = get_last_pet_info_id()
    print(f"idul jsonului este = {pet_id}")
    directory = "files"
    json_file = f'pet_info_{pet_id}.json'
    image_file_patterns = [f'image_{pet_id}_1.jpg', f'image_{pet_id}_2.jpg', f'image_{pet_id}_3.jpg', f'image_{pet_id}_4.jpg' , f'image_{pet_id}_5.jpg']  # Add more formats as needed
    
    # Full paths
    json_file_path = os.path.join(directory, json_file)
    image_file_paths = [os.path.join(directory, img) for img in image_file_patterns]
    # Delete the JSON file if it exists
    if os.path.isfile(json_file_path):
        os.remove(json_file_path)
        print(f'Deleted JSON file: {json_file_path}')
    else:
        print(f'JSON file not found: {json_file_path}')

    # Delete image files if they exist
    for img_path in image_file_paths:
        if os.path.isfile(img_path):
            os.remove(img_path)
            print(f'Deleted image file: {img_path}')
        else:
            print(f'Image file not found: {img_path}')

    start_renaming1 = False
    start_renaming2 = False

    for filename in sorted(os.listdir(directory)):
        if filename.startswith("pet_info_") and filename.endswith(".json"): # renames json files and does -1 to each one
           
            try:
                current_id = int(filename.split("pet_info_")[1].split(".json")[0])
            except ValueError:
                continue  
            print(f"idul calculat current id:{current_id}")
            print(f"pet id {pet_id}" )
            print(f"max json id este :{maxJsonId}")
            
            if current_id > pet_id:
                print("MEOW")
                start_renaming1 = True

           
            if start_renaming1 and current_id <= maxJsonId:
             
                new_id = current_id - 1
                new_filename = f"pet_info_{new_id}.json"
                
                os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
                print(f"Renamed {filename} to {new_filename}")
        elif filename.startswith("image_") and filename.endswith(".jpg"): # renames files

            try:
                parts = filename.split("_")
                current_id = int(parts[1])
                image_number = parts[2].split(".jpg")[0]
            except (ValueError, IndexError):
                continue 

            
            if current_id > pet_id:
                start_renaming2 = True

            
            if start_renaming2 and current_id <= maxJsonId:
                new_id = current_id - 1
                new_filename = f"image_{new_id}_{image_number}.jpg"
                os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
                print(f"Renamed {filename} to {new_filename}")
           
            if current_id > maxJsonId:
                break
    temp_window.destroy()
    

    
def editPetsCommand(pet_id):
    global widgets
    directory = './files'
    file_name = f"pet_info_{pet_id}.json"
    file_path = os.path.join(directory, file_name)

    # Check if the file exists
    if os.path.exists(file_path):
        # Open and read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)  # This will load the contents of the JSON file into a dictionary
    pet_name = data.get('pet', {}).get('name', 'Unknown')
    pet_details = data.get('pet', {}).get('details', {})

    # Nested pet details
    pet_age = pet_details.get('age', 'Unknown')
    pet_type = pet_details.get('type', 'Unknown')
    pet_breed = pet_details.get('breed', 'Unknown')
    pet_sex = pet_details.get('sex', 'Unknown')
    pet_weight = pet_details.get('weight', 'Unknown')
    pet_color = pet_details.get('color', 'Unknown')
    pet_vaccinated = pet_details.get('vaccinated', 'Unknown')
    pet_microchipped = pet_details.get('microchipped', 'Unknown')
    pet_spayed_neutered = pet_details.get('spayed_neutered', 'Unknown')
    pet_special_needs = pet_details.get('special_needs', 'Unknown')
    pet_adoption_fee = pet_details.get('adoption_fee', 'Unknown')
    pet_images = pet_details.get('images', [])

    # Extract shelter details
    shelter_name = data.get('shelter', {}).get('name', 'Unknown')
    shelter_location = data.get('shelter', {}).get('location', {})
    shelter_contact = data.get('shelter', {}).get('contact', {})

    # Nested shelter location
    shelter_address = shelter_location.get('address', 'Unknown')
    shelter_city = shelter_location.get('city', 'Unknown')
    shelter_state = shelter_location.get('state', 'Unknown')
    shelter_zip = shelter_location.get('zip', 'Unknown')

    # Nested shelter contact
    shelter_phone = shelter_contact.get('phone', 'Unknown')
    shelter_email = shelter_contact.get('email', 'Unknown')
    shelter_website = shelter_contact.get('website', 'Unknown')
    



    

    

def open_temporary_windowDelete():#touple with the 
    global btnList

    directory = "files"

    pet_names = []

    for filename in os.listdir(directory):

        if filename.startswith("pet_info_") and filename.endswith(".json"):

            file_path = os.path.join(directory, filename)


            with open(file_path, 'r') as file:
                data = json.load(file)
            

            pet_name = data["pet"]["name"]
            print(pet_name)
            pet_names.append(pet_name)

    print(pet_name)
    temp_window = tk.Toplevel(root)
    temp_window.title("Delete Menu")
    temp_window.geometry("300x300")
    max = get_last_pet_info_id()
    # Set the window to stay on top
    temp_window.attributes("-topmost", True)
    btnList = []
    for i in range (max):
        
        btnList.append(tk.Button(temp_window , text = pet_names[i] , command = lambda i=i: deleteJsonBtnCmd(i+1,temp_window) ))

        btnList[i].pack()

    close_button = tk.Button(temp_window, text="Close", command=temp_window.destroy)
    close_button.pack()






def open_temporary_windowEdit():#touple with the 
    global btnList

    directory = "files"

    # List to store the names of all pets
    pet_names = []

    # Iterate through all files in the "files" directory
    for filename in os.listdir(directory):
        # Check if the file matches the "pet_info_{pet_id}.json" format
        if filename.startswith("pet_info_") and filename.endswith(".json"):
            # Construct the full file path
            file_path = os.path.join(directory, filename)

            # Open and load the JSON data from the file
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            # Extract the pet name from the JSON data
            pet_name = data["pet"]["name"]
            print(pet_name)
            # Append the pet name to the list
            pet_names.append(pet_name)

    print(pet_name)
    temp_window = tk.Toplevel(root)
    temp_window.title("Edit Menu")
    temp_window.geometry("300x300")
    max = get_last_pet_info_id()
    # Set the window to stay on top
    temp_window.attributes("-topmost", True)
    btnList = []
    for i in range (max):
        
        btnList.append(tk.Button(temp_window , text = pet_names[i] , command= lambda i=i : editPetsCommand(i+1)  ))

        btnList[i].pack()

    close_button = tk.Button(temp_window, text="Close", command=temp_window.destroy)
    close_button.pack()





def select_images():
    global selected
    image_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
    selected = 1
    for image_path in image_paths:
        image_listbox.insert(tk.END, image_path)

def resize_image(image_path, target_height):

    with Image.open(image_path) as img:
        aspect_ratio = img.width / img.height
        new_width = int(target_height * aspect_ratio)
        resized_img = img.resize((new_width, target_height))
        return resized_img
    

def convert_image_to_jpg(image_path):
    # Check if the image is already a JPG or JPEG
    if image_path.lower().endswith(('.jpg')):
        print(f"Image is already a JPG or JPEG: {image_path}")
        return image_path  

    directory, image_name = os.path.split(image_path)
    
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: The file at {image_path} was not found.")
        return None 

    rgb_image = image.convert("RGB")

    file_name, _ = os.path.splitext(image_name)

    new_image_name = f"{file_name}.jpg"

    destination_path = os.path.join(directory, new_image_name)

    rgb_image.save(destination_path, "JPEG")
    print(f"Image successfully converted and saved as {new_image_name} in the '{directory}' folder.")
    
    return destination_path  # Return the new JPG path



totalButtons = get_last_pet_info_id()


def generate_json_file():
    global selected
    letterOnly = []
    numberOnly = []
    entryIs = []
    whereBad = []
    allGood = 0

    

    pet_name = pet_name_entry.get()
    letterOnly.append(pet_name)

    age = age_entry.get()
    numberOnly.append(age)

    type_of_pet = type_entry.get()
    letterOnly.append(type_of_pet)

    breed = breed_entry.get()
    letterOnly.append(breed)

    sex = sex_entry.get()
    entryIs.append(sex)

    weight = weight_entry.get()
    numberOnly.append(weight)

    color = color_entry.get()
    letterOnly.append(color)

    special_needs = special_needs_entry.get()
    
    
    adoption_fee = adoption_fee_entry.get()
    numberOnly.append(adoption_fee)

    shelter_name = shelter_name_entry.get()
    entryIs.append(shelter_name)

    address = address_entry.get()
    entryIs.append(address)

    city = city_entry.get()
    entryIs.append(city)

    state = state_entry.get()
    letterOnly.append(state)

    zip_code = zip_entry.get()
    numberOnly.append(zip_code)

    phone = phone_entry.get()
    numberOnly.append(phone)

    email = email_entry.get()
    entryIs.append(email)

    website = website_entry.get()
    entryIs.append(website)

    vaccinated = vaccinated_entry.get()
    entryIs.append(vaccinated)

    microchipped = microchipped_entry.get()
    entryIs.append(microchipped)

    spayed_neutered = spayed_neutered_entry.get()
    entryIs.append(spayed_neutered)

    file_id = get_next_id()
    images = []

    for i in range (len(letterOnly)):
        if letterOnly[i].isalpha() == False:
            print(letterOnly[i])
            whereBad.append((letterOnly[i],1))
            allGood = 1

    for i in range (len(numberOnly)):
        if numberOnly[i].isdigit() == False:
            whereBad.append((numberOnly[i],2))
            allGood = 1

    for i in range(len(entryIs)):
        if entryIs[i] == "":
            whereBad.append((entryIs[i],3))
            allGood = 1
     #debug
        
            
    allGood = 0
    print (enumerate(image_listbox.get(0, tk.END)))
    if allGood == 0 and selected == 1:
        for idx, image_path in enumerate(image_listbox.get(0, tk.END)):
            image_extension = os.path.splitext(image_path)[1]
            new_image_name = f"image_{file_id}_{idx + 1}{image_extension}"

            destination_path = os.path.join("files", new_image_name)

            print(destination_path)
            if os.path.exists(destination_path):
                os.remove(destination_path)

            if Image.open(image_path).height != 280:
                resized_img = resize_image(image_path, 280)
                resized_img.save(destination_path)
            else:
                shutil.copy(image_path, destination_path)

            new_jpg_path = convert_image_to_jpg(destination_path)

            if new_jpg_path and new_jpg_path != destination_path:
                try:
                    os.remove(destination_path)  # delete converted file
                    print(f"Deleted original image: {destination_path}")
                except Exception as e:
                    print(f"Error deleting the file {destination_path}: {e}")

            
            images.append(new_jpg_path)
        data = {
            "pet": {
                "name": pet_name,
                "details": {
                    "age": age,
                    "type": type_of_pet,
                    "breed": breed,
                    "sex": sex,
                    "weight": weight,
                    "color": color,
                    "vaccinated": vaccinated,
                    "microchipped": microchipped,
                    "spayed_neutered": spayed_neutered,
                    "special_needs": special_needs,
                    "adoption_fee": adoption_fee,
                    "images": images
                }
            },
            "shelter": {
                "name": shelter_name,
                "location": {
                    "address": address,
                    "city": city,
                    "state": state,
                    "zip": zip_code
                },
                "contact": {
                    "phone": phone,
                    "email": email,
                    "website": website
                }
            }
        }

        with open(f"files/pet_info_{file_id}.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        messagebox.showinfo("Succes", f"Fișierul JSON a fost generat cu succes: pet_info_{file_id}.json")
    else:
        print("ERROR date incorecte/necorespunzatoare")
        open_temporary_window(whereBad,"Enter text",selected)

def deleteJsons():
    pog=1

root = tk.Tk()
root.title("Generator de informații despre animale de companie")
root.geometry("1200x600")

options = ["Da","Nu"]

widgets = [
    ("Nume animal de companie:", pet_name_entry := tk.Entry(root,fg="grey")),
    ("Vârstă:", age_entry := tk.Entry(root,fg="grey")),
    ("Tip:", type_entry := tk.Entry(root,fg="grey")),
    ("Rasă:", breed_entry := tk.Entry(root,fg="grey")),
    ("Sex :", sex_entry := ttk.Combobox(root,value=["Male","Female"], width = 17, state = "readonly")),
    ("Greutate:", weight_entry := tk.Entry(root,fg="grey")),
    ("Culoare:", color_entry := tk.Entry(root,fg="grey")),
    ("Vaccinat (Da/Nu):", vaccinated_entry := ttk.Combobox(root,value=options, width = 17, state = "readonly")),
    ("Microcipat (Da/Nu):", microchipped_entry := ttk.Combobox(root,value=options, width = 17, state = "readonly")),
    ("Sterilizat (Da/Nu):", spayed_neutered_entry := ttk.Combobox(root,value=options, width = 17, state = "readonly")),
    ("Nevoi speciale:", special_needs_entry := tk.Entry(root,fg="grey")),
    ("Taxă de adopție:", adoption_fee_entry := tk.Entry(root,fg="grey")),
    ("Numele adăpostului:", shelter_name_entry := tk.Entry(root,fg="grey")),
    ("Adresă:", address_entry := tk.Entry(root,fg="grey")),
    ("Oraș:", city_entry := tk.Entry(root,fg="grey")),
    ("Stat:", state_entry := tk.Entry(root,fg="grey")),
    ("Cod poștal:", zip_entry := tk.Entry(root,fg="grey")),
    ("Telefon:", phone_entry := tk.Entry(root,fg="grey")),
    ("Email:", email_entry := tk.Entry(root,fg="grey")),
    ("Website:", website_entry := tk.Entry(root,fg="grey"))
]

placeholdertxt="Enter text"
for label_text, entry_widget in widgets:
    if isinstance(entry_widget,tk.Entry)and not isinstance(entry_widget, ttk.Combobox):
        print(label_text,entry_widget)
        entry_widget.insert(0, placeholdertxt)  
        entry_widget.bind("<FocusIn>", lambda event, ew=entry_widget, pt=placeholdertxt: on_focus_in(ew, pt))  
        entry_widget.bind("<FocusOut>", lambda event, ew=entry_widget, pt=placeholdertxt: on_focus_out(ew, pt))  




for index, (label_text, entry) in enumerate(widgets):
    tk.Label(root, text=label_text).grid(row=index // 4, column=(index % 4) * 2, sticky="w", padx=5, pady=5)
    entry.grid(row=index // 4, column=(index % 4) * 2 + 1, padx=5, pady=5)

tk.Label(root, text="Selectați imagini:").grid(row=len(widgets) // 4, column=0, sticky="w", padx=5, pady=5)
select_images_button = tk.Button(root, text="Selectați imagini", command=select_images)
select_images_button.grid(row=len(widgets) // 4, column=1, padx=5, pady=5)

deleteMenu = tk.Button(root,text = "Delete Menu" , command = open_temporary_windowDelete)
deleteMenu.place(x= 900 , y=300)

editMenu = tk.Button(root,text = "Edit Menu", command = open_temporary_windowEdit)
editMenu.place(x= 900 , y=330)

image_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=5)
image_listbox.grid(row=(len(widgets) // 4) + 1, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

generate_button = tk.Button(root, text="Generează fișier JSON", command=generate_json_file)
generate_button.grid(row=(len(widgets) // 4) + 2, column=0, columnspan=4, pady=10)

root.mainloop()
