import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from tkinter import Tk, Entry, Button, StringVar, messagebox, Canvas, Frame, Label
from PIL import Image, ImageTk

# Load the dataset and preprocess
file_path = "C:\\Users\\91834\\Downloads\\survey lung cancer.csv"
data = pd.read_csv(file_path)

# Convert 'GENDER' and 'LUNG_CANCER' to numeric
data['GENDER'] = data['GENDER'].map({'M': 0, 'F': 1})
data['LUNG_CANCER'] = data['LUNG_CANCER'].map({'YES': 1, 'NO': 0})

# Ensure 'Age' is the first column in the dataset
data = data[['AGE'] + [col for col in data.columns if col != 'AGE']]

# Split features (X) and target (y)
X = data.drop('LUNG_CANCER', axis=1)
y = data['LUNG_CANCER']

# Train-test split and model training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Tkinter GUI for input and prediction
def predict_lung_cancer():
    try:
        input_data = pd.DataFrame([[int(var.get()) for var in entries]], columns=X.columns)
        prediction = model.predict(input_data)[0]
        result = "Lung Cancer Detected!" if prediction == 1 else "No Lung Cancer Detected!"
        messagebox.showinfo("Prediction Result", result)
        canvas.create_text(550, 750, text="Thank you for trusting us with your care. Stay healthy! 😊", 
                           font=("Arial", 14, "bold"), fill="white")
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Tkinter GUI Layout
root = Tk()
root.title("Lung Cancer Prediction")
root.geometry("1424x768")

# Load and resize the background image
image_path = "C:\\Users\\91834\\Downloads\\pics.jpg"
bg_image = Image.open(image_path)
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = Canvas(root, width=1424, height=768)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")
canvas.create_text(500, 40, text="Lung Cancer Prediction 🫁", font=("Arial", 20, "bold"), fill="white")

labels = list(X.columns)
entries = []
for i, label_text in enumerate(labels):
    canvas.create_text(500, 100 + i * 40, text=f"{label_text}:", font=("Arial", 18, "bold"), fill="white", anchor="e")
    entry_var = StringVar()
    entry = Entry(root, textvariable=entry_var, font=("Arial", 18), bg=root.cget('bg'), width=10, bd=2, relief="flat")
    canvas.create_window(600, 100 + i * 40, window=entry)
    entries.append(entry_var)

predict_button = Button(root, text="Predict", bg="lightgrey", font=("Arial", 18), command=predict_lung_cancer)
canvas.create_window(600, 710, window=predict_button)

# Function to display sample data
def display_data(sample):
    clear_table()
    table_frame.place(x=1000, y=100)
    for i, feature in enumerate(X.columns): # Ensure Age is first
        Label(table_frame, text=f"{feature}:", font=("Arial", 14, "bold"), bg="lightblue", width=20).grid(row=i, column=0, padx=10, pady=2)
        Label(table_frame, text=str(sample[feature]), font=("Arial", 14), bg="white", width=15).grid(row=i, column=1, padx=10, pady=2)
    Button(table_frame, text="X", font=("Arial", 12, "bold"), bg="red", fg="white", command=close_data_window).grid(row=i+1, column=1, padx=10, pady=10)

# Show sample healthy/unhealthy data
def show_healthy_data():
    display_data(data[data["LUNG_CANCER"] == 0].sample(n=1).iloc[0].to_dict())

def show_unhealthy_data():
    display_data(data[data["LUNG_CANCER"] == 1].sample(n=1).iloc[0].to_dict())

# Clear and close table functions
def clear_table():
    for widget in table_frame.winfo_children():
        widget.destroy()

def close_data_window():
    table_frame.place_forget()

table_frame = Frame(root, bg="lightblue", padx=10, pady=10)

healthy_button = Button(root, text="Healthy Data", bg="green", fg="white", font=("Arial", 14, "bold"), command=show_healthy_data)
canvas.create_window(1150, 50, window=healthy_button)

unhealthy_button = Button(root, text="Unhealthy Data", bg="red", fg="white", font=("Arial", 14, "bold"), command=show_unhealthy_data)
canvas.create_window(1400, 50, window=unhealthy_button)

root.mainloop()