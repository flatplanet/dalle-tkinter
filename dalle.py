from tkinter import *
import customtkinter
from tkinter import messagebox
from tkinter import filedialog
import openai
from PIL import ImageTk, Image
import requests
from io import BytesIO
import os
import pickle


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Create our app
root = customtkinter.CTk()
root.title('Displaced.ai Dall-e Image app')
root.geometry('700x300')


# Grab the API Key
def grab_key():
	# Define filename
	filename = 'api_key'
	try:
		if os.path.isfile(filename):
			# open the file
			input_file = open(filename, 'rb')

			# Load the data into a variable
			stuff = pickle.load(input_file)

			# output stuff to entry box
			return stuff

		else:
			# Create the file 
			input_file = open(filename, 'wb')
			# Close the file
			input_file.close()

	except Exception as e:
		messagebox.showinfo("Whoops!", f'Error: {e}')

# Save API Key Function
def save_key():
	# Create a New window
	api_window = customtkinter.CTkToplevel(root)
	api_window.title("API Key")
	api_window.geometry("400x200")

	def saver():
		# Define filename
		filename = 'api_key'
		try:
			# open the file
			output_file = open(filename, 'wb')

			# Add the stuff to the file
			pickle.dump(api_entry.get(), output_file)
			messagebox.showinfo("Saved!", 'Your API Key Was Saved!')
			# Close the window
			api_window.destroy()
			api_window.update()
		

		except Exception as e:
			messagebox.showinfo("Whoops!", f'Error: {e}')

	def get_key():
		# Define filename
		filename = 'api_key'
		try:
			if os.path.isfile(filename):
				# open the file
				input_file = open(filename, 'rb')

				# Load the data into a variable
				stuff = pickle.load(input_file)

				# output stuff to entry box
				api_entry.insert(0, stuff)

			else:
				# Create the file 
				input_file = open(filename, 'wb')
				# Close the file
				input_file.close()




		except Exception as e:
			messagebox.showinfo("Whoops!", f'Error: {e}')



	# Add Label
	api_label = customtkinter.CTkLabel(api_window, text="API Key", font=("Helvetica", 18))
	api_label.pack(pady=20)

	# Add entry box
	api_entry = customtkinter.CTkEntry(api_window, width=300)
	api_entry.pack(pady=10)

	# Add Button
	save_api_button = customtkinter.CTkButton(api_window, text="Save Key", command=saver)
	save_api_button.pack(pady=10)

	# Get the key
	get_key()

# Create function
def generate():
	# Get the text from the box
	prompt = my_text.get("0.0", "end")
	# Get the size options
	size = radio_var.get()

	# Check to make sure they typed something
	if my_text.compare("end-1c", "==", "1.0"):
		messagebox.showinfo("Whoops!", "You forgot to fill out the text box!  Try again!")
	else:
		try:
			# Get the api key with pickle
			key = grab_key()
			# set the api key
			#openai.api_key = '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'
			openai.api_key = key
			# Get a response
			response = openai.Image.create(prompt=prompt, n=1, size=f'{size}x{size}')
			# Get image URL
			image_url = response['data'][0]['url']
			
			# Create some new windows
			new_window = customtkinter.CTkToplevel(root)
			new_window.title(f'{size}x{size}')
			new_window.geometry(f'{size}x{size}')

			def copy_url():
				# Clear the clipboard
				new_window.clipboard_clear()
				# Copy to Clipboard
				new_window.clipboard_append(image_url)
				# Throw up a success message
				messagebox.showinfo("Copied!", "Your URL has been copied successfully!")


			def save_image():
				file_name = filedialog.asksaveasfilename(initialdir="C:/dalle/images",
					title="Save Image",
					filetypes=(("PNG Files", "*.png"), ("All Files", "*.*")))

				if file_name:
					# Make sure filename ends in png
					if file_name.endswith(".png"):
						pass
					else:
						file_name = f"{file_name}.png"

					# save the file
					saved_image = Image.open(BytesIO(img_data)).save(file_name)
					messagebox.showinfo("Saved!", "Your Image Has Been Saved!!")
				else:
					messagebox.showinfo("Whoops!", "You Forgot To Enter A FileName, Please Try Again")






			# Add a Menu
			my_menu = Menu(new_window)
			optionbar = Menu(my_menu, tearoff=0)
			optionbar.add_command(label="Copy URL", command=copy_url)
			optionbar.add_command(label="Save Image", command=save_image)

			my_menu.add_cascade(label="File", menu=optionbar)
			new_window.config(menu=my_menu)


			# Add Image To Our App
			response_image = requests.get(image_url)
			img_data = response_image.content
			img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
			# Add a label to the new window
			panel = customtkinter.CTkLabel(new_window, image=img, text='')
			panel.pack(side="bottom", fill="both", expand="yes")

			# Delete From Text Box
			my_text.delete('0.0', 'end')
		
		except Exception as e:
			# delete from our textbox
			#my_text.delete('0.0', 'end')
			# Insert Error Message
			#my_text.insert("end", e)

			# Pop up error message
			messagebox.showinfo("OpenAI Error", f'{e}')




# Create a Textbox
my_text = customtkinter.CTkTextbox(root, width=650, height=200)
my_text.pack(pady=10)

# Create a Frame to hold buttons
my_frame = customtkinter.CTkFrame(root)
my_frame.pack()

# Create some radio buttons 
radio_var = customtkinter.IntVar(value=256)
rb1 = customtkinter.CTkRadioButton(my_frame, text="256x256", variable=radio_var, value=256)
rb2 = customtkinter.CTkRadioButton(my_frame, text="512x512", variable=radio_var, value=512)
rb3 = customtkinter.CTkRadioButton(my_frame, text="1024x1024", variable=radio_var, value=1024)
# Add the buttons to the screen
rb1.grid(row=0, column=0)
rb2.grid(row=0, column=1)
rb3.grid(row=0, column=2)

# Add Frame
my_frame = customtkinter.CTkFrame(root)
my_frame.pack(pady=10)

# Add a Button
my_button = customtkinter.CTkButton(my_frame, text="Generate Image", command=generate)
my_button.grid(row=0, column=0, padx=10)

api_button = customtkinter.CTkButton(my_frame, text="API Key", command=save_key)
api_button.grid(row=0, column=1)







root.mainloop()